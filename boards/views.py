from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import models
from django.utils import timezone

from .models import Board, BoardMember, BoardInvitation, InvitationStatus
from .forms import BoardForm, InviteUserForm

User = get_user_model()


@login_required
def board_list(request):
    """Главная страница со списком досок пользователя"""
    user_boards = Board.objects.filter(
        models.Q(owner=request.user) |
        models.Q(members__user=request.user)
    ).distinct().order_by('-created_at')

    pending_invitations = BoardInvitation.objects.filter(
        invited_user=request.user,
        status=InvitationStatus.PENDING
    ).select_related('board', 'invited_by')

    return render(request, 'boards/board_list.html', {
        'boards': user_boards,
        'pending_invitations': pending_invitations
    })


@login_required
def board_create(request):
    """Создание новой доски"""
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()

            BoardMember.objects.create(
                board=board,
                user=request.user,
                role='owner'
            )

            messages.success(
                request, f'Доска "{board.title}" успешно создана!'
            )
            return redirect('boards:board_detail', board_id=board.id)
    else:
        form = BoardForm()

    return render(request, 'boards/board_create.html', {'form': form})


@login_required
def board_detail(request, board_id):
    """Детальная страница доски с задачами"""
    board = get_object_or_404(Board, id=board_id)

    if not (board.owner == request.user or
            board.members.filter(user=request.user).exists()):
        messages.error(request, 'У вас нет доступа к этой доске.')
        return redirect('boards:board_list')

    tasks_by_status = {
        'todo': board.tasks.filter(
            status='todo'
        ).order_by('position', 'created_at'),
        'in_progress': board.tasks.filter(
            status='in_progress'
        ).order_by('position', 'created_at'),
        'review': board.tasks.filter(
            status='review'
        ).order_by('position', 'created_at'),
        'done': board.tasks.filter(
            status='done'
        ).order_by('position', 'created_at'),
    }

    board_members = User.objects.filter(
        models.Q(id=board.owner.id) |
        models.Q(board_members__board=board)
    ).distinct()

    return render(request, 'boards/board_detail.html', {
        'board': board,
        'tasks_by_status': tasks_by_status,
        'board_members': board_members,
    })


@login_required
@require_POST
def board_delete(request, board_id):
    """Удаление доски"""
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    board_title = board.title
    board.delete()

    messages.success(request, f'Доска "{board_title}" удалена.')
    return redirect('boards:board_list')


@login_required
def board_invite_user(request, board_id):
    """Приглашение пользователя в доску"""
    board = get_object_or_404(Board, id=board_id, owner=request.user)

    if request.method == 'POST':
        form = InviteUserForm(request.POST, board=board)
        if form.is_valid():
            user_to_invite = form.cleaned_data['username']

            if (
                board.owner == user_to_invite or board.members.filter(
                    user=user_to_invite
                ).exists()
            ):
                messages.warning(
                    request, f'{user_to_invite.username} уже участник доски.'
                )
                return redirect('boards:board_detail', board_id=board.id)

            existing_invitation = BoardInvitation.objects.filter(
                board=board,
                invited_user=user_to_invite,
                status=InvitationStatus.PENDING
            ).first()

            if existing_invitation:
                messages.warning(
                    request, f'{
                        user_to_invite.username
                    } уже приглашен в эту доску.'
                )
                return redirect('boards:board_detail', board_id=board.id)

            BoardInvitation.objects.create(
                board=board,
                invited_user=user_to_invite,
                invited_by=request.user
            )

            messages.success(
                request, f'Приглашение отправлено пользователю {
                    user_to_invite.username
                }!'
            )
            return redirect('boards:board_detail', board_id=board.id)
    else:
        form = InviteUserForm(board=board)

    return render(request, 'boards/board_invite.html', {
        'board': board,
        'form': form
    })


@login_required
@require_POST
def invitation_respond(request, invitation_id):
    """Ответ на приглашение (принять/отклонить)"""
    invitation = get_object_or_404(
        BoardInvitation,
        id=invitation_id,
        invited_user=request.user,
        status=InvitationStatus.PENDING
    )

    action = request.POST.get('action')

    if action == 'accept':
        invitation.status = InvitationStatus.ACCEPTED
        invitation.responded_at = timezone.now()
        invitation.save()

        BoardMember.objects.create(
            board=invitation.board,
            user=request.user,
            role='member'
        )

        messages.success(
            request, f'Вы присоединились к доске "{invitation.board.title}"!'
        )

    elif action == 'decline':
        invitation.status = InvitationStatus.DECLINED
        invitation.responded_at = timezone.now()
        invitation.save()

        messages.info(
            request, f'Приглашение к доске "{
                invitation.board.title
            }" отклонено.'
        )

    return redirect('boards:board_list')

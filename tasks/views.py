from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Task
from .forms import TaskForm
from boards.models import Board


@login_required
@require_POST
def task_create(request, board_id):
    """Создание новой задачи"""
    board = get_object_or_404(Board, id=board_id)

    if not (board.owner == request.user or
            board.members.filter(user=request.user).exists()):
        messages.error(request, 'У вас нет доступа к этой доске.')
        return redirect('boards:board_list')

    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)

            task = Task.objects.create(
                title=data.get('title'),
                description=data.get('description', ''),
                board=board,
                status=data.get('status', 'todo'),
                assignee_id=data.get('assignee') if data.get('assignee') else None,
                creator=request.user
            )

            return JsonResponse({
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'status': task.status,
                    'assignee': task.assignee.username if task.assignee else None,
                    'created_at': task.created_at.strftime('%d.%m')
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        form = TaskForm(request.POST, board=board)
        if form.is_valid():
            task = form.save(commit=False)
            task.board = board
            task.creator = request.user
            task.save()

            messages.success(request, f'Задача "{task.title}" создана!')
            return redirect('boards:board_detail', board_id=board.id)
        else:
            messages.error(request, 'Ошибка при создании задачи.')
            return redirect('boards:board_detail', board_id=board.id)


@login_required
@require_POST
def task_update_status(request, task_id):
    """Обновление статуса задачи (для drag & drop)"""
    task = get_object_or_404(Task, id=task_id)

    if not (task.board.owner == request.user or
            task.board.members.filter(user=request.user).exists()):
        return JsonResponse({'success': False, 'error': 'Нет доступа'})

    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')

            valid_statuses = ['todo', 'in_progress', 'review', 'done']
            if new_status not in valid_statuses:
                return JsonResponse({'success': False, 'error': 'Неверный статус'})

            task.status = new_status
            task.save()

            return JsonResponse({
                'success': True,
                'task_id': task.id,
                'new_status': new_status,
                'message': f'Задача "{
                    task.title
                }" перемещена в "{task.get_status_display()}"'
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Неверный тип запроса'})

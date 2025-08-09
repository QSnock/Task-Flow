from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Role(models.TextChoices):
    OWNER = 'owner', 'Владелец'
    MEMBER = 'member', 'Участник'


class Board(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Владелец'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'


class BoardMember(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        verbose_name='Доска',
        related_name='members'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='board_members'
    )
    role = models.CharField(
        max_length=100,
        verbose_name='Роль',
        choices=Role.choices,
    )
    added_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Участник доски'
        verbose_name_plural = 'Участники доски'
        unique_together = ('board', 'user')
        ordering = ('-added_at',)


class InvitationStatus(models.TextChoices):
    PENDING = 'pending', 'Ожидает'
    ACCEPTED = 'accepted', 'Принято'
    DECLINED = 'declined', 'Отклонено'


class BoardInvitation(models.Model):
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, verbose_name='Доска',
        related_name='invitations'
    )
    invited_user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Приглашенный пользователь',
        related_name='board_invitations'
    )
    invited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пригласил',
        related_name='sent_invitations'
    )
    status = models.CharField(
        max_length=20, choices=InvitationStatus.choices,
        default=InvitationStatus.PENDING, verbose_name='Статус'
    )
    invited_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата приглашения'
    )
    responded_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Дата ответа'
    )

    class Meta:
        verbose_name = 'Приглашение в доску'
        verbose_name_plural = 'Приглашения в доски'
        unique_together = ('board', 'invited_user')
        ordering = ('-invited_at',)

    def __str__(self):
        return (
            f'{self.invited_user.username} -> {self.board.title} '
            f'({self.status})'
        )

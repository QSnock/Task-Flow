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
        Board, on_delete=models.CASCADE, verbose_name='Доска'
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

from django.db import models
from django.contrib.auth import get_user_model

from boards.models import Board

User = get_user_model()


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        verbose_name='Доска'
    )
    status = models.CharField(max_length=100, verbose_name='Статус')
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        verbose_name='Исполнитель'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name='Создатель'
    )
    position = models.IntegerField(default=0, verbose_name='Позиция')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата обновления'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

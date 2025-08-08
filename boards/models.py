from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Board(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'


class BoardMember(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Участник доски'
        verbose_name_plural = 'Участники доски'

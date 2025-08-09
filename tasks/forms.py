from django import forms
from django.contrib.auth import get_user_model
from django.db import models

from .models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assignee']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название задачи'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание задачи (необязательно)',
                'rows': 3
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assignee': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'status': 'Статус',
            'assignee': 'Исполнитель',
        }

    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board', None)
        super().__init__(*args, **kwargs)

        if board:
            board_members = User.objects.filter(
                models.Q(id=board.owner.id) |
                models.Q(board_members__board=board)
            ).distinct()

            self.fields['assignee'].queryset = board_members
            self.fields['assignee'].empty_label = "Не назначено"

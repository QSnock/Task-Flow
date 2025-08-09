from django import forms
from django.contrib.auth import get_user_model
from django.db import models

from .models import Board

User = get_user_model()


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название доски'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание доски (необязательно)',
                'rows': 3
            }),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
        }


class InviteUserForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите username или выберите из списка',
            'list': 'usersList'
        }),
        label='Имя пользователя'
    )

    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board', None)
        super().__init__(*args, **kwargs)

        if board:
            excluded_users = User.objects.filter(
                models.Q(id=board.owner.id) |
                models.Q(board_members__board=board)
            ).values_list('id', flat=True)
            self.available_users = User.objects.exclude(
                id__in=excluded_users
            ).order_by('username')[:50]

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(
                'Пользователь с таким username не найден.'
            )

        return user

from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path(
        'board/<int:board_id>/create/', views.task_create, name='task_create'
    ),
    path(
        '<int:task_id>/update-status/',
        views.task_update_status,
        name='task_update_status'
    ),
]

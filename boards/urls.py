from django.urls import path

from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('create/', views.board_create, name='board_create'),
    path('<int:board_id>/', views.board_detail, name='board_detail'),
    path('<int:board_id>/delete/', views.board_delete, name='board_delete'),
    path(
        '<int:board_id>/invite/', views.board_invite_user, name='board_invite'
    ),
    path(
        'invitation/<int:invitation_id>/respond/',
        views.invitation_respond,
        name='invitation_respond'
    ),
]

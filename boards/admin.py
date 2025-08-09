from django.contrib import admin

from boards.models import Board, BoardMember, BoardInvitation


@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'board', 'user', 'role', 'added_at')
    list_filter = ('role', 'added_at')
    search_fields = ('board__title', 'user__username')
    list_select_related = ('board', 'user')


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'owner')
    list_editable = ('title',)
    search_fields = ('title', 'description', 'owner__username')
    list_select_related = ('owner',)


@admin.register(BoardInvitation)
class BoardInvitationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'board', 'invited_user', 'invited_by', 'status', 'invited_at'
    )
    list_filter = ('status', 'invited_at', 'responded_at')
    search_fields = (
        'board__title', 'invited_user__username', 'invited_by__username'
    )
    list_select_related = ('board', 'invited_user', 'invited_by')
    list_editable = ('status',)

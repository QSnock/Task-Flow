from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'board', 'status', 'assignee', 'creator', 'created_at'
    )
    list_filter = ('status', 'board', 'assignee', 'creator', 'created_at')
    search_fields = ('title', 'description', 'board__title')
    list_editable = ('status', 'assignee')
    list_select_related = ('board', 'assignee', 'creator')

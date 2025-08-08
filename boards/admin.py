from django.contrib import admin

from boards.models import Board, BoardMember


class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'board', 'user', 'role', 'added_at')
    list_filter = ('role', 'added_at')
    search_fields = ('board__title', 'user__username')
    list_select_related = ('board', 'user')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'owner')
    list_editable = ('title',)
    search_fields = ('title', 'description', 'owner__username')
    list_select_related = ('owner',)


admin.site.register(Board, BoardAdmin)
admin.site.register(BoardMember, BoardMemberAdmin)

from django.contrib import admin
from tracker.models import Issue, Status, Type, Project


class IssueAdmin(admin.ModelAdmin):
    list_display = ('summary', 'project', 'status', 'created_at', 'updated_at')
    list_filter = ('project', 'status', 'type')
    search_fields = ('summary', 'description')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)

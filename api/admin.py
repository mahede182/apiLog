from django.contrib import admin
from .models import Note
from drf_api_logger.models import APILogsModel

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')

# Ensure APILogsModel is registered
if not admin.site.is_registered(APILogsModel):
    @admin.register(APILogsModel)
    class APILogsAdmin(admin.ModelAdmin):
        list_display = ['id', 'api', 'method', 'status_code', 'execution_time', 'added_on']
        list_filter = ['method', 'status_code', 'added_on']
        search_fields = ['api', 'method', 'status_code']
        readonly_fields = [field.name for field in APILogsModel._meta.fields]

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return False

        def has_delete_permission(self, request, obj=None):
            return False

from django.contrib import admin
from django.utils.html import format_html
from .models import FileAnalysis

@admin.register(FileAnalysis)
class FileAnalysisAdmin(admin.ModelAdmin):
    # Define color scheme for all crypto types
    CRYPTO_TYPE_COLORS = {
        'symmetric': '#27ae60',    # Green
        'asymmetric': '#2980b9',   # Blue
        'hash': '#8e44ad',         # Purple
        'hmac': '#d35400',         # Orange
        'kdf': '#c0392b',          # Red
        'default': '#7f8c8d'       # Gray (fallback)
    }

    list_display = ('file_name_display', 'user_display', 'crypto_type_display', 
                   'algorithm_display', 'file_size_display', 'timestamp_display', 
                   'estimated_time_display')
    
    list_filter = ('crypto_type', 'algorithm', 'user', 'metric')  # Removed 'visualization'
    search_fields = ('file_name', 'user__username', 'algorithm')
    readonly_fields = ('timestamp', 'estimated_time')
    
    fieldsets = (
        ('File Information', {
            'fields': ('file_name', 'file_size', 'file_type',)
        }),
        ('Analysis Configuration', {
            'fields': ('crypto_type', 'algorithm', 'metric', 'visualization', 'bar_type',)
        }),
        ('Results', {
            'fields': ('estimated_time', 'timestamp',)
        }),
        ('User Information', {
            'fields': ('user',)
        }),
    )

    def file_name_display(self, obj):
        return format_html('<span style="color: #447e9b;">{}</span>', obj.file_name)
    file_name_display.short_description = 'File Name'

    def user_display(self, obj):
        return format_html('<strong>{}</strong>', obj.user.username)
    user_display.short_description = 'User'

    def crypto_type_display(self, obj):
        color = self.CRYPTO_TYPE_COLORS.get(obj.crypto_type, self.CRYPTO_TYPE_COLORS['default'])
        return format_html('<span style="color: {};">{}</span>', 
                         color, 
                         obj.crypto_type.title())
    crypto_type_display.short_description = 'Cryptography Type'

    def algorithm_display(self, obj):
        return format_html('<span style="font-family: monospace;">{}</span>', 
                         obj.algorithm.upper())
    algorithm_display.short_description = 'Algorithm'

    def file_size_display(self, obj):
        size = '{:.2f}'.format(obj.file_size)
        return format_html('<span style="font-family: monospace;">{} KB</span>', size)
    file_size_display.short_description = 'File Size'

    def timestamp_display(self, obj):
        return format_html('<span style="color: #666;">{}</span>', 
                         obj.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
    timestamp_display.short_description = 'Timestamp'

    def estimated_time_display(self, obj):
        if obj.estimated_time is None:
            return '-'
        time = '{:.4f}'.format(obj.estimated_time)
        return format_html('<span style="font-family: monospace; color: #d35400;">{} s</span>', time)
    estimated_time_display.short_description = 'Estimated Time'

    def has_add_permission(self, request):
        return False

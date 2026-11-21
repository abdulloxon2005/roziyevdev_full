
from django.contrib import admin
from .models import VisitorLog
from .models import VisitorLog, SystemLog
from .models import VisitorLog, SystemLog, SecurityLog

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "user",
        "path",
        "method",
        "status_code",
        "visited_at",
    )

    list_filter = (
        "method",
        "status_code",
        "visited_at",
    )

    search_fields = (
        "ip_address",
        "path",
        "user__username",
    )

    readonly_fields = (
        "user",
        "ip_address",
        "path",
        "method",
        "status_code",
        "user_agent",
        "referrer",
        "visited_at",
    )

    date_hierarchy = "visited_at"
    ordering = ("-visited_at",)



@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = (
        "level",
        "logger_name",
        "path",
        "created_at",
    )

    list_filter = (
        "level",
        "created_at",
    )

    search_fields = (
        "message",
        "logger_name",
        "path",
    )

    readonly_fields = (
        "level",
        "logger_name",
        "message",
        "path",
        "created_at",
    )

    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):

    list_display = (
        "ip_address",
        "event_type",
        "severity",
        "path",
        "created_at",
    )

    list_filter = (
        "severity",
        "event_type",
        "created_at",
    )

    search_fields = (
        "ip_address",
        "path",
        "description",
    )

    readonly_fields = (
        "ip_address",
        "event_type",
        "severity",
        "path",
        "description",
        "user_agent",
        "created_at",
    )

    date_hierarchy = "created_at"
    ordering = ("-created_at",)

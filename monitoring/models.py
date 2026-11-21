
from django.db import models
from django.contrib.auth.models import User


class VisitorLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    path = models.CharField(max_length=500)

    method = models.CharField(max_length=10)

    status_code = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    referrer = models.URLField(
        max_length=1000,
        blank=True,
    )

    visited_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-visited_at"]
        indexes = [
            models.Index(fields=["-visited_at"]),
            models.Index(fields=["ip_address"]),
        ]

    def __str__(self):
        return f"{self.ip_address} - {self.path}"

#loglar

class SystemLog(models.Model):
    LEVEL_CHOICES = [
        ("DEBUG", "Debug"),
        ("INFO", "Info"),
        ("WARNING", "Warning"),
        ("ERROR", "Error"),
        ("CRITICAL", "Critical"),
    ]

    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
    )

    logger_name = models.CharField(
        max_length=255,
        blank=True,
    )

    message = models.TextField()

    path = models.CharField(
        max_length=500,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["level"]),
        ]

    def __str__(self):
        return f"{self.level} - {self.created_at}"




class SecurityLog(models.Model):
    SEVERITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    event_type = models.CharField(max_length=100)

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default="LOW",
    )

    path = models.CharField(max_length=500, blank=True)

    description = models.TextField()

    user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.severity} - {self.event_type}"

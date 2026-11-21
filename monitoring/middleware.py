
from django.utils.deprecation import MiddlewareMixin
from .models import VisitorLog


class VisitorTrackingMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        path = request.path

        # Admin, static va media fayllarni kuzatmaymiz
        if (
            path.startswith("/admin/")
            or path.startswith("/static/")
            or path.startswith("/media/")
        ):
            return response

        # Faqat sahifalarni ochish so'rovlarini qayd qilamiz
        if request.method != "GET":
            return response

        # IP manzilni olish
        ip_address = request.META.get("REMOTE_ADDR")

        # Brauzer va qurilma ma'lumotlari
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        # Qaysi sahifadan kelgani
        referrer = request.META.get("HTTP_REFERER", "")

        # Login qilgan foydalanuvchi
        user = request.user if request.user.is_authenticated else None

        VisitorLog.objects.create(
            user=user,
            ip_address=ip_address,
            path=path,
            method=request.method,
            status_code=response.status_code,
            user_agent=user_agent,
            referrer=referrer,
        )

        return response



import logging

error_logger = logging.getLogger("roziyevdev")


class ErrorTrackingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

            if response.status_code >= 400:
                error_logger.warning(
                    "HTTP %s | %s %s",
                    response.status_code,
                    request.method,
                    request.path,
                )

            return response

        except Exception:
            error_logger.exception(
                "UNHANDLED EXCEPTION | %s %s",
                request.method,
                request.path,
            )
            raise



from .security import detect_suspicious_request


class SecurityMonitoringMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            detect_suspicious_request(request, response)
        except Exception:
            error_logger.exception(
                "Security monitoring error"
            )

        return response

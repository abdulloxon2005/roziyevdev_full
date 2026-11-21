
from .models import SecurityLog


SUSPICIOUS_PATHS = [
    "/.env",
    "/wp-admin/",
    "/phpmyadmin/",
    "/wp-login.php",
    "/.git/config",
    "/config.php",
]

SQL_PATTERNS = [
    "union select",
    "select * from",
    "or 1=1",
    "drop table",
    "insert into",
    "information_schema",
]


def detect_suspicious_request(request, response):
    path = request.path.lower()
    query = request.META.get("QUERY_STRING", "").lower()

    full_request = f"{path}?{query}"

    event_type = None
    severity = "LOW"
    description = ""

    if any(item in path for item in SUSPICIOUS_PATHS):
        event_type = "SUSPICIOUS_PATH"
        severity = "HIGH"
        description = "Shubhali fayl yoki admin manziliga murojaat"

    elif any(item in full_request for item in SQL_PATTERNS):
        event_type = "POSSIBLE_SQL_INJECTION"
        severity = "HIGH"
        description = "SQL Injection belgilariga o'xshash so'rov"

    elif response.status_code == 404:
        return

    if event_type:
        ip_address = request.META.get("REMOTE_ADDR")

        SecurityLog.objects.create(
            ip_address=ip_address,
            event_type=event_type,
            severity=severity,
            path=request.path,
            description=description,
            user_agent=request.META.get(
                "HTTP_USER_AGENT", ""
            ),
        )


import logging


class DatabaseLogHandler(logging.Handler):

    def emit(self, record):
        try:
            from .models import SystemLog

            message = self.format(record)

            request = getattr(record, "request", None)
            path = request.path if request else ""

            SystemLog.objects.create(
                level=record.levelname,
                logger_name=record.name,
                message=message,
                path=path,
            )

        except Exception:
            self.handleError(record)

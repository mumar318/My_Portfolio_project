from __future__ import annotations

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from .models import PageView


class AnalyticsMiddleware(MiddlewareMixin):
    """Very lightweight page view tracking.

    - Tracks only GET requests
    - Skips admin, static and media paths
    - Respects "Do Not Track" header
    - Uses anonymised IP where possible
    """

    def process_response(self, request, response):  # type: ignore[override]
        try:
            if request.method != "GET":
                return response

            path = request.path or "/"

            # Skip admin and static/media assets
            if path.startswith("/admin"):
                return response
            if settings.STATIC_URL and path.startswith(settings.STATIC_URL):
                return response
            if settings.MEDIA_URL and path.startswith(settings.MEDIA_URL):
                return response

            # Respect Do Not Track
            if request.headers.get("DNT") == "1":
                return response

            # Only log successful-ish responses
            if response.status_code >= 400:
                return response

            session_key = request.session.session_key
            if not session_key:
                # Ensure session exists
                request.session.save()
                session_key = request.session.session_key

            ip = request.META.get("REMOTE_ADDR")
            # Very light anonymisation: drop the last octet for IPv4
            if ip and "." in ip:
                parts = ip.split(".")
                if len(parts) == 4:
                    ip = ".".join(parts[:3] + ["0"])

            user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
            referrer = request.META.get("HTTP_REFERER", "")

            PageView.objects.create(
                path=path,
                session_key=session_key or "unknown",
                ip_address=ip or None,
                user_agent=user_agent,
                referrer=referrer,
            )
        except Exception:
            # Never break the request flow because of analytics issues
            pass

        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add a set of sensible security headers.

    These are intentionally conservative and compatible with the current
    use of inline scripts and external CDNs.
    """

    def process_response(self, request, response):  # type: ignore[override]
        # Basic hardening headers
        response.setdefault("X-Content-Type-Options", "nosniff")
        response.setdefault("X-Frame-Options", "DENY")
        response.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")

        # Simple Content Security Policy that still allows current inline usage
        csp = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com; "
            "style-src 'self' 'unsafe-inline'; "
            "connect-src 'self'; "
            "font-src 'self' data:; "
            "object-src 'none';"
        )
        response.setdefault("Content-Security-Policy", csp)

        # HSTS only when not in DEBUG
        if not getattr(settings, "DEBUG", True):
            response.setdefault(
                "Strict-Transport-Security",
                "max-age=63072000; includeSubDomains; preload",
            )

        return response

from __future__ import annotations

from typing import Dict, Any

from .models import SiteSettings, Profile


def site_settings(request) -> Dict[str, Any]:  # pragma: no cover - small helper
    """Expose a SiteSettings instance to all templates as `site_settings`.

    If no settings row exists yet, returns sensible defaults without writing
    anything to the database.
    """

    settings_obj = SiteSettings.objects.first()
    if settings_obj is None:
        # Return an unsaved instance with very generic defaults.
        settings_obj = SiteSettings(
            site_name="My Portfolio",
            site_description="Personal portfolio website.",
            site_keywords="portfolio, developer, projects, resume",
        )

    profile_obj = Profile.objects.first()

    return {"site_settings": settings_obj, "profile": profile_obj}

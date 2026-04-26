from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

import json

from .forms import ContactForm
from .models import (
    AboutStat,
    Certification,
    EducationEntry,
    ExperienceEntry,
    Project,
    Category,
    ResumeProjectHighlight,
    SkillCategory,
    Profile,
    Technology,
)


def home(request):
    """Home page view driven from DB Profile/Stats/Projects/Technologies."""

    profile = Profile.objects.first()

    stats_qs = AboutStat.objects.all().order_by("order")
    stats = [
        {"number": s.number, "label": s.label, "description": s.description}
        for s in stats_qs
    ]

    featured_tech = list(
        Technology.objects.filter(featured_on_home=True)
        .order_by("order")
        .values("name", "icon")
    )

    featured_projects = (
        Project.objects.filter(featured=True)
        .order_by("order", "-created_at")[:6]
    )

    context = {
        "profile": profile,
        "stats": stats,
        "featured_tech": featured_tech,
        "featured_projects": featured_projects,
    }
    return render(request, 'portfolio/home.html', context)

def about(request):
    """About page view (DB-driven)."""

    stats_qs = AboutStat.objects.all().order_by('order')
    stats = [
        {"number": s.number, "label": s.label, "description": s.description}
        for s in stats_qs
    ]

    skills_context = {}
    for category in (
        SkillCategory.objects.filter(section__in=["about", "both"])
        .prefetch_related("skills")
        .order_by("order")
    ):
        skills_context[category.name] = [
            {"name": sk.name, "level": sk.level or 0}
            for sk in category.skills.all().order_by("order")
        ]

    education = []
    for edu in EducationEntry.objects.filter(
        section__in=["about", "both"]
    ).order_by("order"):
        highlights = [
            line.strip() for line in (edu.highlights or "").splitlines() if line.strip()
        ]
        education.append(
            {
                "degree": edu.degree,
                "institution": edu.institution,
                "year": edu.period,
                "grade": edu.grade,
                "highlights": highlights,
            }
        )

    experience = []
    for exp in ExperienceEntry.objects.filter(
        section__in=["about", "both"]
    ).order_by("order"):
        achievements = [
            line.strip() for line in (exp.achievements or "").splitlines() if line.strip()
        ]
        experience.append(
            {
                "company": exp.company,
                "role": exp.role,
                "period": exp.period,
                "type": exp.employment_type or "",
                "achievements": achievements,
            }
        )

    context = {
        "stats": stats,
        "skills": skills_context,
        "education": education,
        "experience": experience,
    }
    return render(request, "portfolio/about.html", context)

def projects(request):
    """Projects page view (DB-backed)."""
    qs = Project.objects.prefetch_related('categories', 'technologies').order_by('-featured', 'order', '-created_at')

    projects_list = []
    for project in qs:
        categories = [c.name for c in project.categories.all()]
        tech = [t.name for t in project.technologies.all()]
        features = [
            line.strip() for line in (project.features or '').splitlines() if line.strip()
        ]
        projects_list.append({
            'id': project.id,
            'title': project.title,
            'desc': project.description,
            'category': categories,
            'tech': tech,
            'link': project.live_url or '#',
            'github': project.github_url,
            'features': features,
            'status': project.get_status_display(),
            'date': project.year or (project.created_at.year if project.created_at else ''),
            'rating': f"{project.rating:.1f}" if project.rating is not None else '',
        })

    # Categories for filter chips
    category_names = list(Category.objects.values_list('name', flat=True).order_by('name'))
    categories = ['all'] + category_names

    context = {
        'projects': projects_list,
        'categories': categories,
    }
    return render(request, 'portfolio/projects.html', context)

def contact(request):
    """Contact page view."""

    # Expose an empty form instance for potential server-side rendering
    form = ContactForm()
    return render(request, 'portfolio/contact.html', {"form": form})

def resume(request):
    """Resume page view (DB-driven)."""

    # Skills: use SkillCategory/Skill with section in resume/both but only expose names
    skills_context = {}
    for category in (
        SkillCategory.objects.filter(section__in=["resume", "both"])
        .prefetch_related("skills")
        .order_by("order")
    ):
        skills_context[category.name] = [
            sk.name for sk in category.skills.all().order_by("order")
        ]

    experience_list = []
    for exp in ExperienceEntry.objects.filter(
        section__in=["resume", "both"]
    ).order_by("order"):
        experience_list.append(
            {
                "role": exp.role,
                "company": exp.company,
                "period": exp.period,
                "description": exp.description,
            }
        )

    education_list = []
    for edu in EducationEntry.objects.filter(
        section__in=["resume", "both"]
    ).order_by("order"):
        education_list.append(
            {
                "degree": edu.degree,
                "institution": edu.institution,
                "year": edu.period,
                "grade": edu.grade,
            }
        )

    certifications = list(
        Certification.objects.filter(section__in=["resume", "both"])
        .order_by("order")
        .values_list("title", flat=True)
    )

    resume_projects = list(
        ResumeProjectHighlight.objects.all().order_by("order").values_list("text", flat=True)
    )

    context = {
        "profile": Profile.objects.first(),
        "skills": skills_context,
        "experience": experience_list,
        "education": education_list,
        "certifications": certifications,
        "projects": resume_projects,
    }
    return render(request, "portfolio/resume.html", context)

@csrf_protect
def contact_api(request):
    """JSON API endpoint for the contact form with validation and rate limiting."""

    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON payload"}, status=400)

    # Basic IP-based rate limiting (5 submissions per hour per IP)
    ip = request.META.get("REMOTE_ADDR", "unknown")
    cache_key = f"contact_rate:{ip}"
    try:
        count = cache.get(cache_key, 0)
        if count >= 5:
            return JsonResponse(
                {
                    "success": False,
                    "message": "You have reached the submission limit. Please try again later.",
                },
                status=429,
            )
        cache.incr(cache_key) if cache.get(cache_key) is not None else cache.set(cache_key, 1, 60 * 60)
    except Exception:
        # Never fail the request just because cache is unavailable
        pass

    form = ContactForm(data=data)
    if not form.is_valid():
        # Flatten errors into a simple string for the frontend
        error_messages = [
            f"{field}: {', '.join(messages)}" for field, messages in form.errors.items()
        ]
        return JsonResponse(
            {"success": False, "message": " ".join(error_messages)},
            status=400,
        )

    try:
        message_obj = form.save(request=request)

        email_message = (
            "New Contact Form Submission\n\n"
            f"Name: {message_obj.name}\n"
            f"Email: {message_obj.email}\n"
            f"Subject: {message_obj.subject}\n\n"
            f"Message:\n{message_obj.message}\n"
        )

        send_mail(
            subject=f"Portfolio Contact: {message_obj.subject}",
            message=email_message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@portfolio.com"),
            recipient_list=[
                getattr(settings, "CONTACT_TO_EMAIL", "malikabdulsattar9947@gmail.com"),
            ],
            fail_silently=False,
        )

        return JsonResponse(
            {
                "success": True,
                "message": "Message sent successfully! I will get back to you soon.",
            }
        )
    except Exception as exc:  # pragma: no cover - defensive
        return JsonResponse(
            {
                "success": False,
                "message": f"Error sending message. Please try again later.",
            },
            status=500,
        )

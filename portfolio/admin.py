from django.contrib import admin

from .models import (
    AboutStat,
    Achievement,
    BlogPost,
    Category,
    Certification,
    ContactMessage,
    EducationEntry,
    ExperienceEntry,
    PageView,
    Profile,
    Project,
    ProjectImage,
    ResumeProjectHighlight,
    SiteSettings,
    Skill,
    SkillCategory,
    Tag,
    Technology,
    Testimonial,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_editable = ("order",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "color", "featured_on_home", "order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_editable = ("featured_on_home", "order",)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "featured",
        "order",
        "created_at",
        "updated_at",
        "views",
    )
    list_filter = ("status", "featured", "categories", "technologies")
    search_fields = ("title", "description", "full_description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    list_editable = ("order", "featured")
    readonly_fields = ("views", "created_at", "updated_at")
    filter_horizontal = ("categories", "technologies")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at", "views")
    list_filter = ("status", "author", "categories", "tags")
    search_fields = ("title", "content", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories", "tags")
    readonly_fields = ("views", "created_at", "updated_at")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "read", "replied")
    list_filter = ("read", "replied", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "company", "rating", "featured", "order")
    list_filter = ("featured", "rating")
    search_fields = ("name", "role", "company", "content")
    list_editable = ("featured", "order")


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date", "order")
    list_filter = ("category", "date")
    search_fields = ("title", "description")
    list_editable = ("order",)


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("path", "session_key", "ip_address", "timestamp")
    list_filter = ("path", "timestamp")
    search_fields = ("path", "session_key", "ip_address", "user_agent", "referrer")
    readonly_fields = ("timestamp",)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "contact_email", "analytics_enabled", "maintenance_mode")
    
    def has_add_permission(self, request):
        # Only allow one SiteSettings instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of site settings
        return False
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("site_name", "site_description", "site_keywords"),
            "description": "General site information and SEO settings"
        }),
        ("Contact Information", {
            "fields": ("contact_email",),
            "description": "Primary contact email for the site"
        }),
        ("Social Media & Links", {
            "fields": ("github_url", "linkedin_url", "twitter_url", "kaggle_url", "whatsapp_url"),
            "description": "Social media profile URLs"
        }),
        ("Assets", {
            "fields": ("resume_file",),
            "description": "Downloadable files and documents"
        }),
        ("Site Options", {
            "fields": ("analytics_enabled", "maintenance_mode"),
            "description": "Site-wide feature toggles"
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "location")
    
    def has_add_permission(self, request):
        # Only allow one Profile instance
        return not Profile.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of profile
        return False
    
    fieldsets = (
        ("Personal Identity", {
            "fields": ("name", "title", "headline", "avatar"),
            "description": "Your name, professional title, and profile image"
        }),
        ("Contact Information", {
            "fields": ("email", "phone", "location"),
            "description": "How people can reach you"
        }),
        ("About Content", {
            "fields": ("current_position", "short_bio", "summary"),
            "description": "Professional summary and current status"
        }),
    )


@admin.register(AboutStat)
class AboutStatAdmin(admin.ModelAdmin):
    list_display = ("number", "label", "order")
    list_editable = ("order",)


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "order")
    list_filter = ("section",)
    list_editable = ("order",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "order")
    list_filter = ("category",)
    search_fields = ("name",)
    list_editable = ("order", "level")


@admin.register(EducationEntry)
class EducationEntryAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "period", "section", "order")
    list_filter = ("section",)
    list_editable = ("order",)


@admin.register(ExperienceEntry)
class ExperienceEntryAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "period", "section", "order")
    list_filter = ("section",)
    search_fields = ("role", "company")
    list_editable = ("order",)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "order")
    list_filter = ("section",)
    list_editable = ("order",)


@admin.register(ResumeProjectHighlight)
class ResumeProjectHighlightAdmin(admin.ModelAdmin):
    list_display = ("text", "order")
    list_editable = ("order",)

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class TimestampedModel(models.Model):
    """Abstract base with created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderedModel(models.Model):
    """Abstract base for simple manual ordering."""

    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ("order",)


class Category(OrderedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Categories"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Technology(OrderedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(
        max_length=20,
        blank=True,
        help_text="Tailwind or hex color class used in badges (e.g. text-indigo-400)",
    )
    featured_on_home = models.BooleanField(
        default=False,
        help_text="Display this tech on the home page hero tech stack"
    )

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class ProjectImage(OrderedModel):
    project = models.ForeignKey(
        "Project", related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="projects/")
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.caption or f"Image for {self.project.title}"


STATUS_CHOICES = (
    ("draft", "Draft"),
    ("in_progress", "In progress"),
    ("completed", "Completed"),
    ("production", "In production"),
)


class Project(TimestampedModel, OrderedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    full_description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name="projects", blank=True)
    technologies = models.ManyToManyField(Technology, related_name="projects", blank=True)
    featured_image = models.ImageField(upload_to="projects/", blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="completed")
    featured = models.BooleanField(default=False)
    year = models.CharField(max_length=10, blank=True, help_text="Display year, e.g. 2024")
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    features = models.TextField(blank=True, help_text="One feature per line")
    views = models.PositiveIntegerField(default=0)

    class Meta(OrderedModel.Meta):
        ordering = ("-featured", "order", "-created_at")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title

    def save(self, *args, **kwargs):  # pragma: no cover - trivial slug helper
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogPost(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    featured_image = models.ImageField(upload_to="blog/", blank=True)
    categories = models.ManyToManyField(Category, related_name="blog_posts", blank=True)
    tags = models.ManyToManyField(Tag, related_name="blog_posts", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(
        default=0, help_text="Estimated reading time in minutes"
    )

    class Meta:
        ordering = ("-published_at", "-created_at")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title

    @property
    def is_published(self) -> bool:
        return self.status in {"completed", "production"} and (
            self.published_at is None or self.published_at <= timezone.now()
        )


class ContactMessage(TimestampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Message from {self.name} <{self.email}>"


class Testimonial(TimestampedModel, OrderedModel):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    avatar = models.ImageField(upload_to="testimonials/", blank=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=5
    )
    featured = models.BooleanField(default=False)

    class Meta(OrderedModel.Meta):
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.name} - {self.role}"


class Achievement(OrderedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    date = models.DateField()
    category = models.CharField(max_length=100)

    class Meta(OrderedModel.Meta):
        ordering = ("-date", "order")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title


class PageView(models.Model):
    path = models.CharField(max_length=500)
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    referrer = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.path} @ {self.timestamp:%Y-%m-%d %H:%M}"


class Profile(TimestampedModel):
    """Primary profile for About/Resume/Home sections."""

    name = models.CharField(
        max_length=100,
        help_text="Your full name (e.g., Umer)"
    )
    title = models.CharField(
        max_length=150,
        help_text="Your professional title (e.g., Full Stack Developer)"
    )
    headline = models.CharField(
        max_length=255,
        help_text="One-line professional headline (shown on Home/About)",
    )
    location = models.CharField(
        max_length=150,
        blank=True,
        help_text="Your location (e.g., Lahore, Pakistan)"
    )
    email = models.EmailField(
        blank=True,
        help_text="Your contact email address"
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        help_text="Your phone number"
    )
    short_bio = models.TextField(
        blank=True,
        help_text="Brief bio about yourself"
    )
    current_position = models.CharField(
        max_length=200,
        blank=True,
        help_text="Text for home page status badge (e.g., 'Currently Working at RoyalSoft')"
    )
    summary = models.TextField(
        blank=True,
        help_text="Professional summary shown on About & Resume pages (supports paragraphs)"
    )
    avatar = models.ImageField(
        upload_to="profile/",
        blank=True,
        help_text="Profile image for navbar/home/footer"
    )

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name if self.name else "Profile"


class AboutStat(OrderedModel):
    number = models.CharField(max_length=20)
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.number} {self.label}"


SECTION_CHOICES = (
    ("about", "About"),
    ("resume", "Resume"),
    ("both", "Both"),
)


class SkillCategory(OrderedModel):
    name = models.CharField(max_length=150)
    section = models.CharField(max_length=10, choices=SECTION_CHOICES, default="about")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Skill(OrderedModel):
    category = models.ForeignKey(
        SkillCategory, related_name="skills", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150)
    level = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="0-100 proficiency (used for About skill bars)",
    )

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class EducationEntry(OrderedModel):
    section = models.CharField(max_length=10, choices=SECTION_CHOICES, default="both")
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    grade = models.CharField(max_length=100, blank=True)
    highlights = models.TextField(blank=True, help_text="One highlight per line")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.degree} @ {self.institution}"


class ExperienceEntry(OrderedModel):
    section = models.CharField(max_length=10, choices=SECTION_CHOICES, default="both")
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    achievements = models.TextField(
        blank=True,
        help_text="One achievement/bullet per line (used on About page)",
    )

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.role} @ {self.company}"


class Certification(OrderedModel):
    section = models.CharField(max_length=10, choices=SECTION_CHOICES, default="resume")
    title = models.CharField(max_length=255)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title


class ResumeProjectHighlight(OrderedModel):
    text = models.CharField(max_length=255)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.text


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    site_description = models.TextField(blank=True)
    site_keywords = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    kaggle_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True, help_text="Full WhatsApp link, e.g. https://wa.me/... with message")
    resume_file = models.FileField(upload_to="files/", blank=True)
    analytics_enabled = models.BooleanField(default=False)
    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.site_name

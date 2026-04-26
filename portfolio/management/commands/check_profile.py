from django.core.management.base import BaseCommand
from portfolio.models import Profile, SiteSettings


class Command(BaseCommand):
    help = 'Check and display current Profile and SiteSettings data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Profile Data ==='))
        
        profile = Profile.objects.first()
        if profile:
            self.stdout.write(f"Name: {profile.name}")
            self.stdout.write(f"Title: {profile.title}")
            self.stdout.write(f"Headline: {profile.headline}")
            self.stdout.write(f"Email: {profile.email}")
            self.stdout.write(f"Phone: {profile.phone}")
            self.stdout.write(f"Location: {profile.location}")
            self.stdout.write(f"Current Position: {profile.current_position}")
            self.stdout.write(f"Avatar: {profile.avatar}")
        else:
            self.stdout.write(self.style.WARNING("No Profile found. Please add one in Django admin."))
        
        self.stdout.write(self.style.SUCCESS('\n=== Site Settings ==='))
        
        settings = SiteSettings.objects.first()
        if settings:
            self.stdout.write(f"Site Name: {settings.site_name}")
            self.stdout.write(f"Contact Email: {settings.contact_email}")
            self.stdout.write(f"GitHub: {settings.github_url}")
            self.stdout.write(f"LinkedIn: {settings.linkedin_url}")
            self.stdout.write(f"Twitter: {settings.twitter_url}")
            self.stdout.write(f"Kaggle: {settings.kaggle_url}")
            self.stdout.write(f"WhatsApp: {settings.whatsapp_url}")
            self.stdout.write(f"Resume File: {settings.resume_file}")
        else:
            self.stdout.write(self.style.WARNING("No SiteSettings found. Please add one in Django admin."))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Check complete!\n'))

from django.core.management.base import BaseCommand
from portfolio.models import SkillCategory, Skill

SKILLS_DATA = [
    ("Data Science & Data Analysis", "both", [
        ("Python", 95), ("Pandas", 90), ("NumPy", 90),
        ("Data Cleaning", 88), ("Data Analysis", 92), ("Data Visualization", 88),
    ]),
    ("AI & ML Engineer", "both", [
        ("Machine Learning", 92), ("Supervised Learning", 90), ("Unsupervised Learning", 85),
        ("Model Evaluation", 88), ("Scikit-learn", 90),
    ]),
    ("Computer Vision & Deep Learning", "both", [
        ("CNN", 85), ("OpenCV", 82), ("Image Processing", 83),
        ("TensorFlow", 88), ("PyTorch", 85),
    ]),
    ("Generative AI", "both", [
        ("LLMs", 88), ("Prompt Engineering", 90), ("Chatbot Development", 87), ("AI Automation", 85),
    ]),
    ("Python Developer", "both", [
        ("Python", 95), ("OOP", 90), ("Scripting", 88),
        ("API Development", 85), ("Flask", 82),
    ]),
    ("Power BI", "both", [
        ("Power BI Dashboards", 85), ("Data Modeling", 82), ("DAX", 80), ("Reporting", 83),
    ]),
    ("EDA (Exploratory Data Analysis)", "both", [
        ("Data Exploration", 90), ("Statistical Analysis", 88), ("Data Visualization", 88),
    ]),
    ("Data Preprocessing", "both", [
        ("Data Cleaning", 90), ("Missing Value Handling", 88),
        ("Feature Engineering", 85), ("Data Transformation", 87),
    ]),
    ("Development & Deployment", "both", [
        ("API Integration", 85), ("Model Deployment", 83), ("End-to-End Project Development", 85),
    ]),
]

class Command(BaseCommand):
    help = 'Seed skills and skill categories'

    def handle(self, *args, **kwargs):
        for order, (cat_name, section, skills) in enumerate(SKILLS_DATA, start=1):
            category, _ = SkillCategory.objects.get_or_create(
                name=cat_name,
                defaults={"section": section, "order": order}
            )
            category.section = section
            category.order = order
            category.save()

            for skill_order, (skill_name, level) in enumerate(skills, start=1):
                skill, created = Skill.objects.get_or_create(
                    name=skill_name,
                    category=category,
                    defaults={"level": level, "order": skill_order}
                )
                if not created:
                    skill.level = level
                    skill.order = skill_order
                    skill.save()

            self.stdout.write(self.style.SUCCESS(f'✓ {cat_name} ({len(skills)} skills)'))

        self.stdout.write(self.style.SUCCESS('\nAll skills added successfully!'))

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from portfolio.models import (
    Profile,
    AboutStat,
    SkillCategory,
    Skill,
    EducationEntry,
    ExperienceEntry,
    Certification,
    ResumeProjectHighlight,
    SiteSettings,
    Technology,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Seed all portfolio data including profile, skills, education, experience, etc."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Profile...")
        self.seed_profile()
        
        self.stdout.write("Seeding Site Settings...")
        self.seed_site_settings()
        
        self.stdout.write("Seeding About Stats...")
        self.seed_about_stats()
        
        self.stdout.write("Seeding Skills...")
        self.seed_skills()
        
        self.stdout.write("Seeding Education...")
        self.seed_education()
        
        self.stdout.write("Seeding Experience...")
        self.seed_experience()
        
        self.stdout.write("Seeding Certifications...")
        self.seed_certifications()
        
        self.stdout.write("Seeding Resume Projects...")
        self.seed_resume_projects()
        
        self.stdout.write("Seeding Technologies...")
        self.seed_technologies()
        
        self.stdout.write(self.style.SUCCESS("All data seeded successfully!"))

    def seed_profile(self):
        Profile.objects.update_or_create(
            id=1,
            defaults={
                'name': 'Umer',
                'title': 'AI Engineer & ML Specialist',
                'headline': 'Passionate AI Engineer specializing in Machine Learning, Deep Learning, and NLP with production experience',
                'location': 'Pakistan',
                'email': 'umer@example.com',
                'phone': '+92 300 0000000',
                'short_bio': 'AI Engineer with expertise in building intelligent systems and deploying ML models to production.',
                'current_position': 'AI Engineer',
                'summary': '''I am an AI Engineer and Machine Learning Specialist with extensive experience in developing and deploying intelligent systems. My expertise spans across Deep Learning, Natural Language Processing, Computer Vision, and MLOps.

I have successfully deployed production-ready AI solutions and my technical skills include working with modern frameworks like TensorFlow, PyTorch, and Transformers, as well as building scalable APIs with FastAPI.

I am passionate about solving complex problems using AI and continuously learning new technologies to stay at the forefront of this rapidly evolving field.''',
            }
        )

    def seed_site_settings(self):
        SiteSettings.objects.update_or_create(
            id=1,
            defaults={
                'site_name': 'Umer Portfolio',
                'site_description': 'AI Engineer & ML Specialist - Portfolio showcasing projects in Machine Learning, Deep Learning, NLP, and Computer Vision',
                'site_keywords': 'AI Engineer, Machine Learning, Deep Learning, NLP, Computer Vision, Python, TensorFlow, PyTorch, Umer',
                'contact_email': 'umer@example.com',
                'github_url': 'https://github.com/umer',
                'linkedin_url': 'https://linkedin.com/in/umer',
                'twitter_url': 'https://twitter.com/umer',
                'kaggle_url': 'https://kaggle.com/umer',
                'whatsapp_url': 'https://wa.me/923000000000?text=Hi%20Umer%2C%20I%20would%20like%20to%20discuss%20a%20project',
                'analytics_enabled': True,
                'maintenance_mode': False,
            }
        )

    def seed_about_stats(self):
        stats = [
            {'number': '35+', 'label': 'Projects', 'description': 'Completed AI/ML Projects', 'order': 1},
            {'number': '2+', 'label': 'Years', 'description': 'Experience in AI/ML', 'order': 2},
            {'number': '10+', 'label': 'Technologies', 'description': 'Mastered Tech Stack', 'order': 3},
            {'number': '5+', 'label': 'Certifications', 'description': 'Professional Certifications', 'order': 4},
        ]
        
        for stat in stats:
            AboutStat.objects.update_or_create(
                order=stat['order'],
                defaults=stat
            )

    def seed_skills(self):
        skills_data = {
            'Programming Languages': [
                ('Python', 95),
                ('SQL', 85),
                ('JavaScript', 75),
                ('C++', 70),
            ],
            'AI/ML Frameworks': [
                ('TensorFlow', 90),
                ('PyTorch', 88),
                ('Scikit-learn', 92),
                ('Keras', 85),
                ('Hugging Face Transformers', 87),
            ],
            'Deep Learning': [
                ('CNNs', 90),
                ('RNNs/LSTMs', 85),
                ('Transformers', 88),
                ('GANs', 75),
                ('Transfer Learning', 90),
            ],
            'NLP & GenAI': [
                ('BERT', 88),
                ('GPT', 85),
                ('Text Classification', 90),
                ('Sentiment Analysis', 92),
                ('Machine Translation', 80),
            ],
            'Computer Vision': [
                ('OpenCV', 88),
                ('Image Classification', 90),
                ('Object Detection (YOLO)', 85),
                ('Image Segmentation', 80),
            ],
            'MLOps & Tools': [
                ('Docker', 85),
                ('Git', 90),
                ('MLflow', 80),
                ('FastAPI', 88),
                ('Streamlit', 92),
            ],
            'Data Science': [
                ('Pandas', 95),
                ('NumPy', 95),
                ('Matplotlib', 90),
                ('Seaborn', 88),
                ('Statistical Analysis', 85),
            ],
            'Databases': [
                ('PostgreSQL', 80),
                ('MySQL', 82),
                ('SQLite', 85),
                ('MongoDB', 75),
            ],
        }
        
        for order, (category_name, skills) in enumerate(skills_data.items(), start=1):
            category, _ = SkillCategory.objects.update_or_create(
                name=category_name,
                defaults={'section': 'both', 'order': order}
            )
            
            for skill_order, (skill_name, level) in enumerate(skills, start=1):
                Skill.objects.update_or_create(
                    category=category,
                    name=skill_name,
                    defaults={'level': level, 'order': skill_order}
                )

    def seed_education(self):
        education_data = [
            {
                'degree': 'Bachelor of Science in Computer Science',
                'institution': 'University of Engineering and Technology, Lahore',
                'period': '2020 - 2024',
                'grade': 'CGPA: 3.5/4.0',
                'highlights': '''Machine Learning Specialization
Deep Learning and Neural Networks
Data Structures and Algorithms
Database Management Systems''',
                'section': 'both',
                'order': 1,
            },
            {
                'degree': 'Intermediate in Computer Science',
                'institution': 'Punjab College, Lahore',
                'period': '2018 - 2020',
                'grade': 'Marks: 85%',
                'highlights': '''Computer Science Fundamentals
Mathematics and Statistics
Physics and Chemistry''',
                'section': 'both',
                'order': 2,
            },
        ]
        
        for edu in education_data:
            EducationEntry.objects.update_or_create(
                degree=edu['degree'],
                defaults=edu
            )

    def seed_experience(self):
        experience_data = [
            {
                'company': 'RoyalSoft',
                'role': 'AI Engineer',
                'period': '2024 - Present',
                'employment_type': 'Full-time',
                'description': 'Developing and deploying AI-powered solutions for enterprise clients, including chatbots and data analytics systems.',
                'achievements': '''Deployed bilingual AI chatbot for ERP system with 95% accuracy
Built real-time data visualization dashboard using FastAPI
Implemented safe SQL query execution with natural language processing
Reduced customer support response time by 60%''',
                'section': 'both',
                'order': 1,
            },
            {
                'company': 'Freelance',
                'role': 'Machine Learning Engineer',
                'period': '2023 - 2024',
                'employment_type': 'Freelance',
                'description': 'Worked on various ML projects including computer vision, NLP, and predictive analytics for clients worldwide.',
                'achievements': '''Completed 15+ ML projects with 100% client satisfaction
Developed custom image classification models with 92% accuracy
Built sentiment analysis systems for social media monitoring
Created automated data pipelines for ETL processes''',
                'section': 'both',
                'order': 2,
            },
            {
                'company': 'Tech Startup',
                'role': 'Data Science Intern',
                'period': '2022 - 2023',
                'employment_type': 'Internship',
                'description': 'Assisted in data analysis, model development, and deployment of ML solutions.',
                'achievements': '''Analyzed large datasets using Pandas and NumPy
Built predictive models for customer churn
Created interactive dashboards with Streamlit
Collaborated with cross-functional teams''',
                'section': 'both',
                'order': 3,
            },
        ]
        
        for exp in experience_data:
            ExperienceEntry.objects.update_or_create(
                company=exp['company'],
                role=exp['role'],
                defaults=exp
            )

    def seed_certifications(self):
        certifications = [
            'Machine Learning Specialization - Stanford University (Coursera)',
            'Deep Learning Specialization - deeplearning.ai',
            'TensorFlow Developer Certificate - Google',
            'Natural Language Processing Specialization - deeplearning.ai',
            'MLOps Specialization - deeplearning.ai',
            'Python for Data Science - IBM',
        ]
        
        for order, cert in enumerate(certifications, start=1):
            Certification.objects.update_or_create(
                title=cert,
                defaults={'section': 'both', 'order': order}
            )

    def seed_resume_projects(self):
        projects = [
            'AI-Powered ERP Chatbot - Bilingual chatbot with SQL execution and data visualization',
            'Image Classification System - 92% accuracy using transfer learning with ResNet50',
            'Real-time Object Detection - YOLOv5-based system processing 30+ FPS',
            'Neural Machine Translator - Multilingual translation supporting 10+ languages',
            'House Price Prediction - Ensemble model with R² score of 0.89',
            'Medical Diagnosis Assistant - Multi-class classification for disease prediction',
        ]
        
        for order, project in enumerate(projects, start=1):
            ResumeProjectHighlight.objects.update_or_create(
                text=project,
                defaults={'order': order}
            )

    def seed_technologies(self):
        from django.utils.text import slugify
        
        featured_tech = [
            {'name': 'Python', 'icon': 'code', 'color': 'text-blue-400', 'featured': True, 'order': 1},
            {'name': 'TensorFlow', 'icon': 'cpu', 'color': 'text-orange-400', 'featured': True, 'order': 2},
            {'name': 'PyTorch', 'icon': 'zap', 'color': 'text-red-400', 'featured': True, 'order': 3},
            {'name': 'Scikit-learn', 'icon': 'bar-chart', 'color': 'text-green-400', 'featured': True, 'order': 4},
            {'name': 'FastAPI', 'icon': 'server', 'color': 'text-teal-400', 'featured': True, 'order': 5},
            {'name': 'Docker', 'icon': 'package', 'color': 'text-blue-500', 'featured': True, 'order': 6},
        ]
        
        for tech in featured_tech:
            slug = slugify(tech['name'])
            Technology.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': tech['name'],
                    'icon': tech['icon'],
                    'color': tech['color'],
                    'featured_on_home': tech['featured'],
                    'order': tech['order'],
                }
            )

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from portfolio.models import Category, Project, Technology


PROJECTS_DATA = [
    # Featured project - Production
    {
        'title': 'AI-Powered ERP Chatbot',
        'desc': 'Enterprise chatbot deployed at RoyalSoft providing bilingual (English/Urdu) support for ERP systems. Executes safe SQL queries, delivers intelligent business insights, and generates real-time data visualizations for end-users.',
        'categories': ['GenAI', 'NLP', 'Production'],
        'tech': ['Python', 'LLMs', 'SQL', 'FastAPI', 'Transformers'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Bilingual NLP', 'Safe SQL Execution', 'Real-time Analytics', 'Data Visualization'],
        'status': 'production',
        'year': '2025',
        'rating': '5.0',
    },
    # Phase 10: MLOps & Production
    {
        'title': 'ML Model API Service',
        'desc': 'Production-ready REST API for serving machine learning models with FastAPI, including model versioning and monitoring.',
        'categories': ['MLOps', 'Production'],
        'tech': ['FastAPI', 'Docker', 'Python', 'MLflow'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['REST API', 'Model Versioning', 'Monitoring', 'Docker Deployment'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.8',
    },
    {
        'title': 'Automated ML Pipeline',
        'desc': 'CI/CD pipeline for automated model training, testing, and deployment with experiment tracking and version control.',
        'categories': ['MLOps', 'Automation'],
        'tech': ['Python', 'Docker', 'Git', 'MLflow', 'DVC'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['CI/CD', 'Experiment Tracking', 'Auto Deployment', 'Version Control'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.7',
    },
    # Phase 9: NLP & Generative AI
    {
        'title': 'AI Content Generator',
        'desc': 'Advanced text generation system leveraging GPT-based transformers for automated content creation. Generates articles, summaries, and creative writing with customizable style and tone control.',
        'categories': ['GenAI', 'NLP'],
        'tech': ['Python', 'Transformers', 'GPT', 'PyTorch', 'Hugging Face'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Text Generation', 'Style Control', 'Auto Summarization', 'Multi-format Output'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.9',
    },
    {
        'title': 'Neural Machine Translator',
        'desc': 'Multilingual translation system built with transformer architecture supporting 10+ languages. Implements attention mechanisms for context-aware translations with 85%+ accuracy on standard benchmarks.',
        'categories': ['NLP', 'Deep Learning'],
        'tech': ['Python', 'Transformers', 'BERT', 'TensorFlow', 'Attention'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['10+ Languages', 'Attention Mechanism', '85%+ Accuracy', 'Real-time Translation'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.8',
    },
    {
        'title': 'Sentiment Analysis with Transformers',
        'desc': 'Advanced sentiment analysis using BERT and RoBERTa for analyzing customer reviews, social media, and feedback.',
        'categories': ['NLP', 'AI/ML'],
        'tech': ['Python', 'BERT', 'Transformers', 'PyTorch'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['BERT Model', 'Multi-class Classification', 'Fine-tuning', 'High Accuracy'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.7',
    },
    # Phase 8: Deep Learning & Neural Networks
    {
        'title': 'Image Classification System',
        'desc': 'Deep CNN model achieving 92% accuracy on image classification using transfer learning with ResNet50 and VGG16. Implements data augmentation and fine-tuning for optimal performance on custom datasets.',
        'categories': ['Deep Learning', 'Computer Vision'],
        'tech': ['Python', 'TensorFlow', 'Keras', 'ResNet', 'VGG'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Transfer Learning', 'Data Augmentation', '92% Accuracy', 'Multi-class Support'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.8',
    },
    {
        'title': 'Real-time Object Detection',
        'desc': 'YOLOv5-based object detection system processing video streams at 30+ FPS. Detects and localizes 80+ object classes with bounding boxes and confidence scores for real-time applications.',
        'categories': ['Computer Vision', 'Deep Learning'],
        'tech': ['Python', 'YOLOv5', 'OpenCV', 'PyTorch'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['30+ FPS', '80+ Object Classes', 'Bounding Boxes', 'Video Processing'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.9',
    },
    {
        'title': 'RNN for Time Series Prediction',
        'desc': 'Recurrent neural network with LSTM for predicting stock prices, weather patterns, and sequential data.',
        'categories': ['Deep Learning', 'Time Series'],
        'tech': ['Python', 'LSTM', 'TensorFlow', 'Pandas'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['LSTM Architecture', 'Sequence Prediction', 'Time Series Analysis', 'Forecasting'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.7',
    },
    # Phase 7: Unsupervised Learning
    {
        'title': 'Customer Segmentation with K-Means',
        'desc': 'Clustering analysis for customer segmentation using K-Means, DBSCAN, and hierarchical clustering algorithms.',
        'categories': ['AI/ML', 'Unsupervised'],
        'tech': ['Python', 'Scikit-learn', 'Pandas', 'Matplotlib'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['K-Means Clustering', 'DBSCAN', 'Visualization', 'Business Insights'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.6',
    },
    {
        'title': 'Anomaly Detection System',
        'desc': 'Detect outliers and anomalies in network traffic, financial transactions, and system logs using isolation forest.',
        'categories': ['AI/ML', 'Security'],
        'tech': ['Python', 'Scikit-learn', 'Isolation Forest', 'PCA'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Outlier Detection', 'Real-time Monitoring', 'Visualization', 'Alert System'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.7',
    },
    {
        'title': 'Dimensionality Reduction with PCA',
        'desc': 'Reduce high-dimensional data using PCA, t-SNE, and UMAP for visualization and feature extraction.',
        'categories': ['Data Science', 'Unsupervised'],
        'tech': ['Python', 'Scikit-learn', 'PCA', 't-SNE', 'UMAP'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['PCA', 't-SNE', 'UMAP', '3D Visualization'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.5',
    },
    # Phase 6: Supervised Learning
    {
        'title': 'House Price Prediction',
        'desc': 'Ensemble regression model achieving R² score of 0.89 for house price prediction. Combines Linear Regression, Random Forest, and XGBoost with advanced feature engineering and hyperparameter tuning.',
        'categories': ['AI/ML', 'Regression'],
        'tech': ['Python', 'Scikit-learn', 'XGBoost', 'Pandas'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Ensemble Methods', 'Feature Engineering', 'R² = 0.89', 'Hyperparameter Tuning'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.8',
    },
    {
        'title': 'Medical Diagnosis Assistant',
        'desc': 'Multi-class classification for disease prediction using ensemble methods and feature importance analysis.',
        'categories': ['AI/ML', 'Healthcare'],
        'tech': ['Python', 'Scikit-learn', 'Random Forest', 'XGBoost'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Ensemble Methods', 'Feature Importance', 'High Accuracy', 'Medical Insights'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.9',
    },
    {
        'title': 'Credit Risk Assessment',
        'desc': 'Binary classification for credit risk prediction handling imbalanced data with SMOTE and ensemble techniques.',
        'categories': ['AI/ML', 'Finance'],
        'tech': ['Python', 'Scikit-learn', 'SMOTE', 'LightGBM'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Imbalanced Data Handling', 'SMOTE', 'Ensemble Methods', 'Risk Scoring'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.7',
    },
    {
        'title': 'Spam Email Classifier',
        'desc': 'Text classification using Naive Bayes, SVM, and ensemble methods for detecting spam emails with high accuracy.',
        'categories': ['NLP', 'AI/ML'],
        'tech': ['Python', 'Scikit-learn', 'NLP', 'TF-IDF'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Text Classification', 'Multiple Algorithms', 'High Precision', 'Real-time Detection'],
        'status': 'completed',
        'year': '2024',
        'rating': '4.6',
    },
    # Phase 5: ML Fundamentals
    {
        'title': 'Iris Flower Classification',
        'desc': 'Multi-class classification project demonstrating ML fundamentals with cross-validation and evaluation metrics.',
        'categories': ['AI/ML', 'Classification'],
        'tech': ['Python', 'Scikit-learn', 'Pandas', 'Matplotlib'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Multi-class Classification', 'Cross-validation', 'Metrics Analysis', 'Visualization'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.5',
    },
    {
        'title': 'Customer Churn Prediction',
        'desc': 'Binary classification with feature engineering and model comparison for predicting customer churn.',
        'categories': ['AI/ML', 'Business'],
        'tech': ['Python', 'Scikit-learn', 'Pandas', 'Seaborn'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Feature Engineering', 'Model Comparison', 'Business Insights', 'Churn Analysis'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.6',
    },
    {
        'title': 'Sales Forecasting System',
        'desc': 'Time-aware ML model for predicting future sales with business impact analysis and seasonal patterns.',
        'categories': ['AI/ML', 'Time Series'],
        'tech': ['Python', 'Scikit-learn', 'Prophet', 'Pandas'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Time Series', 'Forecasting', 'Seasonal Patterns', 'Business Metrics'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.7',
    },
    # Phase 4: Statistics & Mathematics
    {
        'title': 'A/B Testing Framework',
        'desc': 'Statistical framework for designing and analyzing A/B tests with hypothesis testing and confidence intervals.',
        'categories': ['Data Science', 'Statistics'],
        'tech': ['Python', 'SciPy', 'Pandas', 'Matplotlib'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Hypothesis Testing', 'Statistical Analysis', 'Confidence Intervals', 'P-value Calculation'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.5',
    },
    {
        'title': 'Survey Data Analysis',
        'desc': 'Comprehensive statistical analysis of survey data with descriptive statistics and hypothesis testing.',
        'categories': ['Data Science', 'Statistics'],
        'tech': ['Python', 'Pandas', 'SciPy', 'Seaborn'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Descriptive Statistics', 'Hypothesis Testing', 'Correlation Analysis', 'Visualization'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.4',
    },
    {
        'title': 'Market Research Analytics',
        'desc': 'Statistical inference and correlation analysis for market research with business recommendations.',
        'categories': ['Data Science', 'Business'],
        'tech': ['Python', 'Pandas', 'NumPy', 'Matplotlib'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Correlation Analysis', 'Statistical Inference', 'Market Insights', 'Recommendations'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.6',
    },
    # Phase 3: Data Science Libraries
    {
        'title': 'Stock Market Data Analyzer',
        'desc': 'Analyze historical stock data using NumPy and Pandas with technical indicators and trend analysis.',
        'categories': ['Data Science', 'Finance'],
        'tech': ['Python', 'NumPy', 'Pandas', 'Matplotlib'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Technical Indicators', 'Trend Analysis', 'Data Visualization', 'Financial Metrics'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.7',
    },
    {
        'title': 'Sales Dashboard',
        'desc': 'Interactive sales dashboard with comprehensive visualizations using Matplotlib and Seaborn.',
        'categories': ['Data Science', 'Visualization'],
        'tech': ['Python', 'Matplotlib', 'Seaborn', 'Pandas'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Interactive Plots', 'Multiple Chart Types', 'Business Insights', 'KPI Tracking'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.6',
    },
    {
        'title': 'Weather Data Explorer',
        'desc': 'Process and visualize weather patterns from CSV files with statistical analysis and forecasting.',
        'categories': ['Data Science', 'Analysis'],
        'tech': ['Python', 'Pandas', 'Matplotlib', 'Seaborn'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Data Processing', 'Pattern Analysis', 'Visualization', 'Weather Forecasting'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.5',
    },
    {
        'title': 'E-commerce Analytics',
        'desc': 'Analyze customer behavior using Pandas groupby, aggregations, and advanced data manipulation.',
        'categories': ['Data Science', 'E-commerce'],
        'tech': ['Python', 'Pandas', 'NumPy', 'Seaborn'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Customer Behavior', 'Sales Analysis', 'Cohort Analysis', 'RFM Segmentation'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.7',
    },
    # Phase 2: Advanced Programming
    {
        'title': 'ATM Management System',
        'desc': 'Full-featured ATM simulation with PIN management, transactions, and real-time balance tracking. Streamlit-based interface with transaction history, export functionality, and comprehensive validation.',
        'categories': ['Python', 'OOP'],
        'tech': ['Python', 'OOP', 'File Handling', 'Streamlit'],
        'live_url': 'https://atmmanagementsystemoop-txryky3ccw6ek8qri3pz2b.streamlit.app/',
        'github_url': 'https://github.com/umer',
        'features': [
            'Full ATM functionalities with PIN setup/change, deposit, withdrawal, and balance inquiry',
            'Streamlit web interface with transaction history and export options',
            'Input validation, session management, and visual feedback',
            'Real-time balance updates and professional error handling',
        ],
        'status': 'production',
        'year': '2024',
        'rating': '5.0',
    },
    {
        'title': 'Library Management System',
        'desc': 'Complete OOP project with classes, inheritance, file handling, and database integration.',
        'categories': ['Python', 'OOP'],
        'tech': ['Python', 'OOP', 'SQLite', 'File Handling', 'Streamlit'],
        'live_url': 'https://oop-library-system-management.streamlit.app/',
        'github_url': 'https://github.com/umer',
        'features': ['OOP Design', 'Database Integration', 'File Handling', 'User Management'],
        'status': 'production',
        'year': '2024',
        'rating': '5.0',
    },
    {
        'title': 'Custom Data Structure Library',
        'desc': 'Implementation of stacks, queues, linked lists, and trees from scratch in Python.',
        'categories': ['Python', 'Algorithms'],
        'tech': ['Python', 'Data Structures', 'Algorithms'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Stack', 'Queue', 'Linked List', 'Binary Tree'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.4',
    },
    {
        'title': 'Automated File Organizer',
        'desc': 'Use modules, decorators, and generators to automatically organize files by type and date.',
        'categories': ['Python', 'Automation'],
        'tech': ['Python', 'OS Module', 'Decorators', 'Generators'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['File Organization', 'Automation', 'Decorators', 'Generators'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.5',
    },
    # Phase 1: Programming Foundation
    {
        'title': 'Personal Finance Calculator',
        'desc': 'Calculator using functions, loops, and conditionals for budget tracking and expense management.',
        'categories': ['Python', 'Basics'],
        'tech': ['Python', 'Functions', 'Loops', 'Conditionals'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Budget Tracking', 'Expense Management', 'Reports', 'Savings Calculator'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.3',
    },
    {
        'title': 'Text Analysis Tool',
        'desc': 'Analyze text files using string methods, file handling, and basic NLP techniques.',
        'categories': ['Python', 'Text Processing'],
        'tech': ['Python', 'String Methods', 'File Handling'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Word Count', 'Frequency Analysis', 'Text Statistics', 'File Processing'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.4',
    },
    {
        'title': 'Student Grade Management',
        'desc': 'Grade management system using lists, dictionaries, and basic OOP concepts.',
        'categories': ['Python', 'Education'],
        'tech': ['Python', 'Lists', 'Dictionaries', 'OOP'],
        'live_url': 'https://school-management-system-oop-python.streamlit.app/',
        'github_url': 'https://github.com/umer',
        'features': ['Grade Tracking', 'Student Records', 'GPA Calculation', 'Reports'],
        'status': 'production',
        'year': '2024',
        'rating': '5.0',
    },
    {
        'title': 'Data Structure Visualizer',
        'desc': 'Interactive demonstrations of lists, sets, tuples, and dictionary operations.',
        'categories': ['Python', 'Education'],
        'tech': ['Python', 'Data Structures', 'Visualization'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['Interactive Demo', 'Visual Learning', 'Multiple Data Structures', 'Operations'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.3',
    },
    {
        'title': 'Tic-Tac-Toe Game',
        'desc': 'Classic game combining all basic Python concepts including functions, loops, and conditionals.',
        'categories': ['Python', 'Game'],
        'tech': ['Python', 'Game Logic', 'Functions'],
        'live_url': '#',
        'github_url': 'https://github.com/umer',
        'features': ['2-Player Mode', 'Score Tracking', 'Game Logic'],
        'status': 'completed',
        'year': '2023',
        'rating': '4.4',
    },
]


STATUS_MAP = {
    'Production': 'production',
    'Deployed': 'production',
    'Completed': 'completed',
    'In Progress': 'in_progress',
}


class Command(BaseCommand):
    help = "Seed the database with portfolio projects, categories and technologies."

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for index, data in enumerate(PROJECTS_DATA, start=1):
            title = data['title']
            slug = slugify(title)

            categories = []
            for cat_name in data.get('categories', []):
                cat_slug = slugify(cat_name)
                category, _ = Category.objects.get_or_create(
                    slug=cat_slug,
                    defaults={'name': cat_name},
                )
                categories.append(category)

            technologies = []
            for tech_name in data.get('tech', []):
                tech_slug = slugify(tech_name)
                tech, _ = Technology.objects.get_or_create(
                    slug=tech_slug,
                    defaults={'name': tech_name},
                )
                technologies.append(tech)

            status_raw = data.get('status', 'Completed')
            status = STATUS_MAP.get(status_raw, status_raw.lower())

            rating_raw = data.get('rating')
            try:
                rating = float(rating_raw) if rating_raw is not None else None
            except (TypeError, ValueError):
                rating = None

            features_list = data.get('features') or []
            if isinstance(features_list, (list, tuple)):
                features_text = "\n".join(features_list)
            else:
                features_text = str(features_list)

            project, created = Project.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': data.get('desc', ''),
                    'full_description': data.get('desc', ''),
                    'github_url': data.get('github_url', ''),
                    'live_url': data.get('live_url', ''),
                    'status': status,
                    'featured': index == 1,  # First project is the main featured one
                    'year': data.get('year', ''),
                    'rating': rating,
                    'features': features_text,
                    'order': index,
                },
            )

            project.categories.set(categories)
            project.technologies.set(technologies)

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded projects successfully (created={created_count}, updated={updated_count})."
        ))

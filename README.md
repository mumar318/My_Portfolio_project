# Muhammad Umar - Portfolio Website

A modern, responsive Django-based portfolio website showcasing my projects, skills, and professional experience.

## Features

- **Responsive Design**: Works perfectly on all devices
- **Admin Panel**: Easy content management through Django admin
- **Project Showcase**: Display your projects with images, descriptions, and links
- **Contact Form**: Visitors can reach out directly through the website
- **Blog System**: Share your thoughts and experiences
- **Resume Section**: Professional experience and education display
- **Analytics**: Track page views and visitor engagement

## Tech Stack

- **Backend**: Django 4.1.13
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with responsive design
- **Deployment**: Ready for Heroku/Railway deployment

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/mumar318/My_protofolio.git
   cd My_protofolio
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Configuration

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

## Deployment

This project is ready for deployment on platforms like Heroku, Railway, or any Django-compatible hosting service.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

- **Name**: Muhammad Umar
- **GitHub**: [@mumar318](https://github.com/mumar318)
- **Portfolio**: [Live Demo](https://your-portfolio-url.com)
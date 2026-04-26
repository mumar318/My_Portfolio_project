# Deployment Guide - Render

## 📋 Pre-Deployment Checklist

Your project is now configured for Render deployment with:
- ✅ Gunicorn (production server)
- ✅ WhiteNoise (static files)
- ✅ PostgreSQL support (dj-database-url)
- ✅ Environment-based configuration
- ✅ Procfile for Render
- ✅ Build script

## 🚀 Deploy to Render

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Create PostgreSQL Database
1. In Render Dashboard → Click **New +** → **PostgreSQL**
2. Name: `portfolio-db` (or your choice)
3. Database: `portfolio` (auto-generated)
4. User: `portfolio` (auto-generated)
5. Region: Choose closest to you
6. Plan: **Free**
7. Click **Create Database**
8. Once created, copy the **External Database URL** (starts with `postgres://`)

### Step 4: Create Web Service
1. In Render Dashboard → Click **New +** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `your-portfolio` (becomes your-portfolio.onrender.com)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: (leave blank)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn portfolio_django.wsgi:application`

### Step 5: Add Environment Variables
In your Web Service → **Environment** → Add these variables:

```
DATABASE_URL = <paste your PostgreSQL External URL here>
DJANGO_SECRET_KEY = <generate a long random string>
DJANGO_DEBUG = False
DJANGO_ALLOWED_HOSTS = your-portfolio.onrender.com
```

**Generate SECRET_KEY** (run locally):
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Click **Save Changes** → Render will deploy automatically

### Step 6: Create Superuser
Once deployment succeeds:
1. Go to your Web Service → **Shell** tab
2. Run:
```bash
python manage.py createsuperuser
```
3. Enter username, email, and password

### Step 7: Access Your Site
- **Live Site**: `https://your-portfolio.onrender.com/`
- **Admin Panel**: `https://your-portfolio.onrender.com/admin/`

Log in with the superuser credentials you just created.

## 🔧 Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| DisallowedHost error | Add your domain to `DJANGO_ALLOWED_HOSTS` env var |
| 500 error | Check logs in Render dashboard, ensure migrations ran |
| Static files missing | Verify `collectstatic` ran in build command |
| Can't login to admin | Create superuser via Shell on Render |
| Database connection error | Verify `DATABASE_URL` is set correctly |

## 📝 Important Notes

### Media Files
- Render's free tier has **ephemeral storage** - uploaded files may be lost on redeploy
- For production, consider using AWS S3 or Cloudinary for media storage
- Current setup works fine for initial deployment and testing

### Security (Production)
Add these to `settings.py` once stable:
```python
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
```

### Free Tier Limitations
- Service spins down after 15 min of inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month free (enough for one service)

## 🔄 Updating Your Site

After making changes locally:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render auto-deploys on every push to main branch.

## 📊 Monitoring
- View logs: Web Service → **Logs** tab
- Check metrics: Web Service → **Metrics** tab
- Database status: PostgreSQL → **Info** tab

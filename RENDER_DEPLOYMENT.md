# Render Deployment Guide

This guide walks you through deploying the Backend E-Commerce application to Render.

## Prerequisites

- GitHub account with the repository pushed
- Render account (https://render.com)
- PostgreSQL database (Render provides free tier)

## Pre-Deployment Checklist

✅ **Configuration Files**
- [x] `config.py` - Updated to use environment variables
- [x] `requirements.txt` - Includes gunicorn and psycopg2-binary
- [x] `Procfile` - Configured for gunicorn
- [x] `runtime.txt` - Python version specified
- [x] `.env.example` - Updated with production variables

✅ **Database**
- [x] Uses SQLAlchemy ORM (compatible with PostgreSQL)
- [x] Alembic migrations configured
- [x] Database URL supports PostgreSQL format

✅ **Static Files**
- [x] Static files in `/static` directory
- [x] Upload folder configured

✅ **Environment Variables**
- [x] SECRET_KEY configured via env vars
- [x] DATABASE_URL configurable
- [x] PORT configurable

## Step 1: Prepare Your Repository

1. Ensure all files are committed to GitHub:
   ```bash
   git status
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

## Step 2: Create PostgreSQL Database on Render

1. Log in to [Render.com](https://render.com)
2. Click "New" → "PostgreSQL"
3. Fill in the details:
   - **Name**: `ecommerce-db` (or your choice)
   - **Database**: `ecommerce_db`
   - **User**: `ecommerce_user`
   - **Region**: Select closest to your users
4. Click "Create Database"
5. **IMPORTANT**: Copy and save the **Internal Database URL** (looks like: `postgresql://user:password@...`)

## Step 3: Create Web Service on Render

1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Select the repository
4. Fill in the deployment details:
   - **Name**: `ecommerce-backend` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Region**: Same as database (recommended)
   - **Plan**: Free (or paid tier as needed)

5. Click "Advanced" and add Environment Variables:

## Step 4: Configure Environment Variables

In the Render dashboard for your Web Service, add these environment variables:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Generate a secure random string (e.g., `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DATABASE_URL` | Paste the Internal Database URL from Step 2 |
| `FLASK_ENV` | `production` |
| `PORT` | `10000` (Render's default) |

## Step 5: Deploy

1. Click "Create Web Service"
2. Render will automatically start building and deploying
3. Monitor the deployment in the "Logs" tab
4. Once deployed, you'll get a URL like: `https://ecommerce-backend.onrender.com`

## Step 6: Initialize Database

After first deployment:

1. In Render dashboard, click "Shell" tab
2. Run migration commands:
   ```bash
   flask db upgrade
   ```

3. (Optional) Create an admin user:
   ```bash
   python create_admin.py
   ```

## Step 7: Post-Deployment Verification

✅ Check your application at `https://your-app-name.onrender.com`
✅ Verify admin login works
✅ Test product creation/management
✅ Verify database connections work
✅ Check logs for any errors

## Environment Variables Reference

```env
# Required
SECRET_KEY=<strong-random-string>
DATABASE_URL=<postgresql-url-from-render>

# Optional (defaults provided)
FLASK_ENV=production
PORT=10000
```

## Troubleshooting

### Application won't start
- Check logs in Render dashboard
- Verify `DATABASE_URL` is correct
- Check that `SECRET_KEY` is set
- Ensure `requirements.txt` has all dependencies

### Database connection error
- Verify `DATABASE_URL` environment variable
- Check PostgreSQL database is running (green status in Render)
- Confirm database user has correct permissions
- Try restarting the Web Service

### Static files not loading
- Ensure Flask is configured to serve static files
- Check `UPLOAD_FOLDER` exists: `os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)`
- Verify permissions on static directory

### Internal Server Error (500)
- Check application logs in Render
- Verify database migrations ran successfully
- Check environment variables are properly set
- Look for import errors or configuration issues

### Port already in use
- Render auto-assigns ports; shouldn't be an issue
- If testing locally, use: `export PORT=5000 && gunicorn app:app`

## Useful Render Commands

### Access Application Shell
1. Go to your Web Service in Render
2. Click "Shell" tab
3. Run commands directly (e.g., `python create_admin.py`)

### View Logs
1. Click "Logs" tab to see real-time logs
2. Scroll to see deployment and runtime logs

### Restart Service
1. Click "Environment" → "Redeploy latest commit"
2. Or manually click "Restart" button

## Database Backups

Render automatically backs up PostgreSQL databases. To manually backup:
1. In PostgreSQL dashboard, click "Backups"
2. Click "Create Backup"

## Performance Tips

1. Set up caching for static assets
2. Use database connection pooling
3. Monitor resources in Render dashboard
4. Upgrade plan if needed for better performance
5. Consider using a CDN for static files

## Security Best Practices

✅ **IMPORTANT**: Before deployment:
1. Generate a new SECRET_KEY (don't use the placeholder)
2. Use strong database credentials
3. Enable HTTPS (Render does this automatically)
4. Regularly update dependencies
5. Monitor logs for suspicious activity
6. Set up error tracking (optional: integrate with Sentry)

## Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Configure email notifications
3. Set up monitoring/alerting
4. Plan backup strategy
5. Document your deployment process

## Support

For Render-specific issues:
- Render Docs: https://render.com/docs
- Render Support: https://support.render.com

For application issues:
- Check application logs
- Review code for errors
- Test locally first before pushing

## Useful Links

- Render Dashboard: https://dashboard.render.com
- Render Python Deployment: https://render.com/docs/deploy-python
- Flask Documentation: https://flask.palletsprojects.com
- SQLAlchemy Documentation: https://docs.sqlalchemy.org

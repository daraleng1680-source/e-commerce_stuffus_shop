# Complete Render Deployment Setup Guide

This guide will walk you through deploying the E-Commerce Backend to Render step-by-step.

## Prerequisites

- GitHub account with repository pushed
- Render account (https://render.com)
- A credit card (for free tier resources)

## Step 1: Create PostgreSQL Database on Render

### 1.1 Access Render Dashboard
1. Go to https://render.com/dashboard
2. Log in with your Render account
3. Click the **"New +"** button in the top-right corner
4. Select **"PostgreSQL"**

### 1.2 Configure Database
Fill in the following details:

| Field | Value |
|-------|-------|
| **Name** | `ecommerce-db` |
| **Database** | `ecommerce_db` |
| **User** | `ecommerce_user` |
| **Region** | Select closest to your users (e.g., Ohio, Frankfurt) |
| **PostgreSQL Version** | Keep default (latest) |
| **Plan** | Free (or Pro for production) |

### 1.3 Create the Database
Click **"Create Database"**

⏳ **Wait 2-3 minutes** for the database to be provisioned.

### 1.4 Copy Database URL
Once created:
1. Go to the database settings page
2. Find the **"Internal Database URL"** section (NOT the external one)
3. Copy the full URL that looks like:
   ```
   postgresql://ecommerce_user:PASSWORD@dpg-xxxxx.oregon-postgres.render.com/ecommerce_db
   ```
4. **Save this URL** - you'll need it in the next step

---

## Step 2: Check Web Service Deployment

### 2.1 Your Web Service Should Already Exist
If you've connected your GitHub repository to Render:
- Go to https://render.com/dashboard
- Look for **`ecommerce-backend`** (or your web service name)
- If it doesn't exist, create a new Web Service and connect your GitHub repo

### 2.2 Review Current Settings
Click on the web service to open its settings:
- **Name**: `ecommerce-backend` (or similar)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Region**: Same as database (important for performance)

---

## Step 3: Configure Environment Variables

### 3.1 Generate SECRET_KEY
Run this command in your terminal to generate a secure random key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Copy the output** - you'll need it in the next step.

### 3.2 Add Environment Variables to Render

1. On your web service page, click **"Environment"** tab
2. Click **"Add Environment Variable"** button
3. Add the following variables:

| Key | Value | Description |
|-----|-------|-------------|
| `DATABASE_URL` | Paste the URL from Step 1.4 | PostgreSQL connection string |
| `SECRET_KEY` | Paste from Step 3.1 | Flask secret key for sessions |
| `FLASK_ENV` | `production` | Set Flask to production mode |
| `PORT` | `10000` | Render's port (default) |

### 3.3 Save Variables
Click **"Save"** and wait for the service to redeploy (1-2 minutes)

---

## Step 4: Verify Deployment

### 4.1 Check Deployment Status
1. In your web service, scroll down to see **"Logs"** section
2. Look for messages like:
   - `"Build started"`
   - `"Build succeeded"`
   - `"Service is live at https://ecommerce-backend.onrender.com"`

### 4.2 Test the Application
1. Copy your service URL (e.g., `https://ecommerce-backend.onrender.com`)
2. Open it in your browser
3. You should see the **Stuffus storefront homepage** ✓

### 4.3 If Still Getting 500 Error
Check the logs for errors:
1. Click the **"Logs"** tab
2. Look for error messages
3. Common issues:
   - `DATABASE_URL` not set or incorrect
   - `SECRET_KEY` missing
   - Port not set to `10000`

---

## Step 5: Initialize Database (First Time Only)

After first successful deployment, create database tables:

### 5.1 Access Render Shell
1. In your web service, scroll to the top
2. Click **"Connect"** button
3. Select **"Run command"**
4. This will open a shell where you can run commands

### 5.2 Run Database Migration
In the shell, run:
```bash
flask db upgrade
```

Or if you prefer to create tables directly:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 5.3 Create Admin User (Optional)
In the shell, run:
```bash
python create_admin.py
```

Follow the prompts to create an admin account.

---

## Step 6: Upload Initial Data (Optional)

To populate your store with sample products:

```bash
python seed_data.py
```

---

## Troubleshooting

### ❌ 500 Internal Server Error

**Cause**: Usually missing environment variables or database connection issue

**Solution**:
1. Check all environment variables are set (Step 3)
2. Verify `DATABASE_URL` format is correct
3. Check Render logs for specific error message
4. Restart the service: Click "..." menu → "Restart service"

### ❌ Database Connection Refused

**Cause**: Database URL is wrong or database isn't running

**Solution**:
1. Verify PostgreSQL database is running (check Render dashboard)
2. Copy the Internal Database URL again (not external)
3. Update the `DATABASE_URL` environment variable
4. Redeploy

### ❌ Migrations Failed

**Cause**: Tables already exist or migration conflicts

**Solution**:
1. Connect to database via shell
2. Run: `flask db downgrade` (if needed)
3. Run: `flask db upgrade`

### ❌ Static Files Not Loading

**Cause**: Usually CSS/JS references are broken

**Solution**:
1. Render automatically serves from `/static` folder
2. Check file paths in HTML templates
3. Restart service if files were recently added

---

## Important Notes

⚠️ **For Production Use:**
- Switch to a paid Render plan for better performance
- Use a strong `SECRET_KEY` (the generated one is fine)
- Set `FLASK_ENV=production` (already configured above)
- Enable PostgreSQL backups
- Monitor your service usage

✅ **Monitoring:**
- Check Render dashboard regularly for CPU/memory usage
- Set up email alerts for deployment failures
- Review application logs for errors

---

## Next Steps After Deployment

1. **Test all features**: Login, browse products, add to cart, checkout
2. **Check admin panel**: Navigate to `/auth/login` (after creating admin)
3. **Verify email**: If you've configured email notifications
4. **Monitor performance**: Check Render dashboard for any issues

---

## Support Resources

- Render Documentation: https://render.com/docs
- Flask Documentation: https://flask.palletsprojects.com
- PostgreSQL Documentation: https://www.postgresql.org/docs
- GitHub Issues: Create an issue in your repo if problems occur

---

## Quick Reference

| Task | Command |
|------|---------|
| View logs | Click "Logs" tab in service |
| Restart service | Click "..." → "Restart service" |
| Check variables | Click "Environment" tab |
| Connect to DB | Via Render shell or psql CLI |
| Re-deploy | Push to GitHub (auto-deploys) |

---

**You're all set! Your e-commerce backend should now be live on Render! 🚀**

# Pre-Deployment Checklist for Render

Complete this checklist before pushing to GitHub and deploying to Render.

## 🔍 Configuration & Setup

- [x] **config.py** - Environment variables configured
  - ✅ SECRET_KEY uses `os.getenv()`
  - ✅ DATABASE_URL supports PostgreSQL
  - ✅ Handles postgres:// → postgresql:// conversion for SQLAlchemy
  
- [x] **requirements.txt** - All dependencies included
  - ✅ Flask and extensions
  - ✅ Gunicorn for production server
  - ✅ psycopg2-binary for PostgreSQL
  - ✅ python-dotenv for environment variables

- [x] **Procfile** - Render entry point
  - ✅ Uses gunicorn with proper worker config
  - ✅ Points to app:app correctly

- [x] **runtime.txt** - Python version specified
  - ✅ Python 3.11.8 specified for consistency

- [x] **.env.example** - Environment template
  - ✅ Includes all required variables
  - ✅ Includes Render-specific examples
  - ✅ Clear comments for developers

## 🔐 Security

- [x] **No hardcoded secrets**
  - ✅ SECRET_KEY from environment variable
  - ✅ Database credentials from environment
  - ✅ No API keys in source code

- [x] **.gitignore configured**
  - ✅ .env files excluded
  - ✅ Database files excluded
  - ✅ Virtual environment excluded
  - ✅ __pycache__ excluded

- [x] **app.py main block**
  - ✅ debug mode from environment
  - ✅ host set to 0.0.0.0 (for Render)
  - ✅ port configurable from environment

## 📁 Project Structure

- [x] **Required directories**
  - ✅ templates/ - All HTML templates present
  - ✅ static/ - CSS, JS, upload folders
  - ✅ model/ - Database models
  - ✅ routes/ - API endpoints
  - ✅ migrations/ - Database migrations

- [x] **Entry points**
  - ✅ app.py with create_app() factory
  - ✅ Proper Flask application initialization
  - ✅ All blueprints registered

## 📚 Documentation

- [x] **README.md** - Comprehensive documentation
  - ✅ Project features described
  - ✅ Tech stack listed
  - ✅ Installation instructions
  - ✅ Configuration guide
  - ✅ Troubleshooting section

- [x] **RENDER_DEPLOYMENT.md** - Deployment guide
  - ✅ Step-by-step deployment instructions
  - ✅ Environment variables reference
  - ✅ Troubleshooting guide
  - ✅ Security best practices

- [x] **CHANGELOG.md** - Version history
  - ✅ Initial release documented
  - ✅ Features listed

- [x] **.gitattributes** - Line endings configured
  - ✅ Ensures consistent line endings across platforms

- [x] **LICENSE** - MIT License included
  - ✅ Legal compliance ready

## ✅ Code Quality

- [x] **Database**
  - ✅ SQLAlchemy properly configured
  - ✅ Models defined in model/ directory
  - ✅ Migrations available
  - ✅ db.create_all() in app.py for table creation

- [x] **Error handling**
  - ✅ 404 error handler present
  - ✅ Route protection with before_request
  - ✅ Session management

- [x] **Blueprints**
  - ✅ All routes registered as blueprints
  - ✅ URL prefixes configured
  - ✅ Public/private endpoints separated

## 🚀 Render-Specific

- [x] **Port configuration**
  - ✅ Reads PORT from environment
  - ✅ Defaults to 5000 for local development
  - ✅ Host set to 0.0.0.0

- [x] **Database compatibility**
  - ✅ Works with PostgreSQL
  - ✅ Handles URL format conversion
  - ✅ psycopg2-binary available

- [x] **Gunicorn configuration**
  - ✅ Configured in Procfile
  - ✅ Proper worker count (4 workers)
  - ✅ Timeout set appropriately (60s)

## 📋 Pre-Push Checklist

Before pushing to GitHub:

- [ ] Committed all changes
- [ ] No uncommitted files with `git status`
- [ ] Verified .gitignore excludes unnecessary files
- [ ] Updated version in appropriate files
- [ ] Ran basic code checks locally
- [ ] Updated CHANGELOG.md if needed
- [ ] Confirmed all documentation is accurate

Commands to verify:
```bash
# Check git status
git status

# View files that will be committed
git diff --cached --name-only

# Verify .gitignore
git check-ignore -v <file>  # Check if file would be ignored

# List what will be pushed
git log --oneline origin/main..HEAD
```

## 🎯 Pre-Deployment (Render)

1. **GitHub Ready**
   - [ ] All code pushed to main branch
   - [ ] Latest commit visible on GitHub

2. **Environment Variables Set in Render**
   - [ ] SECRET_KEY - New secure key generated
   - [ ] DATABASE_URL - PostgreSQL URL from Render
   - [ ] FLASK_ENV - Set to "production"
   - [ ] PORT - Set or leave for Render default (10000)

3. **Database Setup**
   - [ ] PostgreSQL database created in Render
   - [ ] Database URL copied correctly
   - [ ] User credentials saved securely

4. **Deployment**
   - [ ] Web Service created
   - [ ] Build command: `pip install -r requirements.txt`
   - [ ] Start command: `gunicorn app:app`
   - [ ] Services linked if needed

5. **Post-Deployment**
   - [ ] Application loads without errors
   - [ ] Admin login page accessible
   - [ ] Database connected properly
   - [ ] Static files serving correctly

## ⚠️ Common Issues to Avoid

- ❌ Don't commit .env file
- ❌ Don't use hardcoded SECRET_KEY
- ❌ Don't forget to set DATABASE_URL in Render
- ❌ Don't use SQLite on Render (no persistent storage)
- ❌ Don't forget Flask migrations might need running
- ❌ Don't ignore error logs during deployment

## 📞 Verification Tests

After deployment, verify:

```
✅ GET http://your-app.onrender.com/ → Returns storefront
✅ GET http://your-app.onrender.com/auth/login → Returns login page
✅ POST login with correct credentials → Redirects to dashboard
✅ POST login with wrong credentials → Shows error
✅ Access /admin without login → Redirects to login
✅ Static files (CSS, JS) load correctly
✅ Database queries work (products, orders, etc.)
```

## 🔗 Helpful Resources

- [Render Documentation](https://render.com/docs)
- [Python Deployment on Render](https://render.com/docs/deploy-python)
- [Flask Documentation](https://flask.palletsprojects.com)
- [SQLAlchemy + PostgreSQL](https://docs.sqlalchemy.org)

---

✅ **When all items are checked, your application is ready for Render deployment!**

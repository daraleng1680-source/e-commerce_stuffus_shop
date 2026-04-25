# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-25

### Added
- Initial release of Backend E-Commerce project
- Admin dashboard for managing products, orders, and customers
- User authentication system for admin and customers
- Product management with categories
- Order management and tracking
- Customer management interface
- Analytics dashboard with order statistics
- File upload support for product images
- Database migration system with Alembic
- RESTful API routes for all operations
- Comprehensive HTML templates for admin and storefront
- Static assets (CSS, JavaScript)
- Helper scripts for database initialization and management

### Features
- Complete admin panel UI
- Customer-facing storefront
- Role-based access control
- Product filtering and search
- Order processing and management
- Customer dashboard

### Security
- User authentication and session management
- Password hashing for user accounts
- CSRF protection ready
- Input validation

### Documentation
- Comprehensive README with setup instructions
- Database schema documentation
- Route documentation
- Configuration guide

### Notes
- SQLite database for development (recommended PostgreSQL for production)
- Flask-SQLAlchemy for ORM
- Jinja2 templating engine
- Bootstrap-compatible HTML templates

from flask import Flask, redirect, url_for, session, flash, request
import os
import config
from datetime import timedelta
from extensions import db, migrate

def create_app(config_class=config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)
    
    # Database and Migrations
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to ensure they are registered with SQLAlchemy
    import model
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Import and Register Blueprints
    from routes.admin.auth import auth_bp
    from routes.storefront import storefront_bp
    from routes.admin.dashboard import dashboard_bp
    from routes.admin.product import product_bp
    from routes.admin.order import admin_bp as order_bp
    from routes.admin.customer import admin_bp as customer_bp
    from routes.admin.category import admin_bp as category_bp
    from routes.admin.analytics import admin_bp as analytics_bp
    from routes.admin.setting import admin_bp as settings_bp
    from routes.admin.user import admin_bp as user_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/admin')
    app.register_blueprint(product_bp, url_prefix='/admin')
    app.register_blueprint(order_bp, url_prefix='/admin')
    app.register_blueprint(customer_bp, url_prefix='/admin')
    app.register_blueprint(category_bp, url_prefix='/admin')
    app.register_blueprint(analytics_bp, url_prefix='/admin')
    app.register_blueprint(settings_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/admin')
    app.register_blueprint(storefront_bp)


    @app.route('/logout')
    def logout():
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for('auth.login'))

    @app.errorhandler(404)
    def page_not_found(e):
        # If a page isn't found, take them back to the homepage
        return redirect(url_for("storefront.index"))

    @app.before_request
    def protect_routes():
        public_endpoints = ['auth.login', 'logout', 'storefront.index', 'storefront.shop']
        if not request.endpoint:
            # If no endpoint, check if it's a static path
            if request.path.startswith('/static/'):
                return None
            return None
            
        if request.endpoint == 'static' or request.endpoint.startswith('static.') or request.endpoint.startswith('storefront.') or request.endpoint in public_endpoints:
            return None
        
        user_id = session.get("user_id")
        if not user_id:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        
        from model import User
        user = User.query.get(user_id)
        if not user:
            session.clear()
            flash("Your account no longer exists.", "warning")
            return redirect(url_for("auth.login"))

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create all tables if they don't exist
        db.create_all()
    
    # Use environment variable to determine debug mode
    debug_mode = app.config.get('DEBUG', False)
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

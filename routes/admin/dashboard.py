from flask import render_template, jsonify, request, Blueprint,session,redirect,url_for,flash
from routes.admin.auth import login_required
import random
from extensions import db

# Create Blueprint
dashboard_bp = Blueprint('admin', __name__, url_prefix='')

# ============ SAMPLE DATA GENERATION ============
def generate_chart_data(period='week'):
    """Generate real chart data from the database"""
    from model import Order
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    # Calculate start date (last 7 days)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=6)
    
    # Query revenue grouped by date
    results = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_amount).label('revenue')
    ).filter(Order.created_at >= start_date)\
     .group_by(func.date(Order.created_at))\
     .order_by('date').all()
    
    # Prepare labels and data for the last 7 days (including days with 0 sales)
    labels = []
    data = []
    revenue_map = {str(r.date): r.revenue for r in results}
    
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')
        labels.append(current_date.strftime('%a')) # Day name (Mon, Tue, etc.)
        data.append(float(revenue_map.get(date_str, 0.0)))
        
    return {
        'labels': labels,
        'datasets': [
            {
                'label': 'Revenue',
                'data': data,
                'borderColor': '#ff9500',
                'backgroundColor': 'rgba(255, 149, 0, 0.1)',
                'fill': True,
                'tension': 0.4
            }
        ],
        'summary': {
            'revenue': f'${sum(data):,.2f}',
            'revenue_change': '0', # Could calculate this vs previous week if needed
            'orders': str(len([d for d in data if d > 0])),
            'orders_change': '0'
        }
    }

def get_analytics_stats(period='week'):
    """Get analytics statistics based on period"""
    base_stats = {
        'week': {
            'revenue': '$12,450',
            'revenue_change': '15',
            'orders': '432',
            'orders_change': '8',
            'avg_order': '$28.81',
            'avg_order_change': '5',
            'conversion': '3.2%',
            'conversion_change': '0.5'
        },
        'month': {
            'revenue': '$52,340',
            'revenue_change': '22',
            'orders': '1,840',
            'orders_change': '14',
            'avg_order': '$28.44',
            'avg_order_change': '7',
            'conversion': '3.8%',
            'conversion_change': '1.2'
        },
        'year': {
            'revenue': '$485,200',
            'revenue_change': '35',
            'orders': '18,450',
            'orders_change': '28',
            'avg_order': '$26.30',
            'avg_order_change': '3',
            'conversion': '4.2%',
            'conversion_change': '2.1'
        }
    }
    return base_stats.get(period, base_stats['week'])

# ============ DASHBOARD ROUTE ============
@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def dashboard_route():
    from model import Product, Category, User, Order
    from sqlalchemy import func
    
    # Fetch real stats from DB
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()
    
    # Calculate Total Revenue
    revenue_sum = db.session.query(func.sum(Order.total_amount)).scalar() or 0.0
    
    stats = {
        'total_orders': str(total_orders),
        'total_revenue': f'${revenue_sum:,.2f}',
        'active_customers': str(total_users),
        'products_in_stock': str(total_products)
    }
    
    # Fetch real recent orders
    db_recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_orders = []
    for o in db_recent_orders:
        recent_orders.append({
            'id': f'#{o.id}',
            'customer': o.customer_name,
            'amount': f'${o.total_amount:,.2f}',
            'status': o.status,
            'date': o.created_at.strftime('%b %d, %Y')
        })

    # Category statistics (Product count per category)
    category_data = db.session.query(
        Category.category_name,
        func.count(Product.id).label('count')
    ).join(Product, Category.id == Product.category_id, isouter=True)\
     .group_by(Category.category_name).all()
    
    category_stats = []
    colors = ['#ff9500', '#4caf50', '#2196f3', '#9c27b0', '#f44336']
    for i, (name, count) in enumerate(category_data):
        category_stats.append({
            'name': name,
            'count': count,
            'color': colors[i % len(colors)]
        })

    # Low stock items (threshold < 10)
    low_stock_db = Product.query.filter(Product.stock < 10).order_by(Product.stock.asc()).limit(5).all()
    low_stock_products = []
    for p in low_stock_db:
        low_stock_products.append({
            'name': p.product_name,
            'stock': p.stock,
            'image': p.image or 'default-product.png'
        })
    
    chart_data = generate_chart_data('week')
    
    return render_template('dashboard/dashboard.html', 
                         stats=stats, 
                         recent_orders=recent_orders, 
                         category_stats=category_stats,
                         low_stock_products=low_stock_products,
                         chart_data=chart_data, 
                         module_name='Dashboard', 
                         module_icon='fa-home')


# ============ API ROUTES FOR DYNAMIC DATA ============
@dashboard_bp.route('/api/analytics')
@login_required
def get_analytics_api():
    """API endpoint for dynamic analytics data"""
    period = request.args.get('period', 'week')
    stats = get_analytics_stats(period)
    chart_data = generate_chart_data(period)
    return jsonify({
        'stats': stats,
        'chart_data': chart_data,
        'period': period
    })


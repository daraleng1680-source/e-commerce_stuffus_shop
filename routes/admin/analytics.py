from flask import render_template, Blueprint
from .dashboard import get_analytics_stats, generate_chart_data
from routes.admin.auth import login_required
from model import Product
from extensions import db
import random

# Create Blueprint
admin_bp = Blueprint('analytics_module', __name__, url_prefix='')

@admin_bp.route('/analytics')
@login_required
def analytics_route():
    from model import Product, Category, Order
    from sqlalchemy import func
    import json
    
    period = 'week'
    chart_data = generate_chart_data(period)
    
    # Real stats from DB
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0.0
    
    # Calculate category data
    db_categories = Category.query.all()
    cat_labels = []
    cat_data = []
    for c in db_categories:
        cat_labels.append(c.category_name)
        cat_data.append(len(c.products))
    
    # Parse top products from Order items_json
    product_sales = {}
    all_orders = Order.query.all()
    for o in all_orders:
        if o.items_json:
            try:
                items = json.loads(o.items_json)
                for item in items:
                    name = item.get('name')
                    qty = item.get('quantity', 1)
                    product_sales[name] = product_sales.get(name, 0) + qty
            except:
                continue
    
    # Sort and get top 5
    sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    top_prod_labels = [p[0] for p in sorted_products] or ['No Sales']
    top_prod_data = [p[1] for p in sorted_products] or [0]

    analytics_data = {
        'stats': {
            'revenue': f'${total_revenue:,.2f}',
            'revenue_change': '0',
            'orders': str(total_orders),
            'orders_change': '0',
            'avg_order': f'${(total_revenue/total_orders):,.2f}' if total_orders > 0 else '$0.00',
            'avg_order_change': '0',
            'conversion': 'N/A',
            'conversion_change': '0'
        },
        'chart_data': {
            'labels': chart_data['labels'],
            'revenue': chart_data['datasets'][0]['data']
        },
        'period': period,
        'categories': {
            'labels': cat_labels or ['General'],
            'data': cat_data or [1],
            'colors': ['#ff9500', '#1e3a5f', '#4caf50', '#2196f3', '#9c27b0']
        },
        'top_products': {
            'labels': top_prod_labels,
            'data': top_prod_data
        }
    }
    
    return render_template('dashboard/analytics.html', analytics=analytics_data, module_name='Analytics & Reports', module_icon='fa-chart-line')

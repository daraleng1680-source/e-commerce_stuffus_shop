from flask import render_template, Blueprint
from routes.admin.auth import login_required

# Create Blueprint
admin_bp = Blueprint('order_module', __name__, url_prefix='')

@admin_bp.route('/orders')
@login_required
def orders_route():
    from model import Order
    from sqlalchemy import func
    from datetime import datetime, date
    from app import db
    
    db_orders = Order.query.order_by(Order.created_at.desc()).all()
    
    orders_list = []
    total_revenue = 0
    pending_count = 0
    today_revenue = 0
    today = date.today()

    for o in db_orders:
        total_revenue += (o.total_amount or 0)
        if o.status == 'pending':
            pending_count += 1
        
        if o.created_at.date() == today:
            today_revenue += (o.total_amount or 0)

        # Simple item count by parsing JSON if available
        item_count = 0
        if o.items_json:
            try:
                import json
                items = json.loads(o.items_json)
                item_count = len(items)
            except:
                item_count = 1

        orders_list.append({
            'id': f'#{o.id}',
            'customer': o.customer_name,
            'email': o.customer_email,
            'amount': f'${o.total_amount:,.2f}',
            'status': o.status,
            'date': o.created_at.strftime('%b %d, %Y'),
            'item_count': item_count
        })

    stats = {
        'total_orders': len(orders_list),
        'total_revenue': f'${total_revenue:,.2f}',
        'pending_orders': pending_count,
        'today_sales': f'${today_revenue:,.2f}'
    }

    return render_template('dashboard/orders.html', orders=orders_list, stats=stats, module_name='Order Management', module_icon='fa-shopping-cart')

@admin_bp.route('/orders/add', methods=['POST'])
@login_required
def add_order():
    from model import Order
    from app import db
    from flask import request, redirect, url_for, flash
    
    try:
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        amount = request.form.get('amount')
        status = request.form.get('status')
        
        if not all([customer_name, customer_email, amount, status]):
            flash('All fields are required!', 'warning')
            return redirect(url_for('order_module.orders_route'))
            
        new_order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            total_amount=float(amount),
            status=status,
            items_json='[]' # Empty items for manual orders for now
        )
        
        db.session.add(new_order)
        db.session.commit()
        flash(f'Order created successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating order: {str(e)}', 'danger')
        
    return redirect(url_for('order_module.orders_route'))

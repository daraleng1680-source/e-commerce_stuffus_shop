from flask import render_template, Blueprint, request, redirect, url_for, flash
from routes.admin.auth import login_required
import json

# Create Blueprint
admin_bp = Blueprint('customer_module', __name__, url_prefix='')

@admin_bp.route('/customers')
@login_required
def customers_route():
    from model import Customer, Order
    from sqlalchemy import func
    from app import db

    page = request.args.get('page', 1, type=int)
    per_page = 10

    # ── Backfill: auto-create Customer rows for any order with no matching customer ──
    orphan_orders = db.session.query(
        Order.customer_email,
        Order.customer_name
    ).outerjoin(Customer, Order.customer_email == Customer.email)\
     .filter(Customer.id == None)\
     .group_by(Order.customer_email, Order.customer_name).all()

    for email, name in orphan_orders:
        if email:
            new_cust = Customer(
                name=name or 'Unknown',
                email=email,
                membership_level='Bronze'
            )
            db.session.add(new_cust)
    if orphan_orders:
        db.session.commit()
    # ────────────────────────────────────────────────────────────────────────────────

    # Aggregate order stats per customer
    customer_stats = db.session.query(
        Customer,
        func.count(Order.id).label('total_orders'),
        func.sum(Order.total_amount).label('total_spent')
    ).outerjoin(Order, Customer.email == Order.customer_email)\
     .group_by(Customer.id)\
     .order_by(Customer.created_at.desc()).all()

    total_customers = len(customer_stats)
    total_revenue = sum((spent or 0.0) for _, _, spent in customer_stats)

    # Server-side pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated = customer_stats[start:end]
    total_pages = max(1, (total_customers + per_page - 1) // per_page)

    customers_list = []
    for customer, order_count, spent in paginated:
        spent = spent or 0.0
        initials = ''.join([n[0] for n in customer.name.split()])[:2].upper()

        # Fetch last 3 orders for this customer (for detail modal)
        recent_orders_db = Order.query\
            .filter_by(customer_email=customer.email)\
            .order_by(Order.created_at.desc()).limit(3).all()

        recent_orders = [
            {
                'id': f'#{o.id}',
                'date': o.created_at.strftime('%b %d, %Y'),
                'amount': f'${o.total_amount:,.2f}',
                'status': o.status.capitalize()
            }
            for o in recent_orders_db
        ]

        customers_list.append({
            'id': customer.id,
            'name': customer.name,
            'initials': initials,
            'email': customer.email,
            'phone': customer.phone or 'N/A',
            'total_orders': order_count,
            'total_spent': f'${spent:,.2f}',
            'member_since': customer.created_at.strftime('%b %Y'),
            'badge': customer.membership_level or 'Bronze',
            'address': customer.address or 'N/A',
            'city': customer.city or 'N/A',
            'avg_spent': f'${(spent / order_count):,.2f}' if order_count > 0 else '$0.00',
            'recent_orders_json': json.dumps(recent_orders)
        })

    stats = {
        'total_customers': total_customers,
        'total_spent': f'${total_revenue:,.2f}',
        'avg_spent': f'${(total_revenue / total_customers):,.2f}' if total_customers else '$0.00',
        'retention': '100%'
    }

    pagination = {
        'current_page': page,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1,
        'next_page': page + 1,
        'pages': list(range(max(1, page - 2), min(total_pages + 1, page + 3)))
    }

    return render_template(
        'dashboard/customers.html',
        customers=customers_list,
        stats=stats,
        pagination=pagination,
        module_name='Customer Management',
        module_icon='fa-users'
    )


@admin_bp.route('/customers/add', methods=['POST'])
@login_required
def add_customer():
    from model import Customer
    from app import db

    try:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        city = request.form.get('city', '').strip()
        membership = request.form.get('membership', 'Bronze')

        if not name or not email:
            flash('Name and Email are required!', 'warning')
            return redirect(url_for('customer_module.customers_route'))

        existing = Customer.query.filter_by(email=email).first()
        if existing:
            flash(f'A customer with email {email} already exists!', 'danger')
            return redirect(url_for('customer_module.customers_route'))

        new_customer = Customer(
            name=name,
            email=email,
            phone=phone or None,
            city=city or None,
            membership_level=membership
        )
        db.session.add(new_customer)
        db.session.commit()
        flash(f'Customer "{name}" added successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error adding customer: {str(e)}', 'danger')

    return redirect(url_for('customer_module.customers_route'))

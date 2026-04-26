from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from functools import wraps
import json

storefront_bp = Blueprint('storefront', __name__)

def customer_login_required(f):
    """Decorator to require customer login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('customer_id'):
            flash("Please log in first.", "warning")
            return redirect(url_for("storefront.customer_login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Homepage - New Landing Page
@storefront_bp.route('/')
def index():
    """Premium landing page with featured content"""
    from model import Product, Category
    from extensions import db
    
    try:
        featured_products = Product.query.filter_by(status='instock').limit(4).all()
        categories = Category.query.all()
    except Exception as e:
        # If database error, return empty lists
        featured_products = []
        categories = []
    
    return render_template('storefront/index.html', 
                         featured_products=featured_products,
                         categories=categories)

# Shop Page - Product Listing
@storefront_bp.route('/shop')
def shop():
    """Display all products with filtering and pagination"""
    from extensions import db
    from model import Product, Category
    
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('search', '')
    
    try:
        # Build query
        query = Product.query.filter_by(status='instock')
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search_query:
            query = query.filter(Product.product_name.ilike(f'%{search_query}%'))
        
        products = query.paginate(page=page, per_page=12)
        categories = Category.query.all()
    except Exception as e:
        # If database error, return empty results
        products = None
        categories = []
    
    return render_template('storefront/shop.html', 
                         products=products,
                         categories=categories,
                         selected_category=category_id,
                         search_query=search_query)

# Product Detail Page
@storefront_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Display product detail page"""
    from model import Product
    
    try:
        product = Product.query.get_or_404(product_id)
        related_products = Product.query.filter(
            Product.category_id == product.category_id,
            Product.id != product_id,
            Product.status == 'instock'
        ).limit(4).all()
    except Exception as e:
        # If database error, redirect to shop
        flash("Product not found.", "warning")
        return redirect(url_for("storefront.shop"))
    
    return render_template('storefront/product_detail.html',
                         product=product,
                         related_products=related_products)

# Cart Management
@storefront_bp.route('/cart')
def view_cart():
    """Display shopping cart"""
    from model import Product
    
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('storefront/cart.html',
                         cart_items=cart_items,
                         total=total)

@storefront_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@customer_login_required
def add_to_cart(product_id):
    """Add product to cart"""
    from model import Product
    
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', 1, type=int)
    
    # Initialize cart in session
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    session.modified = True
    flash(f"{product.product_name} added to cart!", "success")
    
    return redirect(request.referrer or url_for('storefront.index'))

@storefront_bp.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Update cart item quantity"""
    quantity = request.form.get('quantity', 1, type=int)
    
    if 'cart' not in session:
        session['cart'] = {}
    
    if quantity <= 0:
        session['cart'].pop(str(product_id), None)
        flash("Item removed from cart", "info")
    else:
        session['cart'][str(product_id)] = quantity
        flash("Cart updated", "success")
    
    session.modified = True
    return redirect(url_for('storefront.view_cart'))

@storefront_bp.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Remove product from cart"""
    if 'cart' in session:
        session['cart'].pop(str(product_id), None)
        session.modified = True
        flash("Item removed from cart", "info")
    
    return redirect(url_for('storefront.view_cart'))

@storefront_bp.route('/cart/clear', methods=['POST'])
def clear_cart():
    """Clear entire cart"""
    session['cart'] = {}
    session.modified = True
    flash("Cart cleared", "info")
    return redirect(url_for('storefront.view_cart'))

# Checkout
@storefront_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page"""
    from model import Product
    
    if not session.get('cart'):
        flash("Your cart is empty", "warning")
        return redirect(url_for('storefront.index'))
    
    if request.method == 'POST':
        # Process checkout
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        
        if not all([name, email, phone, address, city, country]):
            flash("All fields are required", "danger")
            return redirect(url_for('storefront.checkout'))
        
        # Store order info in session for now
        session['order_info'] = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'city': city,
            'country': country
        }
        session.modified = True
        
        # Redirect to order confirmation
        return redirect(url_for('storefront.order_confirmation'))
    
    # Calculate cart total
    cart = session.get('cart', {})
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            total += product.price * quantity
    
    return render_template('storefront/checkout.html', cart_total=total)

@storefront_bp.route('/order/confirmation')
def order_confirmation():
    """Order confirmation page"""
    from model import Product
    
    if not session.get('order_info'):
        return redirect(url_for('storefront.index'))
    
    order_info = session.get('order_info')
    cart = session.get('cart', {})
    
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('storefront/order_confirmation.html',
                         order_info=order_info,
                         cart_items=cart_items,
                         total=total)

@storefront_bp.route('/order/complete', methods=['POST'])
def complete_order():
    """Complete the order and save to DB"""
    from model import Order, Product, Customer
    from extensions import db
    
    order_info = session.get('order_info')
    if not order_info:
        return redirect(url_for('storefront.index'))
    
    cart = session.get('cart', {})
    total = 0
    items_summary = []
    
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            subtotal = product.price * quantity
            total += subtotal
            items_summary.append({
                'name': product.product_name,
                'quantity': quantity,
                'price': product.price
            })
    
    # Upsert Customer record (create if not exists)
    customer = Customer.query.filter_by(email=order_info['email']).first()
    if not customer:
        customer = Customer(
            name=order_info['name'],
            email=order_info['email'],
            phone=order_info.get('phone'),
            address=order_info.get('address'),
            city=order_info.get('city'),
            membership_level='Bronze'
        )
        db.session.add(customer)
    
    # Create Real Order Record
    new_order = Order(
        customer_name=order_info['name'],
        customer_email=order_info['email'],
        total_amount=total,
        status='pending',
        items_json=json.dumps(items_summary)
    )
    
    db.session.add(new_order)
    db.session.commit()
    
    # Clear cart and order info
    session['cart'] = {}
    session['order_info'] = None
    session.modified = True
    
    flash("Order placed successfully! Thank you for your purchase.", "success")
    return redirect(url_for('storefront.index'))

# Customer Authentication
@storefront_bp.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    """Customer login page"""
    from model import Customer
    from werkzeug.security import check_password_hash
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash("Email and password are required", "danger")
            return redirect(url_for('storefront.customer_login'))
            
        customer = Customer.query.filter_by(email=email).first()
        
        if customer and customer.password and check_password_hash(customer.password, password):
            session['customer_id'] = customer.id
            session['customer_email'] = customer.email
            session['customer_name'] = customer.name
            flash(f"Welcome back, {customer.name}!", "success")
            
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('storefront.index'))
            
        flash("Invalid email or password", "danger")
    
    return render_template('storefront/customer_login.html')

@storefront_bp.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    """Customer registration page"""
    from model import Customer
    from extensions import db
    from werkzeug.security import generate_password_hash
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not name or not email or not password:
            flash("Name, email, and password are required", "danger")
            return redirect(url_for('storefront.customer_register'))
        
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('storefront.customer_register'))
            
        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            # If the customer exists but has no password (e.g. from guest checkout)
            if not existing_customer.password:
                existing_customer.password = generate_password_hash(password)
                existing_customer.name = name
                db.session.commit()
                
                session['customer_id'] = existing_customer.id
                session['customer_email'] = existing_customer.email
                session['customer_name'] = existing_customer.name
                flash("Registration successful! Welcome!", "success")
                return redirect(url_for('storefront.index'))
            else:
                flash("Email already registered. Please login.", "warning")
                return redirect(url_for('storefront.customer_login'))
        
        # Create new customer
        new_customer = Customer(
            name=name,
            email=email,
            password=generate_password_hash(password),
            membership_level='Bronze'
        )
        db.session.add(new_customer)
        db.session.commit()
        
        # Store customer session
        session['customer_id'] = new_customer.id
        session['customer_email'] = new_customer.email
        session['customer_name'] = new_customer.name
        flash("Registration successful! Welcome!", "success")
        return redirect(url_for('storefront.index'))
    
    return render_template('storefront/customer_register.html')

@storefront_bp.route('/customer/logout')
def customer_logout():
    """Logout customer"""
    session.pop('customer_id', None)
    session.pop('customer_email', None)
    session.pop('customer_name', None)
    flash("You have been logged out", "info")
    return redirect(url_for('storefront.index'))

# Customer Orders (if logged in)
@storefront_bp.route('/customer/orders')
@customer_login_required
def customer_orders():
    """Display customer orders"""
    # TODO: Implement order history from database
    return render_template('storefront/customer_orders.html')

# Homepage redirect removed - handled by index() above

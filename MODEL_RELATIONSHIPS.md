# Database Models & Relationships

## Entity Relationship Diagram (ERD)

```
┌──────────────────────────────┐
│        CATEGORY              │
├──────────────────────────────┤
│ id (PK)                      │
│ category_name                │
│ description                  │
└──────────────────────────────┘
           ▲
           │ (1:N)
           │
        has_many
           │
           ▼
┌──────────────────────────────┐
│        PRODUCT               │
├──────────────────────────────┤
│ id (PK)                      │
│ product_name                 │
│ price                        │
│ stock                        │
│ category_id (FK) ─────────┐  │
│ image                      │  │
│ description                │  │
│ create_at                  │  │
│ update_at                  │  │
└──────────────────────────────┘
           ▲
           │ (1:N)
           │
        has_many
           │
           ▼
┌──────────────────────────────┐
│        ORDER_ITEM            │
├──────────────────────────────┤
│ id (PK)                      │
│ order_id (FK) ────┐          │
│ product_id (FK) ──┼──┐       │
│ quantity          │  │       │
│ unit_price        │  │       │
└──────────────────────────────┘
           ▲         │
           │         │
        (1:N)      (1:N)
           │         │
        has_many  has_many
           │         │
           └─────────┴──────┐
                            │
                ┌───────────┘
                │
                ▼
┌──────────────────────────────┐       ┌──────────────────────────────┐
│        ORDER                 │       │      CUSTOMER                │
├──────────────────────────────┤       ├──────────────────────────────┤
│ id (PK)                      │       │ id (PK)                      │
│ order_number                 │       │ name                         │
│ customer_id (FK) ─────────────┼─────→│ email (UNIQUE)               │
│ total_amount                 │       │ phone                        │
│ status                       │       │ address                      │
│ create_at                    │       │ city                         │
│ update_at                    │       │ country                      │
└──────────────────────────────┘       │ join_date                    │
           ▲                            │ create_at                    │
           │ (1:N)                      │ update_at                    │
           │                            └──────────────────────────────┘
        has_many
           │
        customer has
           │
           ▼
┌──────────────────────────────┐
│       DISCOUNT               │
├──────────────────────────────┤
│ id (PK)                      │
│ code (UNIQUE)                │
│ description                  │
│ discount_percent             │
│ expiry_date                  │
│ is_active                    │
│ create_at                    │
│ update_at                    │
└──────────────────────────────┘
```

## Model Relationships

### 1. **Category ↔ Product** (One-to-Many)
- **One Category** has **Many Products**
- Foreign Key: `Product.category_id` → `Category.id`
- Access Products: `category.products`
- Access Category: `product.category`

```python
# Example usage:
category = Category.query.get(1)
products = category.products  # Get all products in this category

product = Product.query.get(1)
category = product.category  # Get the category of this product
```

### 2. **Customer ↔ Order** (One-to-Many)
- **One Customer** has **Many Orders**
- Foreign Key: `Order.customer_id` → `Customer.id`
- Access Orders: `customer.orders`
- Access Customer: `order.customer`

```python
# Example usage:
customer = Customer.query.get(1)
orders = customer.orders  # Get all orders by this customer

order = Order.query.get(1)
customer = order.customer  # Get the customer who placed this order
```

### 3. **Order ↔ OrderItem** (One-to-Many)
- **One Order** has **Many OrderItems**
- Foreign Key: `OrderItem.order_id` → `Order.id`
- Access OrderItems: `order.order_items`
- Access Order: `order_item.order`

```python
# Example usage:
order = Order.query.get(1)
items = order.order_items  # Get all items in this order

order_item = OrderItem.query.get(1)
order = order_item.order  # Get the order containing this item
```

### 4. **Product ↔ OrderItem** (One-to-Many)
- **One Product** has **Many OrderItems** (ordered multiple times)
- Foreign Key: `OrderItem.product_id` → `Product.id`
- Access OrderItems: `product.order_items`
- Access Product: `order_item.product`

```python
# Example usage:
product = Product.query.get(1)
order_items = product.order_items  # Get all orders containing this product

order_item = OrderItem.query.get(1)
product = order_item.product  # Get the product in this order item
```

## Creating Records with Relationships

```python
# 1. Create a category and product
category = Category(category_name='Indoor Plants', description='...')
db.session.add(category)
db.session.commit()

product = Product(
    product_name='Snake Plant',
    price=29.99,
    stock=50,
    category_id=category.id,
    description='Low maintenance plant'
)
db.session.add(product)
db.session.commit()

# 2. Create a customer and order
customer = Customer(
    name='John Doe',
    email='john@example.com',
    phone='555-0123'
)
db.session.add(customer)
db.session.commit()

order = Order(
    order_number='ORD-001',
    customer_id=customer.id,
    total_amount=150.00,
    status='pending'
)
db.session.add(order)
db.session.commit()

# 3. Add items to order
order_item = OrderItem(
    order_id=order.id,
    product_id=product.id,
    quantity=2,
    unit_price=29.99
)
db.session.add(order_item)
db.session.commit()
```

## Querying with Relationships

```python
# Get all products in "Indoor Plants" category
products = Product.query.filter_by(category_id=1).all()

# OR using relationship
category = Category.query.get(1)
products = category.products

# Get all orders for a customer
customer = Customer.query.get(1)
orders = customer.orders

# Get all products ordered by a customer
customer = Customer.query.get(1)
products = []
for order in customer.orders:
    for item in order.order_items:
        products.append(item.product)

# Get products in a specific category with their order history
category = Category.query.get(1)
for product in category.products:
    print(f"{product.product_name} ordered {len(product.order_items)} times")
```

## Migrations

After defining these models, run:

```bash
# Initialize migration
flask db init

# Create migration
flask db migrate -m "Initial models setup"

# Apply migration
flask db upgrade
```

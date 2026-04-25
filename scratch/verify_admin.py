from app import create_app
from model import User, Order, Product
import json

app = create_app()
with app.app_context():
    print("--- All Users ---")
    users = User.query.all()
    for u in users:
        print(f"Username: {u.username} | Profile: {u.profile}")
    
    print("\n--- Statistics ---")
    print(f"Total Products: {Product.query.count()}")
    print(f"Total Orders: {Order.query.count()}")
    
    recent_order = Order.query.order_by(Order.id.desc()).first()
    if recent_order:
        print(f"\n--- Most Recent Order ---")
        print(f"Customer: {recent_order.customer_name}")
        print(f"Amount: ${recent_order.total_amount}")
        print(f"Items: {recent_order.items_json}")

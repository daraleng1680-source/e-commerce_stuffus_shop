from extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), nullable=False, default='pending') # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Simple order items stored as JSON for now to keep it lightweight
    items_json = db.Column(db.Text, nullable=True) 

    def __repr__(self):
        return f'<Order {self.id} by {self.customer_email}>'

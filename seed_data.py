from app import app
from extensions import db
from model import Product, Category, User
from werkzeug.security import generate_password_hash

def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create Categories
        cat1 = Category(category_name="Electronics", description="Latest gadgets and tech")
        cat2 = Category(category_name="Fashion", description="Trendy apparel and accessories")
        cat3 = Category(category_name="Home & Living", description="Essentials for your home")
        
        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()

        # Create Products
        p1 = Product(
            product_name="Pro Wireless Headphones",
            price=199.99,
            stock=15,
            category_id=cat1.id,
            description="Experience crystal clear sound with active noise cancellation and 40-hour battery life.",
            status="instock"
        )
        p2 = Product(
            product_name="Minimalist Smart Watch",
            price=149.50,
            stock=25,
            category_id=cat1.id,
            description="Track your health and stay connected with this sleek, water-resistant smartwatch.",
            status="instock"
        )
        p3 = Product(
            product_name="Organic Cotton Hoodie",
            price=59.99,
            stock=50,
            category_id=cat2.id,
            description="Premium comfort meets sustainable style. Perfect for every season.",
            status="instock"
        )
        p4 = Product(
            product_name="Ceramic Table Lamp",
            price=85.00,
            stock=10,
            category_id=cat3.id,
            description="Handcrafted ceramic base with a linen shade, adding a touch of elegance to any room.",
            status="instock"
        )
        p5 = Product(
            product_name="Leather Messenger Bag",
            price=120.00,
            stock=8,
            category_id=cat2.id,
            description="Genuine top-grain leather bag with multiple compartments for all your essentials.",
            status="instock"
        )

        db.session.add_all([p1, p2, p3, p4, p5])
        
        # Create Admin User
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
            profile="admin.jpg"
        )
        db.session.add(admin)
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()

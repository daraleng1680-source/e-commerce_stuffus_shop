from extensions import db

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Category {self.category_name}>'

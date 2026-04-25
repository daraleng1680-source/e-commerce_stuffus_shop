from flask import render_template, Blueprint, request, redirect, url_for, flash
from routes.admin.auth import login_required

# Create Blueprint
admin_bp = Blueprint('category_module', __name__, url_prefix='')


@admin_bp.route('/categories')
@login_required
def categories_route():
	from extensions import db
	from model import Category
	categories = db.session.query(Category).all()
	
	# Build categories data with product count
	categories_data = []
	for category in categories:
		categories_data.append({
			'id': category.id,
			'name': category.category_name,
			'description': category.description,
			'product_count': len(category.products)
		})
	
	return render_template('dashboard/categories.html', categories=categories_data, module_name='Category Management', module_icon='fa-list')


# Add Category
@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
	from extensions import db
	from model import Category
	
	if request.method == 'POST':
		name = request.form.get('name')
		description = request.form.get('description')
		
		# Check if category already exists
		existing = db.session.query(Category).filter_by(category_name=name).first()
		if existing:
			flash('Category with this name already exists!', 'warning')
			return render_template('dashboard/add_category.html')
		
		# Create new category
		new_category = Category(category_name=name, description=description)
		db.session.add(new_category)
		db.session.commit()
		
		flash('Category added successfully!', 'success')
		return redirect(url_for('category_module.categories_route'))
	
	return render_template('dashboard/add_category.html')


# Edit Category
@admin_bp.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
	from extensions import db
	from model import Category
	
	category = db.session.query(Category).get(category_id)
	if not category:
		flash('Category not found.', 'danger')
		return redirect(url_for('category_module.categories_route'))
	
	if request.method == 'POST':
		name = request.form.get('name')
		description = request.form.get('description')
		
		# Check if new name already exists (and it's not the same category)
		existing = db.session.query(Category).filter_by(category_name=name).filter(Category.id != category_id).first()
		if existing:
			flash('Category with this name already exists!', 'warning')
			return render_template('dashboard/edit_category.html', category={'id': category.id, 'name': category.category_name, 'description': category.description})
		
		category.category_name = name
		category.description = description
		db.session.commit()
		
		flash('Category updated successfully!', 'success')
		return redirect(url_for('category_module.categories_route'))
	
	return render_template('dashboard/edit_category.html', category={'id': category.id, 'name': category.category_name, 'description': category.description})


# Delete Category
@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
	from extensions import db
	from model import Category
	
	category = db.session.query(Category).get(category_id)
	if not category:
		flash('Category not found.', 'danger')
		return redirect(url_for('category_module.categories_route'))
	
	# Check if category has products
	if category.products:
		flash(f'Cannot delete category with {len(category.products)} associated product(s)!', 'danger')
		return redirect(url_for('category_module.categories_route'))
	
	db.session.delete(category)
	db.session.commit()
	
	flash('Category deleted successfully!', 'success')
	return redirect(url_for('category_module.categories_route'))

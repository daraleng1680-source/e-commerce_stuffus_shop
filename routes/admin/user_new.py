from flask import render_template, request, redirect, url_for, Blueprint, flash
from app import db, User
from routes.admin.auth import login_required

admin_bp = Blueprint('user_module', __name__, url_prefix='')

@admin_bp.route('/user')
@login_required
def user_list():
    """Display list of all users with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = User.query.paginate(page=page, per_page=per_page)
    users = pagination.items
    total_pages = pagination.pages
    total = pagination.total
    
    return render_template('dashboard/users.html', 
                         module_name='Users', 
                         module_icon='fa-users', 
                         module='users',
                         users=users, 
                         page=page, 
                         total_pages=total_pages, 
                         total=total)

@admin_bp.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """Add a new user"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        profile = request.form.get('profile')
        
        if not all([username, password, profile]):
            flash('All fields are required!', 'error')
            return redirect(url_for('user_module.add_user'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('user_module.add_user'))
        
        new_user = User(
            username=username,
            password=password,
            profile=profile
        )
        
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('user_module.user_list'))
    
    return render_template('dashboard/add_user.html', 
                         module_name='Add User',
                         module_icon='fa-user-plus',
                         module='users')

@admin_bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit an existing user"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        profile = request.form.get('profile')
        
        if not all([username, password, profile]):
            flash('All fields are required!', 'error')
            return redirect(url_for('user_module.edit_user', user_id=user_id))
        
        # Check if new username is already taken by another user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user_id:
            flash('Username already exists!', 'error')
            return redirect(url_for('user_module.edit_user', user_id=user_id))
        
        user.username = username
        user.password = password
        user.profile = profile
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('user_module.user_list'))
    
    return render_template('dashboard/edit_user.html',
                         user=user,
                         module_name='Edit User',
                         module_icon='fa-user-edit',
                         module='users')

@login_required
@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    
    return redirect(url_for('user_module.user_list'))

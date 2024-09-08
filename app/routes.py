from app import app, db #login  
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as os

from .models import User, Products, user_product
from .forms import RegistrationForm, LoginForm, ShopForm, ResetPasswordRequestForm, ResetPasswordForm
from .send_mail import send_confirmation_email, send_reset_password_email
from .decorators import admin_required


@app.route('/')
def home():
    # products = db.session.scalars(sa.select(Products))
    products = db.paginate(sa.select(Products), per_page=6)
    return render_template('index.html', products=products)


@app.route('/products')
def products_list():
    products = db.session.scalars(sa.select(Products))
    return render_template('products.html', products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = db.session.scalar(sa.select(Products).where(Products.id == product_id))
    return render_template('product_detail.html', product=product) 


@app.route('/products/<int:product_id>/remove')
def remove_product(product_id):
    if  not current_user.is_authenticated:
        return redirect(url_for('login'))

    db.session.query(user_product).filter(user_product.c.user_id == current_user.id).filter(user_product.c.product_id == product_id).delete()
    db.session.commit()

    flash(message='You successfully remove this product', category='success')
    return redirect(url_for('shopping_cart'))


# post_products
@app.route('/products/post', methods=['GET', 'POST'])
def post_products():
    form=ShopForm()
    if form.validate_on_submit():
        new_product=Products(
            # seller=current_user,  # мені здається що продавця можна і без форми записати
            title=form.title.data,
            description=form.description.data,
            seller=form.seller.data,
            price=form.price.data
        )
        new_product.set_photo_path(form.photo.data)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post_product.html', form=form)


#buy_product
@app.route('/products/<int:product_id>/buy')
def buy_products(product_id):
    product = db.session.scalar(sa.select(Products).where(Products.id == product_id))
    user_products = db.session.scalars(current_user.user_products.select()).all()
    
    if product in user_products:

        flash(message='You already has bought this product', category='danger')
        return redirect(url_for('home')) 

    
    product.users.add(current_user)
    db.session.commit()
    flash(message='You successfully  bought this product', category='success')
    return redirect(url_for('home'))

#confirm_mail
@app.route('/confirm-email/<token>')
def confirm_email(token):
    user = User.verify_token(token) # USER or None
    if not user:
        return '<h1>Cannot confirm your email</h1>'
    user.is_admin = True
    db.session.commit()
    return '<h1>You have confirmed your email successfully</h1>'

#reset_password
@app.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            send_reset_password_email(user)
    return render_template('reset_password_request.html', form=form)


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token(token)  # USER or None
    if not user:
        return '<h1>Invalid link'
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)





# registration/login/logout

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if not user or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# shopping_cart
@app.route('/shoppingcart')
def shopping_cart():
    products = db.session.scalars(current_user.user_products.select()).all()
    return render_template('shopping_cart.html', products=products)

@app.route('/info')
def info():
    return render_template('info.html')



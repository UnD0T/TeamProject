from app import app, db #login  
from flask import render_template, url_for, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as os

from app.models import User, Products
from forms import RegistrationForm, LoginForm, ShopForm
from decorators import logout_required


@app.route('/')
def home():
    products = db.session.scalars(sa.select(Products))
    return render_template('home.html', products=products)


@app.route('/products')
def products():
    products = db.session.scalars(sa.select(Products))
    return render_template('products.html', products=products)


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

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('post_product.html')


#buy_product
@app.route('/products/<int:product_id>/buy')
def buy_products(product_id):
    product = db.session.scalar(sa.select(Products).where(Products.id == product_id))
    user_products = db.session.scalars(current_user.user_products.select().all())
    
    if product in user_products:
        return redirect(url_for('products')) # треба буде добавити якесь повідомленнян що цей item вже куплений 
    
    product.users.add(current_user)
    db.session.commit()
    return redirect(url_for('products'))



# registration/login/logout

@app.route('/registration', methods=['GET', 'POST'])
@logout_required
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data) 

        db.session.add(new_user)
        db.session.commit()
        login_user()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if not user or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user()
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# profile

@app.route('/profile')
def profile():
    return render_template('profile.hmtl')
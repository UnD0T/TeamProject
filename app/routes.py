from app import app, db #login  
from flask import render_template, url_for, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import sqlalchemy as sa
import sqlalchemy.orm as os

from .models import User, Products
from .forms import RegistrationForm, LoginForm, ShopForm
from .decorators import admin_required


@app.route('/')
def home():
    products = db.session.scalars(sa.select(Products))
    return render_template('index.html', products=products )


# @app.route('/products')
# def products_list():
#     products = db.session.scalars(sa.select(Products))
#     return render_template('products.html', products=products)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = db.session.scalar(sa.select(Products).where(Products.id == product_id))
    return render_template('product_detail.html', product=product) 

# post_products
@app.route('/products/post', methods=['GET', 'POST'])
def post_products():
    form=ShopForm()
    print('endpoint')
    if form.validate_on_submit(): #чомусь у form.photo.data повертається none і тому валідація не проходить
        print('validate_on_submit')
        new_product=Products(
            # seller=current_user,  # мені здається що продавця можна і без форми записати
            title=form.title.data,
            description=form.description.data,
            seller=form.seller.data,
            price=form.price.data
        )
        print('new product')
        new_product.set_photo_path(form.photo.data) 

        
        # uploaded_file = form.photo.data
        # filename = secure_filename(uploaded_file.filename)
        # post_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        # uploaded_file.save(post_path)
        # new_product.photo = post_path
        # path_list = new_product.photo.split('/')[1:]
        # new_path = '/'.join(path_list)

        # new_product.photo = new_path

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post_product.html', form=form)


#buy_product
@app.route('/products/<int:product_id>/buy')
def buy_products(product_id):
    if  not current_user.is_authenticated:
        return redirect(url_for('login'))
    product = db.session.scalar(sa.select(Products).where(Products.id == product_id))
    user_products = db.session.scalars(current_user.user_products.select().all())
    
    if product in user_products:
        return redirect(url_for('products')) # треба буде добавити якесь повідомленнян що цей item вже куплений 
    
    product.users.add(current_user)
    db.session.commit()
    return redirect(url_for('products'))



# registration/login/logout

@app.route('/registration', methods=['GET', 'POST'])
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
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


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


# profile

@app.route('/profile')
def profile():
    products = db.session.scalars(sa.select(Products))
    return render_template('profile.html', products=products)
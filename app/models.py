import os
from datetime import datetime
from time import time

import jwt
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from config import Config
from app import db, login, app
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional

user_product = sa.Table(
    'user_product',
    db.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'), primary_key=True))


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    is_admin: so.Mapped[bool] = so.mapped_column(default=False)
    # is_seller: so.Mapped[bool] #можна буде зробити вибір при реєстрації: продавець/покупець
    user_products: so.WriteOnlyMapped['Products'] = so.relationship('Products', secondary=user_product, back_populates='users')
    sell_products: so.WriteOnlyMapped['Products'] = so.relationship(back_populates='seller')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expire_in=600):
        return jwt.encode({'id': self.id, 'exp': time()+expire_in},
                          '123456789', algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, '123456789', algorithms=['HS256'])['id']
        except:
            return
        return User.query.get_or_404(id)

    def __repr__(self):
        return self.username


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Products(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    description: so.MappedColumn[str]
    # seller: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    seller_id: so.MappedColumn[int] = so.mapped_column(sa.ForeignKey(User.id))
    seller: so.Mapped[User] = so.relationship(back_populates='sell_products')
    photo: so.MappedColumn[str]
    # time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now())
    price: so.MappedColumn[float]
    users: so.WriteOnlyMapped[User] = so.relationship('User', secondary=user_product, back_populates='user_products', passive_deletes=True)

    def __repr__(self):
        return f'Products: {self.title}'



    def set_photo_path(self, data_in_form):
        print('set_path')
        filename = secure_filename(data_in_form.filename)
        products_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        data_in_form.save(products_path)
        self.photo = products_path
        path_list = products_path.split('/')[1:]
        new_path = '/'.join(path_list)
        self.photo = new_path


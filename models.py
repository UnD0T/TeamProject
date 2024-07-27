from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db, login
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional

user_product = sa.Table(
    'user_product',
    db.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column('product_id', sa.Integer, sa.ForeignKey('product.id'), primary_key=True))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128))
    is_admin: so.Mapped[bool] = so.mapped_column(default=False)
    user_products: so.WriteOnlyMapped['Tour'] = so.relationship('Products', secondary=user_product,back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return self.username


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Products(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    description: so.MappedColumn[str]
    seller: so.MappedColumn[str] = so.mapped_column(sa.String(60))
    # time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now())
    price: so.MappedColumn[float]
    users: so.WriteOnlyMapped[User] = so.relationship('User', secondary=user_product, back_populates='user_products')

    def __repr__(self):
        return f'Tour: {self.title}'

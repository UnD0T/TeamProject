from app import db, login
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
# from datetime import datetime

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True, index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), index=True)
    user_posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    def __repr__(self) -> str:
        return f'User: {self.username}'


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return  check_password_hash(self.password_hash, password)
    


@login.user_loader
def user_loader(id):
    return db.session.get(User, id)


class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='category')



class Post(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(50))
    content: so.MappedColumn[str] = so.mapped_column(sa.Text)
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Category.id))
    category: so.Mapped[Category] = so.relationship(back_populates='posts')
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    author: so.Mapped[User] = so.relationship(back_populates='user_posts')
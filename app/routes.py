from app import app, db #login  
from flask import render_template, url_for, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
import sqlalchemy as sa
import sqlalchemy.orm as os
# from app.models import User


@app.route('/')
def home():
    return render_template('home.html')
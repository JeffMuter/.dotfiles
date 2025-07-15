from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from database.db import get_db_session
from database.models import User

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# Initialize LoginManager
login_manager = LoginManager()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@login_manager.user_loader
def load_user(user_id):
    db = get_db_session()
    try:
        return db.query(User).get(int(user_id))
    finally:
        db.close()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        db = get_db_session()
        try:
            user = db.query(User).filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            flash('Invalid email or password')
        finally:
            db.close()
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        db = get_db_session()
        try:
            if db.query(User).filter_by(email=form.email.data).first():
                flash('Email already registered')
                return render_template('auth/register.html', form=form)
            
            if db.query(User).filter_by(username=form.username.data).first():
                flash('Username already taken')
                return render_template('auth/register.html', form=form)
            
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.add(user)
            db.commit()
            
            login_user(user)
            return redirect(url_for('index'))
        finally:
            db.close()
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index')) 
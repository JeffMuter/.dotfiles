from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
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
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        db = get_db_session()
        try:
            current_app.logger.debug(f"Attempting login for email: {form.email.data}")
            user = db.query(User).filter_by(email=form.email.data).first()
            
            if user:
                current_app.logger.debug("User found, checking password")
                if user.check_password(form.password.data):
                    current_app.logger.debug("Password correct, logging in user")
                    login_user(user)
                    next_page = request.args.get('next')
                    flash('Login successful!', 'success')
                    return redirect(next_page or url_for('home'))
                else:
                    current_app.logger.debug("Password incorrect")
            else:
                current_app.logger.debug("No user found with this email")
            
            flash('Invalid email or password', 'danger')
        finally:
            db.close()
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        db = get_db_session()
        try:
            if db.query(User).filter_by(email=form.email.data).first():
                flash('Email already registered', 'danger')
                return render_template('auth/register.html', form=form)
            
            if db.query(User).filter_by(username=form.username.data).first():
                flash('Username already taken', 'danger')
                return render_template('auth/register.html', form=form)
            
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            current_app.logger.debug(f"Creating new user with email: {form.email.data}")
            db.add(user)
            db.commit()
            
            login_user(user)
            flash('Registration successful! Welcome to PyDial!', 'success')
            return redirect(url_for('home'))
        finally:
            db.close()
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home')) 
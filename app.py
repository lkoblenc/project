from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap 
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'thingxThingYthingZ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

moment = Moment(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False, unique=False)
	email = db.Column(db.String(200), nullable=False, unique=True)
	username = db.Column(db.String(200), nullable=False, unique=False)
	#username is used to record the user creating the contact (one to many)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(200), nullable=False, unique=True)
	password = db.Column(db.String(200), nullable=False, unique=False)

if not os.path.exists('database.db'):
	db.create_all()

class ContactForm(FlaskForm):
	name = StringField('Enter your name', validators=[DataRequired()])
	email = EmailField('Email address', [DataRequired(), Email()])
	submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    name = StringField('Edit the name', validators=[DataRequired()])
    email = EmailField('Email address', [DataRequired(), Email()])
    submit = SubmitField('Submit')

class CreateForm(FlaskForm):
	username = StringField('Enter a username', validators=[DataRequired()])
	password = PasswordField('Enter a password', [DataRequired(), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	submit = SubmitField('Submit')

class SigninForm(FlaskForm):
	username = StringField('Enter your username', validators=[DataRequired()])
	password = PasswordField('Email your password', [DataRequired()])
	submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
	if 'authenticated' not in session or session['authenticated'] == False:
		session['authenticated'] = False
		session['username'] = '-'
	return render_template('index.html', authenticated=session['authenticated'])

@app.route('/leo', methods=['GET', 'POST'])
def leo():
    return render_template('leo.html', authenticated=session['authenticated'])

@app.route('/jack', methods=['GET', 'POST'])
def jack():
    return render_template('jack.html', authenticated=session['authenticated'])

@app.route('/jaafar', methods=['GET', 'POST'])
def jaafar():
    return render_template('jaafar.html', authenticated=session['authenticated'])

@app.route('/create', methods=['GET','POST'])
def create():
	form = CreateForm()
	if form.validate_on_submit():
		error = None
		user = User(username = form.username.data, password = form.password.data)
		check_user = User().query.filter_by(username = form.username.data).first()
		if check_user is not None:
			error = 'Account Already Exists!'
			return render_template('create.html', create_form = form, authenticated=session['authenticated'], error=error)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('create.html', create_form = form, authenticated=session['authenticated'])

@app.route('/signin', methods=['GET','POST'])
def signin():
	form = SigninForm()
	error = None
	if form.validate_on_submit():
		check_user = User().query.filter_by(username = form.username.data).first()
		if check_user is not None and check_user.password == form.password.data:
			session['authenticated'] = True
			session['username'] = form.username.data
			return redirect(url_for('contact'))
		elif check_user is None:
			error = 'Username Does Not Exist!'
			return render_template('signin.html', signin_form=form, authenticated=session['authenticated'], error=error)

		else:
			error = 'Password Incorrect!'
			return render_template('signin.html', signin_form=form, authenticated=session['authenticated'], error=error)
	return render_template('signin.html', signin_form=form, authenticated=session['authenticated'])

@app.route('/signout', methods=['GET'])
def signout():
	session['authenticated'] = False
	session['username'] = '-'
	return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	contact = Contact.query.all()
	form = ContactForm()
	contacts = Contact().query.all()
	error = None
	if form.validate_on_submit():
		inputtedname = form.name.data
		inputtedemail = form.email.data
		new_contact = Contact(name = inputtedname, email = inputtedemail, username = session['username'])
		if len(Contact().query.filter(Contact.email==inputtedemail).all()) == 0:
			db.session.add(new_contact)
			db.session.commit()
		else:
			error = 'Email Already Exists!'
			return render_template('contact.html', form = form, contacts = contacts, authenticated=session['authenticated'], username=session['username'], error=error)
		contacts = Contact().query.all()
		form.name.data = ''
		form.email.data = ''
	return render_template('contact.html', form = form, contacts = contacts, authenticated=session['authenticated'], username=session['username'])

@app.route('/delete/<int:contactId>', methods=['GET', 'POST'])
def delete(contactId):
	if session['authenticated'] == True:
		contact = Contact.query.filter_by(id=contactId).first()
		db.session.delete(contact)
		db.session.commit()
		return redirect(url_for('contact'))
	else:
		return redirect(url_for('contact'))

@app.route('/update/<int:contactId>', methods=['GET', 'POST'])
# direct us to a page where we can edit the current (old) string
def edit_page(contactId):
    update_form = UpdateForm()
    if session['authenticated'] == True:
    	if update_form.validate_on_submit():
    		contact = Contact.query.filter_by(id=contactId).first()
    		contact.name = update_form.name.data
    		contact.email = update_form.email.data
    		db.session.commit()
    		return redirect(url_for('contact'))
    	contact = Contact.query.filter_by(id=contactId).first()
    	return render_template('edit.html', update_form=update_form, contact = contact, authenticated=session['authenticated'])
    else:
    	return redirect(url_for('contact'))


from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap 
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'thingxThingYthingZ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'

moment = Moment(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False, unique=False)
	email = db.Column(db.String(200), nullable=False, unique=True)

class ContactForm(FlaskForm):
	name = StringField('Enter your name', validators=[DataRequired()])
	email = EmailField('Email address', [DataRequired(), Email()])
	submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    name = StringField('Edit the name', validators=[DataRequired()])
    email = EmailField('Email address', [DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/leo', methods=['GET', 'POST'])
def leo():
    return render_template('leo.html')

@app.route('/jack', methods=['GET', 'POST'])
def jack():
    return render_template('jack.html')

@app.route('/jaafar', methods=['GET', 'POST'])
def jaafar():
    return render_template('jaafar.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	contact = Contact.query.all()
	form = ContactForm()
	contacts = Contact().query.all()
	if form.validate_on_submit():
		inputtedname = form.name.data
		inputtedemail = form.email.data
		new_contact = Contact(name = inputtedname, email = inputtedemail)
		if len(Contact().query.filter(Contact.email==inputtedemail).all()) == 0:
			db.session.add(new_contact)
			db.session.commit()
		else:
			print("Email already exists")
		contacts = Contact().query.all()
		form.name.data = ''
		form.email.data = ''
	return render_template('contact.html', form = form, contacts = contacts)

@app.route('/delete/<int:contactId>', methods=['GET', 'POST'])
def delete(contactId):
	contact = Contact.query.filter_by(id=contactId).first()
	db.session.delete(contact)
	db.session.commit()
	return redirect(url_for('contact'))

@app.route('/update/<int:contactId>', methods=['GET', 'POST'])
# direct us to a page where we can edit the current (old) string
def edit_page(contactId):
    update_form = UpdateForm()
    if update_form.validate_on_submit():
    	contact = Contact.query.filter_by(id=contactId).first()
    	contact.name = update_form.name.data
    	contact.email = update_form.email.data
    	db.session.commit()
    	return redirect(url_for('contact'))
    contact = Contact.query.filter_by(id=contactId).first()
    return render_template('edit.html', update_form=update_form, contact = contact)


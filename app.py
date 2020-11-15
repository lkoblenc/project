from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap 
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
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
	phone = db.Column(db.String(200), nullable=False, unique=True)

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
	return render_template('contact.html')

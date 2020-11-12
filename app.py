from flask import Flask, render_template, redirect, url_for
from flask_material import Material 
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredients.db'

moment = Moment(app)
material = Material(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def leo():
    return render_template('leo.html')


@app.route('/', methods=['GET', 'POST'])
def jack():
    return render_template('jack.html')


@app.route('/', methods=['GET', 'POST'])
def jaafar():
    return render_template('jaafar.html')


@app.route('/', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

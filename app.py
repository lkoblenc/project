from flask import Flask, render_template, redirect, url_for
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
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

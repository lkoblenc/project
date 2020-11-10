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
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredients.db'

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self):
        return '<Ingredient %r>' % self.id

class IngredientForm(FlaskForm):
    ingredient = StringField('Enter a new ingredient', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    update = StringField('Edit the ingredient', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    ingredient = Ingredients.query.all()
    form = IngredientForm()
    if form.validate_on_submit():
        ingredients = form.ingredient.data
        new_ingredient = Ingredients(ingredient = ingredients)
        db.session.add(new_ingredient)
        db.session.commit()
        ingredient = Ingredients.query.all()
        form.ingredient.data = ''
    return render_template('index.html', form=form, ingredient=ingredient)

@app.route('/delete/<int:ingredientId>', methods=['GET', 'POST'])
def delete(ingredientId):
    ingredient = Ingredients.query.filter_by(id=ingredientId).first()
    db.session.delete(ingredient)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:ingredientId>', methods=['GET', 'POST'])
# direct us to a page where we can edit the current (old) string
def edit_page(ingredientId):
    update_form = UpdateForm()
    if update_form.validate_on_submit():
        ingredient = Ingredients.query.filter_by(id=ingredientId).first()
        ingredient.ingredient = update_form.update.data
        db.session.commit()
        return redirect(url_for('index'))
    ingredient = Ingredients.query.filter_by(id=ingredientId).first()
    return render_template('edit.html', update_form=update_form, ingredient=ingredient.ingredient)

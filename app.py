from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredients.db'

db = SQLAlchemy(app)
migrate = Migrate(app,db)
class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return ' <Name %r>' % self.id
       

bootstrap = Bootstrap(app)
moment = Moment(app)


class IngForm(FlaskForm):
    ing = StringField('Enter your new ingredient', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    if  request.method == "POST":
        ing_name = request.form['ingredient']
        new_ing = Ingredients(ingredient=ing_name)

        try:
             db.session.add(new_ing)
             db.session.commit()
             return redirect('/')
        except:
            return "There was an error adding your ingredient..."
    else:
        ingredients = Ingredients.query.order_by(Ingredients.id)
        return render_template('index.html',ingredients=ingredients)

@app.route('/update/<int:id>',methods=['GET', 'POST'])
def update(id):
    ing_to_update = Ingredients.query.get_or_404(id)
    if request.method == 'POST':
        ing_to_update.ingredient = request.form['ing']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error updating"
    else:
        return render_template('update.html', ing_to_update=ing_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    ing_to_delete = Ingredients.query.get_or_404(id)
    try:
        db.session.delete(ing_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that friend"




from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField
from wtforms.validators import InputRequired,Email,Length
from flask_sqlalchemy import SQLAlchemy
import projects


db = SQLAlchemy()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'AnimeisGOOD'
app.config.from_object('config.Config')
Bootstrap(app)

class LoginForm(FlaskForm):
    username = StringField('username',validators=[InputRequired(), Length(min=4,max=15)])
    password = PasswordField('password',validators=[InputRequired(), Length(min=8,max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'),Length(max=50)])
    username = StringField('username',validators=[InputRequired(), Length(min=4,max=15)])
    password = PasswordField('password',validators=[InputRequired(), Length(min=8,max=80)])
@app.route('/')
def home_route():
    return render_template("home.html", projects=projects.setup())

@app.route('/lowmaint/')
def hello_route():
    return render_template("low_maint.html", projects=projects.setup())

@app.route('/fruitveggie/')
def fruit_route():
    return render_template("fruit_veggie.html", projects=projects.setup())

@app.route('/login/',methods = ['GET','POST'])
def login():
    form = LoginForm()

    return render_template("login.html", form = form, projects=projects.setup())

@app.route('/signup/',methods = ['GET','POST'])
def signup():
    form = RegisterForm()
    return render_template("signup.html", form = form, projects=projects.setup())


if __name__ == "__main__":
    app.run(debug = True, port=8080)
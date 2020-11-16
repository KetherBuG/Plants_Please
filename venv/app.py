from flask import Flask, render_template,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField
from wtforms.validators import InputRequired,Email,Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import projects


app = Flask(__name__)
app.config['SECRET_KEY'] = 'AnimeisGOOD'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(15),unique = True)
    email = db.Column(db.String(50),unique = True)
    password = db.Column(db.String(80))

    def __repr__(self):
        return '<Task %r>' % self.id

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


@app.route('/highmaint/')
def highmaint_route():
    return render_template("high_maint.html", projects=projects.setup())

@app.route('/sdplants/')
def sdplant_route():
    return render_template("SD_plants.html", projects=projects.setup())

@app.route('/fruitveggie/')
def fruit_route():
    return render_template("fruit_veggie.html", projects=projects.setup())

@app.route('/plantpics/')
def plantpictures():
    return render_template("test.html", projects=projects.setup())

#Create the Login Page
@app.route('/login/',methods = ['GET','POST'])
def login():
    #TODO: Make the form accept the User Value, or somehow update the form
    form = LoginForm()
    #TODO Make The SQL Database work

    if form.validate_on_submit():
        #exists = db.session.query(
            #db.session.query(User).filter_by(username='AndrewZhang').exists()
        #).scalar()
        #if exists == True:
            #return "Exists"
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('showboard'))

        return '<h1>Invalid username or password</h1>'

    return render_template("login.html", form = form, projects=projects.setup())

#Create the SignUp Page
@app.route('/signup/',methods = ['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home_route'))


    return render_template("signup.html", form = form, projects=projects.setup())

@app.route('/dashboard/')
def showboard():
    return render_template("DashBoard.html", projects=projects.setup())



if __name__ == "__main__":
    app.run(debug = True, port=8080)
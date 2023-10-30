from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
import os
from models import Role, User

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_generated_secret_key'  # Set the secret key directly

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:nawzad1@localhost/mysql'  # Update this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app

# Define a form using Flask-WTF
class NameForm(FlaskForm):
    name = StringField('Mikä sinun nimesi on?', validators=[DataRequired()])
    submit = SubmitField('Lähetä')

Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # Specify the login view

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # Foreign key to roles

    def __repr__(self):
        return f'<User {self.username}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    user_name = None
    form = NameForm()

    if form.validate_on_submit():
        user_name = form.name.data
        session['user_name'] = user_name

        with app.app_context():
            db.create_all()

        return redirect(url_for('index'))

    user_name = session.get('user_name', None)

    return render_template('index.html', form=form, user_name=user_name)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

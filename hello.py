from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy
import os
from models import Role, User
from app import app, db  # Import 'app' and 'db'

# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = 'your_generated_secret_key'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Define a form using Flask-WTF
class NameForm(FlaskForm):
    name = StringField('Mikä sinun nimesi on?', validators=[DataRequired()])
    submit = SubmitField('Lähetä')

Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

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

        return redirect(url_for('index'))

    user_name = session.get('user_name', None)

    return render_template('index.html', form=form, user_name=user_name)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

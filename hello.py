from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user

# Define a form using Flask-WTF
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_generated_secret_key'  # Set the secret key directly

# Initialize CSRF protection
csrf = CSRFProtect(app)

Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # Specify the login view

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_name = None  # Renamed 'name' to 'user_name'
    form = NameForm()
    
    if form.validate_on_submit():
        user_name = form.name.data  # Updated the variable name
        
        # Store the user_name in the session
        session['user_name'] = user_name
        
        return redirect(url_for('index'))
    
    # Retrieve 'user_name' from the session
    user_name = session.get('user_name', None)
    
    return render_template('index.html', form=form, user_name=user_name)  # Updated the variable name

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
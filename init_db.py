from app import create_app, db
from models import Role, User

# Create and configure the Flask app
app = create_app()  # Replace with how you create your Flask app

# Establish the application context
app_context = app.app_context()
app_context.push()

# Perform your database operations here
admin_role = Role(name='Admin')
db.session.add(admin_role)
db.session.commit()

# Pop the application context to exit the context
app_context.pop()

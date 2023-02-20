from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired,Length,Email


class UserRegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(),Email(),Length(max=50)])
    first_name = StringField("First name", validators=[InputRequired(),Length(max=30)])
    last_name = StringField("Last name", validators=[InputRequired(),Length(max=30)])
    
class UserLoginForm(FlaskForm):
    """Form for user login"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class AddFeedbackForm(FlaskForm):
    """Form for adding new feedback"""

    title = StringField("Title",validators=[InputRequired(),Length(max=100)])
    content = StringField("Content",validators=[InputRequired()])


from secrets import choice
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from condition_monitor.models import DBConnection, User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label="User name", validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label=" Email address:", validators=[Email(),DataRequired()])
    password1 = PasswordField(label = "Password", validators=[Length(min=8),DataRequired()])
    password2 = PasswordField(label = "Confirm Password", validators=[EqualTo("password1"),DataRequired()])
    submit = SubmitField(label = "Create Account")

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class UserAccessForm(FlaskForm):
    #user_ids = [x.id for x in DBConnection.fetchUsers()]
    user = SelectField("User", validators=[DataRequired()], choices = [ x.username for x in DBConnection().fetchUsers()])
    room = SelectField("Room", validators=[DataRequired()], choices = [ x.name for x in DBConnection().fetchRooms()])
    submit = SubmitField("Grant access")
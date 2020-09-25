from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flowgrate.models import User

class SignUpForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
										validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(this, username):

		user = User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError('Sorry, that username is taken :(')

	def validate_email(this, email):

		user = User.query.filter_by(email=email.data).first()

		if user:
			raise ValidationError('Hm, it seems that email already has an account :P')


class SignInForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign in')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
	email = StringField('Email',
                        validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(this, email):

		user = User.query.filter_by(email=email.data).first()

		if user is None:
			raise ValidationError('There is no account linked to that email address :(')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
										validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')
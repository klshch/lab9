from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, EmailField, FileField, ValidationError, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file import FileAllowed

from flask_login import current_user

from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Username:", 
                           validators=[DataRequired("Це поле обовʼязкове")],
                           render_kw={"class": "form-control"})
    
    password = PasswordField("Password:", 
                             validators=[DataRequired("Це поле обовʼязкове"), 
                                         Length(min=4, max=10)],
                                         render_kw={"class": "form-control"})
    
    remember = BooleanField("Remember me", 
                            render_kw={"class": "form-check-input"})

    submit = SubmitField("Sign In", 
                         render_kw={"class": "btn btn-primary"})

    
class ChangePassword(FlaskForm):
    current_password = PasswordField("Current password:", 
                             validators=[DataRequired("Це поле обовʼязкове"), 
                                         Length(min=4, max=10)],
                                         render_kw={"class": "form-control"})
    new_password = PasswordField("New password:", 
                             validators=[DataRequired("Це поле обовʼязкове"), 
                                         Length(min=4, max=10)],
                                         render_kw={"class": "form-control"})
    submit_password = SubmitField("Change Password", 
                         render_kw={"class": "btn btn-primary"})
    

class FeedbackForm(FlaskForm):
    name = StringField("Username:", 
                           validators=[DataRequired("Це поле обовʼязкове")],
                           render_kw={"class": "form-control"})
    content = TextAreaField("Responde:", 
                           validators=[DataRequired("Це поле обовʼязкове")],
                           render_kw={"class": "form-control"})
    submit_feedback = SubmitField("Confirm", 
                         render_kw={"class": "btn btn-primary"})
    
class TodoForm(FlaskForm):
    title = StringField("Enter a task here: ", 
                         validators=[DataRequired("This field is required.")],
                         render_kw={"class": "form-control me-sm-2"})
    submit_todo = SubmitField("Save",
                         render_kw={"class": "btn btn-primary my-2 my-sm-0"})
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired("This field is required."), 
                                       Length(min=4, max=14),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots, or underscores')],
                                       render_kw={"class": "form-control"})
    email = EmailField('Email', 
                       validators=[DataRequired("This field is required."), 
                                   Email("Invalid email.")],
                                   render_kw={"class": "form-control"})
    password =  PasswordField('Password', 
                              validators=[DataRequired("This field is required."), 
                                          Length(min=6)],
                                          render_kw={"class": "form-control"})
    confirm_password =  PasswordField('Confirm password', 
                                      validators=[DataRequired("This field is required."), 
                                                  EqualTo('password', 'Passwords must match.')],
                                                  render_kw={"class": "form-control"})
    
    submit_registration = SubmitField('Register',
                         render_kw={"class": "btn btn-primary"})
    
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already registred')
        
    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Username already in use.')

   
class LoginForms(FlaskForm):
    email = EmailField('Email', 
                       validators=[DataRequired("This field is required."), 
                                   Email("Invalid email.")],
                                   render_kw={"class": "form-control"})
    password = PasswordField('Password', 
                             validators=[DataRequired("This field is required."), 
                                         Length(min=6)],
                                         render_kw={"class": "form-control"})
    remember = BooleanField('Remember me',
                            render_kw={"class": "form-check-input"})
    submit_login = SubmitField("Login",
                         render_kw={"class": "btn btn-primary"})
    

class UpdateAccountForm(FlaskForm):
    username = StringField('Username:', 
                           validators=[Length(min=4, max=14), 
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots, or underscores')],
                                       render_kw={"class": "form-control"})
    email = StringField('Email:', validators=[Email()],
                        render_kw={"class": "form-control"})
    image_file = FileField('Update Profile Image:', 
                           validators=[FileAllowed(['jpg', 'png'])],
                           render_kw={"class": "form-control"})
    about_me = TextAreaField('About Me', 
                             validators=[Length(min=0, max=240)],
                             render_kw={"class": "form-control"})
    last_seen = DateTimeLocalField('Last Seen',
                                   format='%Y-%m-%dT%H:%M',
                                   render_kw={"class": "form-control"})
    submit = SubmitField('Update',
                         render_kw={"class": "btn btn-primary"})            

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registred')
        
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already in use.')
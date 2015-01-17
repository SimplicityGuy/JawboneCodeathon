from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *
from flask.ext.mongoengine.wtf.orm import validators
import models

user_form = model_form(models.User, exclude=["password"])


class SignupForm(user_form):
    password = PasswordField("Password",
                             validators=[validators.Required(),
                                         validators.EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Repeat Password")


class LoginForm(user_form):
    password = PasswordField("Password", validators=[validators.Required()])

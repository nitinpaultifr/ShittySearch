
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, SelectField, RadioField, validators, ValidationError
from models import db

class SearchForm(Form):

    queryfield = TextField("Query", [validators.Required("Please enter the search query")])
    submit = SubmitField("Search")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True

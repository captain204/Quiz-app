from config import *


class Post(Form):
    title = StringField(u'Title',validators=[validators.input_required(),
    validators.Length(min=10,max=250)])
    body = TextAreaField(u'Body',validators=[validators.input_required(),
    validators.Length(min=10,max=2500)])

class User(Form):
    username = StringField(u'Username',validators=[validators.input_required(),
    validators.Length(min=3, max=250)])
    email = StringField(u'email',validators=[validators.input_required(),
    validators.Length(min=3,max=50)])
    password = PasswordField('Password',[validators.DataRequired(),
    validators.EqualTo('confirm',message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    stack = SelectField('Select Stack', choices=[('python', 'python'),('php', 'php'),('javascript', 'javascript'),])

class Add(Form):
    question = TextAreaField(u'Question',validators=[validators.input_required(),
    validators.Length(min=10,max=2500)])
    category = SelectField('Category', choices=[('python', 'python'),('php', 'php'),('javascript', 'javascript'),])
    option_a = StringField(u'Option A',validators=[validators.input_required(),
    validators.Length(min=3,max=250)])
    option_b = StringField(u'Option B',validators=[validators.input_required(),
    validators.Length(min=3,max=250)])
    option_c = StringField(u'Option C',validators=[validators.input_required(),
    validators.Length(min=3,max=250)])
    option_d = StringField(u'Option D',validators=[validators.input_required(),
    validators.Length(min=3,max=250)])
    correct = SelectField('Correct Answer', choices=[('a', 'a'),('b', 'b'),('c', 'c'),('d', 'd'),])
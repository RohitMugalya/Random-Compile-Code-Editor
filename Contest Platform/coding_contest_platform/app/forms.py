from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

# Form for joining the contest
class JoinContestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Join')

# Form for submitting code
class SubmitCodeForm(FlaskForm):
    code = TextAreaField('Code', validators=[DataRequired()])
    language = SelectField('Language', choices=[
        ('python', 'Python3'),
        ('c', 'C'),
        ('cpp', 'C++'),
        ('java', 'Java')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')
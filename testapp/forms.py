from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL)


class AbstractForm(FlaskForm):
    csrf_token = 'test'
    rows = StringField('Бажаний розмір (кількість речень)', [
        DataRequired()])
    body = TextAreaField('Текст', [
        DataRequired(),
        Length(min=4, message='Текст дуже короткий')])
    language = SelectField(
        'Мова',
        choices=[('ukrainian', 'Українська'), ('russian', 'Російська')]
    )
    submit = SubmitField('Реферат!')
    result = ''
    cosine = 0
    

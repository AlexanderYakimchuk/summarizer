from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     SelectField)
from wtforms.validators import (DataRequired,
                                Length)

from testapp.config import Lang


class AbstractForm(FlaskForm):
    csrf_token = 'test'
    rows = StringField('Бажаний розмір (кількість речень)', [
        DataRequired()])
    body = TextAreaField('Текст', [
        DataRequired(),
        Length(min=4, message='Текст дуже короткий')])
    language = SelectField(
        'Мова',
        choices=[(Lang.UA.value, 'Українська'), (Lang.RU.value, 'Російська')]
    )
    submit = SubmitField('Реферат!')
    result = ''
    cosine = 0

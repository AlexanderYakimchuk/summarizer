from flask import Flask, url_for, render_template, redirect
from .forms import AbstractForm
from .summarizers.general import summarize
from .measures import get_cosine, text_to_vector
import os
from .config import Config, Lang

SECRET_KEY = os.urandom(32)

app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config)
app.config['RECAPTCHA_PUBLIC_KEY'] = 'iubhiukfgjbkhfvgkdfm'
app.config['RECAPTCHA_PARAMETERS'] = {'size': '100%'}
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=('GET', 'POST'))
def home():
    form = AbstractForm()
    if form.is_submitted():
        form.result = summarize(
            form.body.data, Lang(form.language.data), int(form.rows.data))
        form.cosine = get_cosine(text_to_vector(
            form.body.data), text_to_vector(form.result))
        return render_template('abstract.html',
                               form=form,
                               template='form-template')
    return render_template('abstract.html',
                           form=form,
                           template='form-template')

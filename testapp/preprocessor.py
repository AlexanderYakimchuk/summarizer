# Инициализация всего необходимого для предобработки
from functools import lru_cache
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.tokenize import RegexpTokenizer
import csv
import io

from testapp.config import Lang


@lru_cache(maxsize=None)
def get_stop_words(language: Lang):
    stopwords = []
    dir = 'data/help'
    filenames = {
        Lang.UA: 'stop_words_ua.csv',
        Lang.RU: 'stop_words_ru.csv',
    }
    path = f"{dir}/{filenames[language]}"
    with io.open(path, 'r', encoding="utf-8") as file:
        for row in csv.reader(file):
            stopwords.append(row[0])
    return stopwords


def get_abbreviation(language: Lang):
    if language == 'ukrainian':
        return ['тис', 'грн', 'т.я', 'вул', 'cек', 'хв', 'обл', 'кв', 'пл',
                'напр', 'гл', 'і.о', 'зам']
    return ['тыс', 'руб', 'т.е', 'ул', 'д', 'сек', 'мин', 'т.к', 'т.н', 'т.о',
            'ср', 'обл', 'кв', 'пл',
            'напр', 'гл', 'и.о', 'им', 'зам', 'гл', 'т.ч']


@lru_cache(maxsize=None)
def get_tokenizer(language: Lang):
    punkt_param = PunktParameters()
    abbreviation = get_abbreviation(language.value)
    punkt_param.abbrev_types = set(abbreviation)
    sent_tokenizer = PunktSentenceTokenizer(punkt_param).tokenize
    return sent_tokenizer


word_tokenizer = RegexpTokenizer(r'\w+')

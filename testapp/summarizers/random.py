import random

from ..config import Lang
from ..preprocessor import get_tokenizer


def summarize(text, language: Lang, n):
    sent_tokenizer = get_tokenizer(language)
    sentences = sent_tokenizer(text)
    ratings = list(range(len(sentences)))
    random.shuffle(ratings)
    rand_sent = sorted((r, s) for r, s in zip(ratings, sentences))
    sent_n = rand_sent[:n]
    return ' '.join(s[1] for s in sent_n)

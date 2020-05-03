import random
from TextPreprocessor import sent_tokenizer_ru, sent_tokenizer_ua


def summarize(text, language, n):
    sent_tokenizer = sent_tokenizer_ru
    if language == 'ukrainian':
        sent_tokenizer = sent_tokenizer_ua
    sentences = sent_tokenizer(text)
    ratings = list(range(len(sentences)))
    random.shuffle(ratings)
    rand_sent = sorted((r, s) for r, s in zip(ratings, sentences))
    sent_n = rand_sent[:n]
    return ' '.join(s[1] for s in sent_n)

from itertools import combinations
from pymorphy2 import MorphAnalyzer

from ..config import Lang
from ..preprocessor import word_tokenizer, get_tokenizer, get_stop_words
import math
from ..text_graph import rank_graph


def similarity(s1, s2):
    if not len(s1) or not len(s2):
        return 0.0
    return len(s1.intersection(s2)) / (
            math.log(len(s1) + 1) + math.log(len(s2) + 1))


def text_rank(text, language: Lang):
    tokenizer = get_tokenizer(language)
    morph = MorphAnalyzer(lang=language.value)
    sentences = tokenizer(text)
    if len(sentences) < 2:
        s = sentences[0]
        return [(1, 0, s)]
    words = [set(morph.parse(word)[0].normalized for word in
                 word_tokenizer.tokenize(sentence.lower())
                 if word not in get_stop_words(language)) for sentence in
             sentences]

    pairs = combinations(range(len(sentences)), 2)
    scores = [(i, j, similarity(words[i], words[j])) for i, j in pairs]
    scores = filter(lambda x: x[2], scores)
    pr = rank_graph(scores)

    return sorted(((i, pr[i], s) for i, s in enumerate(sentences) if i in pr),
                  key=lambda x: pr[x[0]], reverse=True)


def summarize(text, language, n=5):
    tr = text_rank(text, language)
    top_n = sorted(tr[:n])
    return ' '.join(x[2] for x in top_n)

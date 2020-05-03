from numpy import dot
from numpy.linalg import norm
from testapp.measures import tfidf, get_cosine, text_to_vector
from . import lsa
from .text_rank import text_rank


def similarity(s1, s2):
    n1 = norm(s1)
    n2 = norm(s2)
    if not n1 or not n2:
        return 0.0
    return dot(s1, s2) / (n1 * n2)


def summarize(text, language, n=5):
    tr = text_rank(text, language)
    top_n = sorted(tr[:n])
    text_rank_result = ' '.join(x[2] for x in top_n)
    lsa_result = lsa.summarize(text, language, n)
    cosine_text_rank = get_cosine(text_to_vector(text),
                                  text_to_vector(text_rank_result))
    cosine_lsa = get_cosine(text_to_vector(text), text_to_vector(lsa_result))
    if cosine_lsa > cosine_text_rank:
        return lsa_result
    return text_rank_result

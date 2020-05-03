import re
import math
from pymorphy2 import MorphAnalyzer
from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF, IDF

from .preprocessor import word_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter


class StemTokenizer:
    def __init__(self, language):
        self.morph = MorphAnalyzer()
        if language == 'ukrainian':
            self.morph = MorphAnalyzer(lang='uk')

    def __call__(self, doc):
        return [self.morph.parse(t)[0].normalized for t in
                word_tokenizer.tokenize(doc.lower())]


WORD = re.compile(r'\w+')


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def tfidf(text, language, sentences, stop_words):
    tfidf = TfidfVectorizer(ngram_range=(
        1, 1), stop_words=stop_words,
        tokenizer=StemTokenizer(language)).fit_transform(sentences)
    a = tfidf.toarray()
    return a


def spark_tfidf():
    sc = SparkContext(appName="TFIDFExample")  # SparkContext

    # $example on$
    # Load documents (one per line).
    documents = sc.textFile("testapp/data/input/test.txt").map(
        lambda line: line.split(" "))


    hashingTF = HashingTF()
    tf = hashingTF.transform(documents)

    # While applying HashingTF only needs a single pass to the data, applying IDF needs two passes:
    # First to compute the IDF vector and second to scale the term frequencies by IDF.
    tf.cache()
    idf = IDF().fit(tf)
    tfidf = idf.transform(tf)

    # spark.mllib's IDF implementation provides an option for ignoring terms
    # which occur in less than a minimum number of documents.
    # In such cases, the IDF for these terms is set to 0.
    # This feature can be used by passing the minDocFreq value to the IDF constructor.
    idfIgnore = IDF(minDocFreq=2).fit(tf)
    tfidfIgnore = idfIgnore.transform(tf)
    # $example off$

    print("tfidf:")
    for each in tfidf.collect():
        print(each)

    print("tfidfIgnore:")
    for each in tfidfIgnore.collect():
        print(each)

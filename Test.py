import GeneralSummarizer
import LSASummarizer
import TextRankSummarizer
import feedparser
import csv
import re
import io
from TextPreprocessor import sent_tokenizer_ru, word_tokenizer, stop_words_ru, \
    sent_tokenizer_ua, stop_words_ua
from VectorMeasuresCalculator import tfidf, get_cosine, text_to_vector


def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data).replace('\n', ' ')


def test(language):
    filename = 'RU_dataset.csv'
    if language == 'ukrainian':
        filename = 'UA_dataset_full.csv'
    testData = []

    with io.open(filename, 'r', encoding="utf-8") as file:
        for row in csv.reader(file):
            testData.append({"id": row[0], "title": row[1], "text": row[2]})

    row_list = [["Id", "Title", "Body", "Summary20",
                 "Cosine20", "Summary40", "Cosine40"]]
    for testDataRow in testData:
        testedText = testDataRow["text"]
        result20 = ''
        result40 = ''
        if language == 'ukrainian':
            sentences = sent_tokenizer_ua(testedText)
            if len(sentences) < 10:
                result20 = GeneralSummarizer.summarize(testedText, language, 2)
                if (len(sentences) < 5):
                    result40 = GeneralSummarizer.summarize(testedText, language,
                                                           2)
                else:
                    result40 = GeneralSummarizer.summarize(
                        testedText, language, 4)
            elif len(sentences) < 20:
                result20 = GeneralSummarizer.summarize(testedText, language, 4)
                result40 = GeneralSummarizer.summarize(testedText, language, 8)
            else:
                result20 = GeneralSummarizer.summarize(
                    testedText, language, len(sentences) // 5)
                result40 = GeneralSummarizer.summarize(
                    testedText, language, len(sentences) // 3)
        else:
            sentences = sent_tokenizer_ru(testedText)
            if len(sentences) < 10:
                result20 = GeneralSummarizer.summarize(testedText, language, 2)
                if (len(sentences) < 5):
                    result40 = GeneralSummarizer.summarize(
                        testedText, language, 2)
                else:
                    result40 = GeneralSummarizer.summarize(
                        testedText, language, 4)
            elif len(sentences) < 20:
                result20 = GeneralSummarizer.summarize(testedText, language, 4)
                result40 = GeneralSummarizer.summarize(testedText, language, 8)
            else:
                result20 = GeneralSummarizer.summarize(
                    testedText, language, len(sentences) // 5)
                result40 = GeneralSummarizer.summarize(
                    testedText, language, len(sentences) // 3)

        cosine20 = get_cosine(text_to_vector(
            result20), text_to_vector(testedText))
        cosine40 = get_cosine(text_to_vector(
            result40), text_to_vector(testedText))
        testDataRow["result20"] = result20
        testDataRow["result40"] = result40
        row_list.append(
            [testDataRow["id"], testDataRow["title"], testDataRow["text"],
             testDataRow["result20"], str(cosine20), testDataRow["result40"],
             str(cosine40)])

    with io.open('result' + filename, 'w', newline='',
                 encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerows(row_list)


test('ukrainian')
# test('russian')

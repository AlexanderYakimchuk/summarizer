import GeneralSummarizer
import LSASummarizer
import TextRankSummarizer
import feedparser
import csv
import re
import io
from TextPreprocessor import sent_tokenizer_ru, word_tokenizer, stop_words_ru, sent_tokenizer_ua, stop_words_ua

def remove_html_tags(data):
  p = re.compile(r'<.*?>')
  return p.sub('', data).replace('\n', ' ')


def test(language):
    filename = 'ru_gazeta.csv'
    if language == 'ukrainian':
        filename = 'ua_gazeta.csv'
    testData = []

    with io.open(filename, 'r', encoding="utf-8") as file:
        for row in csv.reader(file):
            testData.append({"id": row[0], "title": row[1], "text": row[2]})

    row_list = [["Id", "Title", "Body", "Summary"]]
    for testDataRow in testData:
        testedText = testDataRow["text"]
        result = ''
        if language == 'ukrainian':
            sentences = sent_tokenizer_ua(testedText)
            if len(sentences) < 20:
                result = GeneralSummarizer.summarize(testedText, language, 2)
            else:
                result = GeneralSummarizer.summarize(
                    testedText, language, len(sentences) // 10)
        else:
            sentences = sent_tokenizer_ru(testedText)
            if len(sentences) < 20:
                result = GeneralSummarizer.summarize(testedText, language, 2)
            else:
                result = GeneralSummarizer.summarize(
                    testedText, language, len(sentences) // 10)
        testDataRow["result"] = result
        row_list.append(
            [testDataRow["id"], testDataRow["title"], testDataRow["text"], testDataRow["result"]])

    with io.open('result'+filename, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerows(row_list)


test('ukrainian')

from testapp.config import Lang
from testapp.summarizers.general import summarize
import csv
import re
import io
from testapp.preprocessor import get_tokenizer


def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data).replace('\n', ' ')


def test(language: Lang):
    dir = 'data/input'
    filenames = {
        Lang.UA: 'ua_gazeta.csv',
        Lang.RU: 'ru_gazeta.csv',
    }
    filename = filenames[language]
    path = '/'.join((dir, filename))
    test_data = []

    with io.open(path, 'r', encoding="utf-8") as file:
        for row in csv.reader(file):
            test_data.append({"id": row[0], "title": row[1], "text": row[2]})

    row_list = [["Id", "Title", "Body", "Summary"]]
    for row in test_data:
        tested_text = row["text"]

        tokenizer = get_tokenizer(language)
        sentences = tokenizer(tested_text)
        if len(sentences) < 20:
            result = summarize(tested_text, language, 2)
        else:
            result = summarize(tested_text, language, len(sentences) // 10)

        row["result"] = result
        row_list.append([row["id"], row["title"], row["text"], row["result"]])

    with io.open(f'data/result/{filename}', 'w', newline='',
                 encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerows(row_list)


if __name__ == "__main__":
    test(Lang.RU)

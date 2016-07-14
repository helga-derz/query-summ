import re

FINAL_PUNCT = '!.?'

RUS_ALF_CAP = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
RUS_ALF = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

ENG_ALF_CAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ENG_ALF = 'abcdefghijklmnopqrstuvwxyz'


def split_word(text):
    return re.findall('\w+-*\w', text)


def split_sentence(text):
    lt_sent = []
    cursor = 0

    for ind, symbol in enumerate(text):
        if len(text)-1 > ind > cursor:
            if symbol in FINAL_PUNCT:
                lt_sent.append(text[cursor:ind+1])
                cursor = ind+1 if text[ind+1] in ' \n\t' else ind   # if we have space between sentences or not
        elif ind > cursor:
            lt_sent.append(text[cursor:])

    return lt_sent


def split_paragraph(text):
    if '\n' in text:
        paragraphs = filter(None, text.split('\n'))
        return list(paragraphs)
    else:
        return False

text = 'Приве-т!\n\nЯ ждала тебя...'

print(split_sentence(text))
print(split_paragraph(text))
print(split_word(text))

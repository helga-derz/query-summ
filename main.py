import re

FINAL_PUNCT = '!.?'

RUS_ALF_CAP = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
RUS_ALF = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

ENG_ALF_CAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ENG_ALF = 'abcdefghijklmnopqrstuvwxyz'


def split_word(text):
    return re.findall('\w+', text)


def split_sentence(text):
    lt_sent = []
    cursor = 0

    for ind, symbol in enumerate(text):
        if ind < len(text)-1:
            if symbol in FINAL_PUNCT:
                print('+')
                lt_sent.append(text[cursor:ind+1])
                cursor = ind+1
        else:
            lt_sent.append(text[cursor:])

    return lt_sent


def split_paragraph(text):
    if '\n' in text:
        return re.findall('\n+', text)
    else:
        return False

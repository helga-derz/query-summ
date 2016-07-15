import re

FINAL_PUNCT = '!.?'

RUS_ALF_CAP = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
RUS_ALF = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

ENG_ALF_CAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ENG_ALF = 'abcdefghijklmnopqrstuvwxyz'


def split_word(text):
    return re.findall('\w+-*\w*-*\w*', text)  # finding words which may include one or two hyphens


def split_sentence(text):
    lt_sent = []
    cursor = 0

    for ind, symbol in enumerate(text):
        if len(text) - 1 > ind > cursor:
            if symbol in FINAL_PUNCT:
                lt_sent.append(text[cursor:ind + 1])
                cursor = ind + 1 if text[ind + 1] in ' \n\t' else ind  # if we have space between sentences or not
        elif ind > cursor:
            lt_sent.append(text[cursor:])

    return lt_sent


def split_sent(text):
    lt_sent = []  # list of sentences
    lt_punct = []  # indexes of each period
    curr_period = [0, 0]  # contains current pack of final punctuation
    EDGE = False

    for ind, symbol in enumerate(text):
        if not EDGE:
            if symbol in FINAL_PUNCT:
                EDGE = True
                curr_period[0] = ind
        else:
            if symbol.isalpha():
                if curr_period[1] == 0:
                    curr_period[0] = ind-1
                else:
                    curr_period[1] = ind-1
                EDGE = False
                lt_punct.append(curr_period)
                curr_period = [0, 0]

            elif symbol.isspace():
                curr_period[1] = ind
            elif symbol in FINAL_PUNCT:
                curr_period[0] = ind

    cursor = 0
    for edge in lt_punct:
        lt_sent.append(text[cursor:edge[0]+1])
        cursor = edge[1] + 1
    lt_sent.append(text[cursor:])

    return lt_sent


def split_paragraph(text):
    if '\n' in text:
        paragraphs = filter(None, text.split('\n'))
        return list(paragraphs)
    else:
        return False


text = 'При-в-ет!!\n\n Я ждала тебя...'

print(split_sent(text))
print(split_paragraph(text))
print(split_word(text))

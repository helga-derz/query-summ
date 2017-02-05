# -*- coding: utf-8 -*-
import re
import pymorphy2
import math


morph = pymorphy2.MorphAnalyzer()

FINAL_PUNCT = '!.?'

RUS_ALF_CAP = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
RUS_ALF = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

ENG_ALF_CAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ENG_ALF = 'abcdefghijklmnopqrstuvwxyz'

conj = open('stuff/conjunctions/all.txt', 'r', encoding='utf-8').read().split('\n')
interj = open('stuff/interjections.txt', 'r', encoding='utf-8').read().split('\n')
particles = open('stuff/particles.txt', 'r', encoding='utf-8').read().split('\n')
prepos = open('stuff/prepositions.txt', 'r', encoding='utf-8').read().split('\n')


def normalize(words):

    norm_words = []
    for word in words:
        parse = morph.parse(word)[0]
        norm_words.append(parse.normal_form)

    return norm_words


def split_word(text):
    all_words = re.findall('\w+-*\w*-*\w*', text)  # finding words which may include one or two hyphens
    return all_words


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
    cursor = 0

    for edge in remove_edges_with_names(text):
        lt_sent.append(text[cursor:edge[0]+1])
        cursor = edge[1] + 1
    lt_sent.append(text[cursor:])

    return lt_sent


def make_edges(text):
    lt_punct = []  # indexes of each period
    curr_period = [0, 0]  # contains current pack of final punctuation
    EDGE = False

    quotes = 0

    for ind, symbol in enumerate(text):
        quotes += 1 if symbol in "»«\"" else 0
        if not EDGE and symbol in FINAL_PUNCT:
            EDGE = True
            curr_period[0] = ind
        elif EDGE:
            if symbol.isalnum() or (symbol in "»«\"" and quotes % 2 != 0):
                if curr_period[1] == 0:
                    curr_period[0] = ind-1
                else:
                    curr_period[1] = ind-1
                EDGE = False
                lt_punct.append(curr_period)
                curr_period = [0, 0]
            elif symbol.isspace():
                curr_period[1] = ind      # we clean sentences from useless whitespaces (these indexes will be missed)
            elif symbol in FINAL_PUNCT or (symbol in "»«\"" and quotes % 2 == 0):
                curr_period[0] = ind      # in case we have lots of final punct (like "!!!!!")

    return lt_punct


def find_names(text):

    name_edges = []
    name = re.compile('[А-Я]\.\s?[А-Я]?\.?\s?[А-Я][а-я]+')
    iterator = name.finditer(text)

    for match in iterator:
        name_edges.append(match.span())

#    print(len(name_edges))

    return name_edges


def remove_edges_with_names(text):

    name_edges = find_names(text)
    fake_edges = []
    edges = make_edges(text)

    for edge in edges:
        for name in name_edges:
            if name[1] > edge[0] > name[0]:
                fake_edges.append(edge)

    for edge in fake_edges:
        edges.remove(edge)

    return edges


def split_paragraph(text):
    if '\n' in text:
        paragraphs = filter(None, text.split('\n'))
        return list(paragraphs)
    else:
        return text


def remove_auxiliary(lt_words):

    text = ' '.join(lt_words)
    stops = conj + interj + particles + prepos
    for word in stops:
        trash = ' ' + word + ' '
        if trash in text:
            text = text.replace(trash, ' ')

    clean_words = filter(None, text.split(' '))

    return list(clean_words)


def complex_split_text(text):  # создает массивы с распарсенным текстом на трёх уровнях

    bag = []
    paragraphs = split_paragraph(text)

    for paragraph in paragraphs:
        bag_sent = []
        sents = split_sent(paragraph)

        for sent in sents:
            words = split_word(sent)
            bag_sent.append(words)

        bag.append(bag_sent)

    return bag


def word_freq(texts):  # возвращает словарь с частотами нормализованных слов
    word_coll = []

    for text in texts:
        words = normalize(list(set(split_word(text))))
        word_coll.extend(words)

    dic = {}

    for word in word_coll:
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1

    return dic


def idf(word, texts):      # тексты в виде списка слов
    n = 0
    for text in texts:
        if word in text:
            n += 1
    return math.log(len(texts)/n, 10)


def tf(word, text):     # текст в виде списка слов
    return text.count(word)/len(text)


texts = []
norm_texts = []

for i in range(0, 5):
    texts.append(open("texts/sport_"+str(i)+".txt", 'r', encoding='utf-8').read())

for text in texts:
    norm_texts.append(normalize(split_word(text)))

dic = word_freq(texts)

dic_idf = {}

for word in dic.keys():
    dic_idf[word] = idf(word, norm_texts)

print(dic_idf)

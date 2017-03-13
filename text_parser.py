# -*- coding: utf-8 -*-
import re
import pymorphy2
import math
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.stem.snowball import RussianStemmer
from itertools import combinations


morph = pymorphy2.MorphAnalyzer()
lmtzr = RussianStemmer()


def normalize(words):

    norm_words = []
    for word in words:
        parse = morph.parse(word)[0]
        norm_words.append(parse.normal_form)

    return [w.lower() for w in norm_words]


def split_word(text):
    all_words = re.findall('\w+-*\w*-*\w*', text)  # finding words which may include one or two hyphens
    return all_words


def split_paragraph(text):
    if '\n' in text:
        paragraphs = filter(None, text.split('\n'))
        return list(paragraphs)
    else:
        return text


def count_idf(word, texts):   # тексты в виде списка слов
    n = 0
    for text in texts:
        if word in text:
            n += 1
    if n == 1:
        return 0
    else:
        return math.log(len(texts)/n, 10)


def tf(word, text):     # текст в виде списка слов
    return text.count(word)/len(text)


def form_dic_idf_from_file():   # формирует список idf из подготовленного файла
    f = open('idfs.txt', 'r', encoding='utf-8').read()
    dic_idf = {}
    for line in f.split('\n'):
        dic_idf[line.split(' ')[0]] = float(line.split(' ')[1])
    return dic_idf


def count_idf_sent(sent, file_idfs, new_idfs):  # считает idf предложения (сначала idf из файла, потом - из текста)

    words = normalize(split_word(sent))
    idf_s = 0
    for word in words:
        if word in file_idfs:
            idf_s += file_idfs[word]
        else:
            idf_s += new_idfs[word]

    return idf_s/len(words)


def delete_tags(text):
    expr_tag1 = re.compile('<[^>/]+>')  # открывающий тег
    expr_tag2 = re.compile('</[^>]+>')  # закрывающий тег
    text = re.sub(expr_tag1, '', text)
    text = re.sub(expr_tag2, '.', text)
    text = re.sub('\.\.', '.', text)  # после удаления тегов могли появиться лишние точки
    text = re.sub('[ \t]{2,}', '', text)  # удаляет лишние whitespaces
    return text


def prepare_text(text):
    text = delete_tags(text)               # чистим текст от html
    words = normalize(split_word(text))    # создаём список нормализованных слов
    sents = sent_tokenize(text)            # делим текст на предложения
    parags = split_paragraph(text)         # делим на параграфы
    return words, sents, parags


def count_idfs_text(words, sents):

    idfs_words = {}
    text_lt = [words]                      # считаем idf слов анализируемого текста
    for word in words:                     # считаем idf так, будто у нас НЕТ таких слов в заготовленных текстах
        idfs_words[word] = count_idf(word, text_lt)

    idfs_sent = {}
    for sent in sents:                     # считаем idf слов анализируемого текста
        idfs_sent[sent] = count_idf_sent(sent, dic_idf, idfs_words)

    return idfs_words, idfs_sent


def make_vectors(bag_words, sents):
    vectors = []
    for sent in sents:
        vector = []
        sent = [lmtzr.stem(word) for word in split_word(sent)]
        for word in bag_words:
            vector.append(sent.count(word))
        vectors.append(vector)
    return vectors


def define_position_sent(parags):                 # формирует словарь с номером абзаца для каждого предложения

    dic_sent_posit = {}
    n = 1
    for parag in parags:
        sents = sent_tokenize(parag)
        for sent in sents:
            dic_sent_posit[sent] = n
        n += 1

    return dic_sent_posit


def cosine_distance(a, b):
    if len(a) != len(b):
        return False
    numerator = 0
    denoma = 0
    denomb = 0
    for i in range(len(a)):
        numerator += a[i]*b[i]
        denoma += abs(a[i])**2
        denomb += abs(b[i])**2
    result = abs(round(1 - numerator / (math.sqrt(denoma)*math.sqrt(denomb)), 3))
    return result


def make_bag_words(texts):
    bag = []
    for text in texts:
        words = [lmtzr.stem(word) for word in split_word(text)]
        bag.extend(words)
    return list(set(bag))


def compare(bag_sents_vectors):
    matrixx = []

    for sent in bag_sents_vectors:
        t = []
        for sent1 in bag_sents_vectors:
            t.append(cosine_distance(sent, sent1))
        matrixx.append(t)
    return matrixx


def delete_same_sents(matrixx):
    n = len(matrixx)
    dlt = []
    final = []
    for strk in range(len(matrixx)):
        if strk not in dlt:
            for stl in range(n):
                if matrixx[strk][stl] <= 0.8:
                    dlt.append(stl)
            n -= 1
            final.append(strk)
    return final


def delete_useless_sents(bag_sents):
    new_bag = []
    for sent in bag_sents:
        if len(split_word(sent)) > 4:
            new_bag.append(sent)
    return new_bag

#   НАЧАЛО

dic_idf = form_dic_idf_from_file()    # создаем словарь idf уже готовых текстов
texts_big_letters = []
texts = []

for f in range(0, 7):
    text = open('train/feed0/text' + str(f) + '.txt', 'r', encoding='utf-8')
    text.readline()
    text.readline()
    text.readline()
    text = text.read()
    texts_big_letters.append(text)
    texts.append(text.lower())


vectors = []   # каждый текст будет представлен в виде вектора
posits = []
bag_words = make_bag_words(texts)   # список слов во всех текстах (стемминг, удаление повторений)
texts_vectors = []
bag_sents = []
bag_sents_vectors = []

r_s = []

for text in texts:
    words, sents, parags = prepare_text(text)     # слова, предложения, абзацы
    idfs_words, idfs_sent = count_idfs_text(words, sents)
    filtered_sents = delete_useless_sents(sents)   # удаляем из списка предложений ненужные
    bag_sents.extend(filtered_sents)

    r_s.extend(sents)

    posits.append(define_position_sent(parags))             # позиции предложений в тексте

    sent_vectors = make_vectors(bag_words, filtered_sents)
    texts_vectors.append(sent_vectors)                      # тексты в виде предложений-векторов
    bag_sents_vectors.extend(sent_vectors)


#print(list(set(r_s).difference(bag_sents)))
for i in delete_same_sents(compare(bag_sents_vectors)):
    print(bag_sents[i])












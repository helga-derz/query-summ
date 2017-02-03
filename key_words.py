# -*- coding: utf-8 -*-
import pymorphy2
import math

morph = pymorphy2.MorphAnalyzer()


def normalize(words):

    norm_words = []
    for word in words:
        parse = morph.parse(word)[0]
        norm_words.append(parse.normal_form)

    return norm_words


def make_bag_of_words(words):

    bag = {}
    for word in words:
        if word in bag:
            bag[word] += 1      # make a dictionary of all words in text
        else:
            bag[word] = 1

    return bag


def define_key_words(lt_words, key_numb):

    bag = make_bag_of_words(normalize(lt_words))

    key_words = []

    words = []
    freq = []

    for word in bag.keys():
        words.append(word)    # turn the dict into two lists
        freq.append(bag[word])

    for i in range(key_numb):
        max_freq_ind = freq.index(max(freq))
        key_words.append(words.pop(max_freq_ind))
        freq.pop(max_freq_ind)

    return key_words


def idf(word, texts):      # тексты в виде списка слов
    n = 0
    for text in texts:
        if word in text:
            n += 1
    return math.log(len(texts)/n, 10)


def tf(word, text):     # текст в виде списка слов
    return text.count(word)/len(text)


# def tf-idf()

'''
words = ['трое', 'троих', 'тремя', 'один']
print(define_key_words(words, 1))
'''
# -*- coding: utf-8 -*-
import pymorphy2
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


def define_key_words(lt_words, key_numb):  # it needs a dictionary

    bag = make_bag_of_words(lt_words)

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


words = ['один', 'одна', 'одному', 'одной', 'три']
print(normalize(words))

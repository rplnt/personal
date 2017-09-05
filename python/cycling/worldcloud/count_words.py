#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from collections import defaultdict
import sys


def read_file(filename, stopwords=None):
    db = defaultdict(int)
    with open(filename, 'r') as f:
        for line in f:
            line = line.replace(']', ' ')
            words = line.split()
            for word in words:
                word = word.strip('!?.,:()\'"\\/-')
                if len(word) < 4 or len(word) > 20:
                    continue
                if stopwords and word.lower() in stopwords:
                    continue
                if word.startswith('http'):
                    continue
                db[word] += 1

    print('Found {} words.'.format(len(db)))
    return db


def remove_duplicates(words):
    precount = len(words)
    for word in words.keys():
        lword = word.lower()
        if word != lword:
            if lword in words:
                # if abs(words[word] - words[lword]) < 2:
                    # print('{}: {} | {}: {}'.format(word, words[word], lword, words[lword]))
                if words[word] > words[lword]:
                    words[word] += words[lword]
                    del words[lword]
                else:
                    words[lword] += words[word]
                    del words[word]

    print('Removed {} duplicate words'.format(precount - len(words)))
    return words


def remove_singles(words, min_count=1):
    precount = len(words)
    for word, count in words.items():
        if count <= min_count:
            del words[word]

    print('Removed {} single words'.format(precount - len(words)))
    return words


def print_words(words):
    for word in sorted(words, key=words.get, reverse=True):
        # uword = unicode(word).encode('utf8')
        print('{} {}'.format(words[word], word))


def save_words(words):
    with open('words.txt', 'w') as f:
        for word in sorted(words, key=words.get, reverse=True):
            f.write('{} {}'.format(words[word], word))


def wordcloud():
    stopwords = read_file('stopwords.txt')
    words = read_file(sys.argv[1], stopwords)
    words = remove_duplicates(words)
    words = remove_singles(words, 2)
    print_words(words)


if __name__ == '__main__':
    wordcloud()

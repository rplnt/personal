#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''BullsAndCows game.'''

from __future__ import print_function

import argparse
import random
import sys
import os
import re

__author__ = "Matej Buday"


#  raw_input -> input for python 2
try:
    input = raw_input
except NameError:
    pass


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--difficulty', type=int, metavar='(3-9)', default=4, choices=range(3, 10),
                        help='set how many digits will the guessing number have')
    parser.add_argument('-n', '--no-leading-zero', dest='leading_zero', action='store_false',
                        help='when generating a random number, 0 won\'t be a lead digit')
    parser.add_argument('-w', '--words', dest='word_file', metavar='FILE',
                        help='file containg words to choose from - one per line, no repeating characters')
                        # eg: `cat /usr/dict/words | grep -P '^(?:([a-z])(?!.*?\1)){5}$'` for 5-char words

    args = parser.parse_args()

    if args.word_file and not os.path.isfile(args.word_file):
        parser.exit('Not a file: "{}"'.format(args.word_file))

    return args


class BullsAndCows(object):
    score_strings = ['unbelievably well', 'awesome', 'pretty good', 'all right', 'mediocre', 'real bad']

    def __init__(self, difficulty=None, leading_zero=None, word_file=None):
        # switch to "word" mode if word file is provided and ignore other options
        if word_file:
            self.word_file = word_file
            self.generate_secret = self._pick_word
            self.validate_guess = self._validate_word
            self.scoring_base = 2.4
            return

        self.difficulty = difficulty
        self.leading_zero = leading_zero
        self.generate_secret = self._generate_number
        self.validate_guess = self._validate_number
        self.scoring_base = 1.2

    def play(self):
        print('Let\'s play Bulls and Cows!')
        self.generate_secret()
        print('(Submit empty answer to exit)')
        attempts = self._game_loop()

        if not attempts:
            return

        # only works for numbers as words could be anything from list of weekdays to random strings
        score = int(max(attempts - len(self.secret), 0) / (1.2 * len(self.secret)))
        print('You did {}'.format(self.score_strings[min(5, score)]))

    def _game_loop(self):
        attempts = 0
        while True:
            print('Enter a guess:')
            raw_guess = input('>>> ')

            # exit
            if len(raw_guess) == 0:
                break

            guess = self.validate_guess(raw_guess)
            if not guess:
                continue

            attempts += 1
            bulls, cows = self._score_guess(guess)
            if bulls == len(self.secret):
                print('Correct, you\'ve guessed the right answer in {} guesses!'.format(attempts))
                return attempts

            print('{} bulls, {} cows'.format(bulls, cows))

    def _score_guess(self, guess):
        bulls = sum([s == g for s, g in zip(self.secret, guess)])
        cows = len(set(self.secret).intersection(guess)) - bulls

        return bulls, cows

    def _generate_number(self):
        if not self.leading_zero:
            digits = range(1, 10)
            random.shuffle(digits)
            first_digit = digits.pop()
            # add 0 to unused digits and sample those
            self.secret = [first_digit] + random.sample(digits + [0], self.difficulty - 1)
        else:
            self.secret = random.sample(range(0, 10), self.difficulty)

        print('I\'ve generated a random {} digit number for you.'.format(len(self.secret)))

    def _validate_number(self, raw_guess):
        guess = list(raw_guess)

        try:
            guess = list(map(int, guess))
        except ValueError:
            print('Only use digits 0-9 as your guess.')
            return False

        if len(guess) != self.difficulty:
            print('Please enter a {}-digit number as a guess.'.format(self.difficulty))
            return False

        return guess

    def _pick_word(self):
        with open(self.word_file, 'r') as f:
            try:
                secret = next(f)
            except StopIteration:
                raise ValueError('No words found in the provided file ({})'.format(self.word_file))

            # Reservoir Sampling
            for i, word in enumerate(f):
                if not random.randint(0, i + 1):
                    secret = word

        secret = secret.strip().lower()

        # validate choice
        if not re.match('[a-z]', secret):
            raise ValueError('Words can only contain letters of the English alphabet, found "{}"'.format(secret))
        if len(secret) != len(set(secret)):
            raise ValueError('Only words without character repetition are supported, found "{}"'.format(secret))

        self.secret = list(secret)
        print('I\'ve picked a {}-character-long word for you.'.format(len(self.secret)))

    def _validate_word(self, raw_guess):
        if not re.match('[a-z]', raw_guess):
            print('Only use characters a-z as your guess')
            return False

        guess = list(raw_guess)

        if len(guess) != len(self.secret):
            print('Please enter {} characters as a guess.'.format(len(self.secret)))
            return False
        # evil TODO: only allow guesses that are valid words

        return guess


if __name__ == '__main__':
    args = parse_args()

    game = BullsAndCows(difficulty=args.difficulty, leading_zero=args.leading_zero, word_file=args.word_file)

    try:
        game.play()
    except ValueError as e:
        sys.exit(e)

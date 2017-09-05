#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from collections import defaultdict
from collections import OrderedDict
from pygal.style import DefaultStyle
from datetime import datetime
from datetime import timedelta

import pygal
import json
import sys

yellow_style = DefaultStyle()
yellow_style.background = '#EBB82B'


def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data


def count_words(data):
    word_db = defaultdict(int)
    user_db = defaultdict(int)
    comments = 0
    for stage in data.values():
        for comment in stage['comments']:
            comments += 1
            user_db[comment['author']] += 1
            body = comment['body'].replace(']', ' ')
            words = body.split()
            for word in words:
                word = word.strip('!?.,:()\'"\\/-')
                if len(word) < 1 or len(word) > 20:
                    continue
                if word.startswith('http'):
                    continue
                word_db[word] += 1

    word_db = deduplicate(word_db)

    print('Total of {} words in {} comments by {} users from {} threads'.format(
          sum(word_db.values()),
          comments,
          len(user_db),
          len(data)
          ))

    return word_db


def deduplicate(words):
    for word in words.keys():
        lword = word.lower()
        if word != lword:
            if lword in words:
                if words[word] > words[lword]:
                    words[word] += words[lword]
                    del words[lword]
                else:
                    words[lword] += words[word]
                    del words[word]

    return words


def load_words(filename):
    words = {}
    with open(filename, 'r') as f:
        for line in f:
            words[line.strip().lower()] = True

    return words


def wordcloud(data):
    stopwords = load_words('stopwords.txt')

    words = count_words(data)
    with open('wordcloud.txt', 'w') as f:
        for word in sorted(words, key=words.get, reverse=True):
            if word.lower() in stopwords:
                continue
            if len(word) < 3:
                continue
            if words[word] < 100:
                continue
            uword = unicode(word).encode('utf8')
            f.write('{} {}\n'.format(words[word]/99, uword))


def total_comments(data):
    chart = pygal.StackedBar(
        x_title='Stage',
        y_title='Comments',
        legend_at_bottom=True,
        style=yellow_style
        )
    chart.x_labels = map(str, range(1, 22))

    race_totals = 22 * [0]
    results_totals = 22 * [0]
    for stage in data.values():
        stage_num = stage['stage']
        if stage['type'] == 'race':
            race_totals[stage_num] = len(stage['comments'])
        elif stage['type'] == 'results':
            results_totals[stage_num] = len(stage['comments'])
        else:
            print('Error stage {}'.format(stage_num))

    chart.add('Race Threads', race_totals[1:])
    chart.add('Results Threads', results_totals[1:])

    chart.render_to_file('final/comments.svg')


def top_users(data):
    users = defaultdict(int)

    for stage in data.values():
        for comment in stage['comments']:
            # users[comment['author']] += 1

            # body = comment['body'].replace(']', ' ')
            # words = body.split()
            # for word in words:
            #     word = word.strip('!?.,:()\'"\\/-')
            #     if len(word) < 1 or len(word) > 20:
            #         continue
            #     if word.startswith('http'):
            #         continue
            #     users[comment['author']] += 1

            users[comment['author']] += comment['score']

    with open('final/user_upvotes.txt', 'w') as f:
        for user in sorted(users, key=users.get, reverse=True):
            f.write('{} {}\n'.format(users[user], user))


def find_oldest(comments):
    oldest = datetime(2111, 1, 1)

    for comment in comments:
        created = datetime.fromtimestamp(comment['created'])
        if created < oldest:
            oldest = created

    return oldest


def bucketize_comments(start, comments):
    interval= 15 * 60
    buckets = [0] * (60/15) * 12

    # start = find_oldest(comments)
    for comment in comments:
        created = datetime.fromtimestamp(comment['created'])
        age = (created - start).total_seconds()
        bucket = int(age / interval)
        if bucket >= len(buckets):
            continue
        buckets[bucket] += 1

    return buckets


def graph_timeline(data, stage):
    oldest = None
    for thread in data.values():
        if thread['stage'] == stage and thread['type'] == 'race':
            oldest = find_oldest(thread['comments'])
            break
    else:
        print('ERRR OLDEST')
        return

    for thread in data.values():
        if thread['stage'] == stage and thread['type'] == 'race':
            race_buckets = bucketize_comments(oldest, thread['comments'])
        elif thread['stage'] == stage and thread['type'] == 'results':
            results_buckets = bucketize_comments(oldest, thread['comments'])

    chart = pygal.Line(width=800, height=400,
        title='Stage {}'.format(stage),
        x_title='Time',
        y_title='Comments',
        legend_at_bottom=True,
        show_x_labels=False,
        show_dots=False,
        style=yellow_style,
        interpolate='hermite', interpolation_parameters={'type': 'kochanek_bartels', 'b': -1, 'c': 1, 't': 1},
        show_y_guides=False,
        stroke_style={'width': 3}
        )

    chart.add('Race Thread', race_buckets[:])
    chart.add('Results Thread', results_buckets[:])

    chart.render_to_file('final/timeline_{}.svg'.format(stage))


def best_comments(data):
    # best = OrderedDict()
    best = {}
    bestest = 0
    for stage in data.values():
        for comment in stage['comments']:
            score = comment['score']
            if score > bestest:
                bestest = score
            if score in best:
                if score > 100:
                    print('Duplicit at {}'.format(score))
                continue
            best[score] = comment

    print(bestest)

    with open('final/best_comments.txt', 'w') as f:
        # for i, (score, comment) in enumerate(best.iteritems()):
        for i, score in enumerate(sorted(best.keys(), reverse=True)):
            comment = best[score]
            body = unicode(comment['body']).encode('utf8')
            f.write('{} {}\n{}\n\n'.format(score, comment['author'], body))
            if i > 10:
                break



if __name__ == '__main__':
    data = load_data(sys.argv[1])
    # top_users(data)
    # count_words(data)
    # total_comments(data)
    # for stage in range(1, 22):
    #     graph_timeline(data, stage)
    best_comments(data)

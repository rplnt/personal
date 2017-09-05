#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import praw
import json
import sys
import os
import re


def get_thread(reddit, thread_url):
    submission = reddit.submission(url=thread_url)
    submission.comments.replace_more(limit=None, threshold=0)
    comments = submission.comments.list()

    comment_list = []
    for comment in comments:
        if not comment.author:
            continue
        comment_list.append({
            'author': comment.author.name,
            'created': comment.created_utc,
            'score': comment.score,
            'body': unicode(comment.body).encode('utf8')
            })

    print('Loaded {} comments'.format(len(comment_list)))
    return comment_list


def get_type_from_url(url):
    return 'race' if url.find('race') > 0 else ('results' if url.find('result') else None)


def get_stage_from_url(url):
    m = re.search(r'stage_(\d\d?)', url, re.IGNORECASE)
    if m:
        try:
            stage = int(m.group(1))
        except ValueError:
            stage = m.group(1)
        return stage
    else:
        return None


def read_multiple(filename):
    reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=sys.argv[1], user_agent='scraper/0.1')

    threads = {}
    with open(filename, 'r') as f:
        for url in f:
            print('Processing {}'.format(url))
            threads[url] = {}
            threads[url]['type'] = get_type_from_url(url)
            threads[url]['stage'] = get_stage_from_url(url)
            # threads[url]['comments'] = get_thread(reddit, url.strip())

    return threads


if __name__ == '__main__':
    threads = read_multiple(sys.argv[2])
    with open('{}.json'.format(sys.argv[2].rsplit('.', 1)[0]), 'w') as f:
        json.dump(threads, f, indent=2)

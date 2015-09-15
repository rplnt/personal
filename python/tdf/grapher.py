from collections import defaultdict
import pygal
import json
import sys
import os
import re

TOP = 5
FRENCH_LIST = [1, 2, 3, 4, 5, 9, 10, 14, 16, 18]

WIDTH = 800
HEIGHT = 480


def get_stage_files(path):
    files = []
    for filename in os.listdir(path):
        if os.path.splitext(filename)[1] == '.json':
            files.append(filename)
    files.sort(key=lambda x: int(re.search(r'(\d+)', x).group(0)))

    return files


def gc_progress(year, key='time'):
    path = os.path.join('.', year)
    files = get_stage_files(path)

    with open(os.path.join(path, files[-1])) as fp:
        final_gc = json.load(fp)

    top = {}
    for rider, data in final_gc.items():
        # if data['pos'] < TOP + 1:
        #     top[data['pos']] = rider
        if data['pos'] in FRENCH_LIST:
            top[data['pos']] = rider

    rider_data = defaultdict(list)
    for stage in files:
        with open(os.path.join(path, stage)) as fp:
            stage_gc = json.load(fp)
        for pos in top.keys():
            val = stage_gc[top[pos]][key]
            rider_data[top[pos]].append(val)

    for _ in range(21 - len(files)):
        for pos in top:
            rider_data[top[pos]].append(None)

    chart = pygal.Line(width=WIDTH, height=HEIGHT,
                       show_legend=True,
                       show_dots=False,
                       fill=False,
                       show_y_labels=True,
                       legend_at_bottom=True,
                       # range=(0, 12*60),
                       label_font_size=17,
                       major_label_font_size=17,
                       legend_font_size=17,
                       y_labels_major_every=3)
    chart.x_labels = map(str, range(1, 22))  # len(files) + 1))  # 22

    for rider, data in rider_data.items():
        chart.add(rider, data)

    chart.render_to_file(year + '_' + 'french2' + '.svg')


def second_place(years=[2012, 2013, 2014, 2015]):

    chart = pygal.Bar(width=WIDTH, height=HEIGHT,
                      fill=True,
                      show_legend=True,
                      show_dots=False,
                      show_y_labels=True,
                      legend_at_bottom=True,
                      label_font_size=17,
                      major_label_font_size=17,
                      legend_font_size=17,
                      y_labels_major_every=3)
    chart.x_labels = map(str, range(1, 22))

    for year in years:
        path = os.path.join('.', str(year))
        files = get_stage_files(path)

        stage_gaps = []
        for stage in files:
            with open(os.path.join(path, stage)) as fp:
                stage_gc = json.load(fp)

            for rider in stage_gc.keys():
                if stage_gc[rider]['pos'] == 2:
                    stage_gaps.append(stage_gc[rider]['time'])
        chart.add(str(year), stage_gaps)

        while len(stage_gaps) < 21:
            stage_gaps.append(None)

    chart.render_to_file('stage_gaps.svg')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        gc_progress(sys.argv[1])
    else:
        second_place()

#!/usr/bin/env python
from __future__ import print_function

import pygal
import re

STAGE_COUNT = 21
CURRENT_STAGE = 13
DEFAULT_YEARS = [2014, 2015, 2016, 2017]
STARTERS = 198

WIDTH = 800
HEIGHT = 400
WITHDRAWALS_FILE = 'withdrawals.{}.txt'
RIDER_COSTS_FILE = 'riders.{}.txt'


def get_widthdrawals(year):
    '''
    Stage ##
    ###\tSURNAME name TEAM\treason
    '''
    with open(WITHDRAWALS_FILE.format(year)) as f:
        withdrawals = f.readlines()

    abandoned = {}
    stage = 0
    for line in withdrawals:
        m = re.match(r'Stage (\d+)', line)
        if m:
            stage = int(m.group(1))
            continue
        number, name_team, reason = line.split('\t')
        name, team = name_team.rsplit(' ', 1)
        m = re.match(r'(([A-Z]+\s?)+)\s\w+', name)
        # m = re.match(r'([A-Z]+)\s\w+', name)
        if m:
            if stage not in abandoned:
                abandoned[stage] = []
            abandoned[stage].append({
                'name': name[len(m.group(1))+1:].split(' ', 1)[0],
                'surname': m.group(1),
                'team': team
                })
        else:
            print('ERR ' + line)

    return abandoned


def find_costs(abandoned, year):
    '''
    name surname\tteam\tclass\tcost
    '''
    with open(RIDER_COSTS_FILE.format(year)) as f:
        riders = f.readlines()

    rider_costs = []
    for line in riders:
        name, team, _, cost = line.split('\t')
        rider_costs.append((name, cost))
    del riders

    costs = {stage: [] for stage in abandoned.keys()}
    for stage in abandoned.keys():
        for withdrawal in abandoned[stage]:
            for rider, cost in rider_costs:
                if re.search(r'\b{}\b'.format(withdrawal['surname']), rider, re.IGNORECASE) and re.search(r'\b{}\b'.format(withdrawal['name']), rider, re.IGNORECASE):
                    costs[stage].append(int(cost))
                    break
            else:
                print('ERR: Could not find rider "{}"'.format(withdrawal['surname']))

    return costs


def cummulative(costs, function):
    total = 0
    totals = []
    for stage in range(1,22):
        if stage in costs:
            total += function(costs[stage])
        totals.append(total)
    return totals


def main(years):
    chart = pygal.Line(width=WIDTH, height=HEIGHT,
                       show_legend=True,
                       legend_at_bottom=True,
                       legend_at_bottom_columns=4,
                       show_dots=False,
                       fill=False,
                       show_y_labels=False,
                       stroke_style={'width': 5, 'dasharray': '3, 6', 'linecap': 'round', 'linejoin': 'round'},
                       interpolate='hermite', interpolation_parameters={'type': 'kochanek_bartels', 'b': -1, 'c': 1, 't': 1}
                       )

    bars = pygal.Bar(width=WIDTH, height=HEIGHT,
                     show_legend=True,
                     legend_at_bottom=True,
                     legend_at_bottom_columns=4,
                     show_dots=False,
                     show_y_labels=True,
                     range=(150, 200)
                     )
    bars.zero = 140

    chart.x_labels = map(str, range(1, 22))
    bars.x_labels = map(str, range(1, 22))

    for year in years:
        print(year)
        abandoned = get_widthdrawals(year)
        costs = find_costs(abandoned, year)
        check = True
        for stage in costs.keys():
            # print(stage, abandoned[stage])
            # print(costs[stage])
            check = check and (len(abandoned[stage]) == len(costs[stage]))
        print(check)
        points = cummulative(costs, sum)
        totals = cummulative(costs, len)
        if year == DEFAULT_YEARS[-1]:
            points = points[:CURRENT_STAGE]
            totals = totals[:CURRENT_STAGE]
        print(totals)
        chart.add('{}'.format(year), points)
        # bars.add('{}'.format(year), [len(abandoned[stage]) if stage in abandoned else 0 for stage in range(1, 22)])
        bars.add('{}'.format(year), map(lambda x: STARTERS - x, totals))

    chart.render_to_file('withdrawals_score.svg')
    bars.render_to_file('withdrawals_total.svg')


if __name__ == '__main__':
    main(DEFAULT_YEARS)

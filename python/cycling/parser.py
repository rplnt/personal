from bs4 import BeautifulSoup as bs
import json
import sys
import os
import re


def load_stage(filepath):
    with open(filepath, 'r') as fp:
        soup = bs(fp, 'html.parser')

    last_t = 0
    stage_data = {}
    for pos in xrange(200):
        columns = soup.find_all('div', {'class': 'top{}'.format(pos)})
        if not columns:
            break
        for column in columns:
            if 'lf6' in column['class'] or 'lf13' in column['class']:
                try:
                    name = column.a['href'].split('/')[1].replace('_', ' ')
                except:
                    continue
            if 'lf92' in column['class'] or 'lf93' in column['class'] or 'lf91' in column['class'] or 'lf94' in column['class']:
                t = column.contents[0]
                if ',,' in t:
                    t = last_t
                if pos == 0:
                    t = '0:00'
                match = re.match(r'(\d\d?)?:?(\d\d?)?:(\d\d)', t)
                if match:
                    if match.group(2):
                        h, m, s = match.groups()
                    else:
                        h, m, s = 0, match.group(1), match.group(3)
                else:
                    print "Err: {}".format(pos)
                    h, m, s = 100, 0, 0
        print '.',
        try:
            stage_data[name] = {'pos': pos + 1, 'time': int(h)*60*60 + int(m)*60 + int(s)}
        except:
            print pos
            sys.exit()
        last_t = t
    print

    return stage_data


def main(year):
    path = os.path.join('.', year)
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            match = re.search(r'(\d+)', filename)
            if match:
                stage = match.group(0)
                print "Loading stage {}".format(stage),
            else:
                print 'Err: Unknown stage'
                stage = 'Err'
            if os.path.isfile(os.path.join(path, 'Stage_{}.json'.format(stage))):
                print '... already exists'.format(stage)
                continue
            stage_data = load_stage(os.path.join(path, filename))

            with open(os.path.join(path, 'Stage_{}.json'.format(stage)), 'w') as fp:
                json.dump(stage_data, fp)

if __name__ == '__main__':
    main(sys.argv[1])

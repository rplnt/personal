from bs4 import BeautifulSoup as bs
import requests
import time
import os

server = 'http://www.procyclingstats.com/'
stages = 'race/Tour_de_France_{year}-stages'
years = [2015]


def get_stages(url):
    r = requests.get(server + url)
    if r.status_code != 200:
        print "Error {} ({})".format(r.status_code, url)
        return

    stage_data = {}
    soup = bs(r.text, 'html.parser')
    table = soup.find('table', id='list5')

    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) < 3:
            continue
        a = tds[2].a
        stage_data[a.contents[0].encode('ascii', 'ignore')] = a['href']

    return stage_data


def get_gc(url, name, year):
    if os.path.isfile('{}/{}.html'.format(year, name)):
        print '{} exists'.format(name)
        return

    r = requests.get(server + url)
    if r.status_code != 200:
        print "Error {} ({})".format(r.status_code, name)
        return

    soup = bs(r.text, 'html.parser')
    menu = soup.find('div', id='rnk_tab')
    if not menu:
        return
    a = menu.find_all('a')[1]  # gc tab

    r = requests.get(server + a['href'])
    if r.status_code != 200:
        print "Error {} ({})".format(r.status_code, url)
        return

    soup = bs(r.text, 'html.parser')
    results = soup.find('div', {'class': 'result_list'})

    with open('{}/{}.html'.format(year, name), 'w') as f:
        f.write(str(results))


def main():
    for year in years:
        stage_data = get_stages(stages.format(year=year))

        for name, url in stage_data.items():
            get_gc(url, name, year)
            time.sleep(0.2)

        time.sleep(1)


if __name__ == '__main__':
    main()

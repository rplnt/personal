from bs4 import BeautifulSoup as bs
from collections import defaultdict
import requests
import json
import time

url = 'http://www.procyclingstats.com/race/{}_{}'
year = 2016

races = {
    2015: [
        'Santos_Tour_Down_Under',
        'Tour_of_Qatar',
        'Tour_of_Oman',
        'Omloop_Het_Nieuwsblad_Elite',
        'Paris_Nice',
        'TirrenoAdriatico',
        'MilanoSanremo',
        'Volta_Ciclista_a_Catalunya',
        'E3_Harelbeke',
        'Gent_Wevelgem',
        'Ronde_van_Vlaanderen_Tour_des_Flandres',
        'Vuelta_Ciclista_al_Pais_Vasco',
        'Paris_Roubaix',
        'Amstel_Gold_Race',
        'La_Fleche_Wallonne',
        'Liege_Bastogne_Liege',
        'Tour_de_Romandie',
        'Giro_d_Italia',
        'Amgen_Tour_of_California',
        'Criterium_du_Dauphine',
        'Tour_de_Suisse',
        'Tour_de_France',
        'Clasica_Ciclista_San_Sebastian',
        'Tour_de_Pologne',
        'Eneco_Tour',
        'Vuelta_a_Espana',
        'Vattenfall_Cyclassics',
        'GP_Ouest_France_Plouay',
        'Tour_of_Britain',
        'Grand_Prix_Cycliste_de_Quebec',
        'Grand_Prix_Cycliste_de_Montreal',
        'World_Championships_ITT',
        'World_Championships_Road_Race',
        'Il_Lombardia'
    ],

    2016: [
        'Santos_Tour_Down_Under',
        'Tour_of_Qatar',
        'Tour_of_Oman',
        'Omloop_Het_Nieuwsblad_Elite',
        'Paris_Nice',
        'Tirreno%20_Adriatico',
        'Milano_Sanremo',
        'Volta_Ciclista_a_Catalunya',
        'E3_Harelbeke',
        'Gentwevelgem',
        'Ronde_van_Vlaanderen',
        'Vuelta_Ciclista_al_Pais_Vasco',
        'Paris_-_Roubaix',
        'Amstel_Gold_Race',
        'La_Fleche_Wallonne',
        'Liege_Bastogne_Liege',
        'Tour_de_Romandie',
        # 'Giro_d_Italia',
        # 'Amgen_Tour_of_California',
        # 'Criterium_du_Dauphine',
        # 'Tour_de_Suisse',
        # 'Tour_de_France',
        # 'Clasica_Ciclista_San_Sebastian',
        # 'Tour_de_Pologne',
        # 'Eneco_Tour',
        # 'Vuelta_a_Espana',
        # 'Vattenfall_Cyclassics',
        # 'GP_Ouest_France_Plouay',
        # 'Tour_of_Britain',
        # 'Grand_Prix_Cycliste_de_Quebec',
        # 'Grand_Prix_Cycliste_de_Montreal',
        # 'World_Championships_ITT',
        # 'World_Championships_Road_Race',
        # 'Il_Lombardia'
    ]
}


def get_top(race):
    print race
    r = requests.get(url.format(race, year))
    if r.status_code != 200:
        print "Error {} ({})".format(r.status_code, race)
        return

    soup = bs(r.text, 'html.parser')
    results = soup.find('div', {'class': 'result'}).find_all('div')[:10]

    race_data = []
    for result in results:
        row = {}
        columns = result.find_all('span', recursive=False)

        row['country'] = filter(lambda x: x != 'flags', columns[1].find('span', {'class': 'flags'})['class'])[0]
        row['name'] = columns[1].a['href'].split('/')[1].replace('_', ' ')
        row['team'] = columns[2].a['href'].split('/')[1].replace('_', ' ')

        race_data.append(row)

    return race_data


def scrape():
    rfl = {}
    for race in races[year]:
        rfl[race] = get_top(race)

        time.sleep(0.75)

    with open('data_{}.json'.format(year), 'w') as f:
        json.dump(rfl, f)


def parse():
    points = [15, 12, 10, 8, 6, 5, 4, 3, 2, 1]
    multipliers = [2.0, 1.8, 1.6, 1.4, 1.2, 1.0, 1.0, 1.0]

    with open('data_{}.json'.format(year), 'r') as f:
        data = json.load(f)

    teams = defaultdict(int)
    countries = defaultdict(int)
    riders = defaultdict(int)

    for race in data:
        print race
        t_count = defaultdict(int)
        c_count = defaultdict(int)

        for pos, rider in enumerate(data[race]):

            if len(t_count) < 8:
                teams[rider['team']] += points[pos] * multipliers[t_count[rider['team']]]
                t_count[rider['team']] += 1

            if len(c_count) < 8:
                countries[rider['country']] += points[pos] * multipliers[c_count[rider['country']]]
                c_count[rider['country']] += 1

            riders[rider['name']] += points[pos] * 2.0

        print t_count.values()
        print c_count.values()
        print

    print 'Team | Points'
    print '---- | ------'
    for team in sorted(teams, key=teams.get, reverse=True):
        print '{} | {}'.format(team, teams[team])

    print

    print 'Country | Points'
    print '---- | ------'
    for country in sorted(countries, key=countries.get, reverse=True):
        print '{} | {}'.format(country, countries[country])

    print

    print 'Rider | Points'
    print '---- | ------'
    for rider in sorted(riders, key=riders.get, reverse=True)[:30]:
        print '{} | {}'.format(rider, riders[rider])


if __name__ == '__main__':
    # scrape()
    parse()

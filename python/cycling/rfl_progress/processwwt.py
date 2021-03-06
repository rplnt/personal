import operator
import csv
import sys


def main(f):
    with open(f, 'r') as data:
        rfl = data.readlines()

    header = rfl[0].split(',')
    header = header[1:]
    rfl = rfl[1:]

    racemap = []
    racedata = {}
    for i, key in enumerate(header):
        racedata[key] = {}
        racemap.append(key)

    for pos, row in enumerate(csv.reader(rfl)):
        user = row[0]

        for race in range(1, len(row)):
            racekey = racemap[race - 1]

            if user in racedata[racekey]:
                raise RuntimeError('User already processed?')

            racedata[racekey][user] = float(row[race]) if row[race] is not '' else 0

    print 'Rank,Name,Stage,Points'

    userdata = {}
    for race in racemap:
        for user in racedata[race].keys():
            if user not in userdata:
                userdata[user] = [racedata[race][user]]
            else:
                userdata[user].append(userdata[user][-1] + racedata[race][user])

    for raceid, race in enumerate(racemap):

        for user in userdata.keys():
            racedata[race][user] = userdata[user][raceid]

        users = sorted(racedata[race].items(), key=operator.itemgetter(1), reverse=True)

        for rank, data in enumerate(users):
            user, _ = data
            print '{},{},{},{}'.format(rank + 1 if userdata[user][raceid] > 0 else len(userdata.keys()), user, raceid + 1, userdata[user][raceid])


if __name__ == '__main__':
    main(sys.argv[1])

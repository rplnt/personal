#! /usr/bin/python
import re
import sys
import datetime

#access log time format
log_time = '%d/%b/%Y:%H:%M:%S' #it's '%d/%b/%Y:%H:%M:%S %z' but %z doesn't seem to work with strptime
#output/input format
io_format = '%Y-%m-%d'
#logline regular
log_pattern = re.compile(r'^(\S+)\s\S+\s-\s\[(.+?)\]\s\".*?\"\s\S+\s(\S+)')


def day_index(time):
    return time.hour*2 + (1 if time.minute-30>0 else 0)


def print_statline(date, visitor_count, traffic_list, separator='\t'):
    day = date.strftime(io_format)
    to_print = [day, str(visitor_count)] + map(str, traffic_list)
    print separator.join(to_print)


def create_stats(startdate, stopdate, handle):
    first = True
    traffic = [0]*48
    visitors = {}
    for line in handle:
        result = re.match(log_pattern, line)
        if result is None:
            print 'err'
            exit()
        current_time = datetime.datetime.strptime(result.group(2)[:-6], log_time) #[:-6] cuts out tz
        
        if startdate > current_time:
            continue
        if first:
            first = False
            old_date = current_time
        if result.group(1) not in visitors:
            visitors[result.group(1)] = 1
        if result.group(3) != '-':
            traffic[day_index(current_time)] += int(result.group(3))

        if current_time.date() != old_date.date():
            print_statline(old_date, len(visitors.keys()), traffic)
            if current_time >= stopdate:
                return
            traffic = [0]*48
            visitors = {}
            old_date = current_time

    if current_time.date() == old_date.date():
        print_statline(old_date, len(visitors.keys()), traffic)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print '"Usage: '+sys.argv[0]+' from-date until-date [file]..." where date format is '+io_format
        exit()
    start = datetime.datetime.strptime(sys.argv[1],io_format)
    stop = datetime.datetime.strptime(sys.argv[2],io_format)

    if len(sys.argv) == 3:
        create_stats(start, stop, sys.stdin)
    else:
        for file in sys.argv[3:]:
            f = open(file, 'rU')
            create_stats(start, stop, f)
            f.close()
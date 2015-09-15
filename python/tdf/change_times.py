from bs4 import BeautifulSoup as bs
import sys
import re


def main(filename):
    with open(filename, 'r') as fp:
        svg = fp.read()

    soup = bs(svg)

    pattern = re.compile('\d+\.0')
    for tag in soup.find_all('text'):
        if '.' in tag.contents[0]:
            seconds = int(str(tag.contents[0]).split('.')[0])
            minutes = '{}:{:0>2d}'.format(seconds/60, seconds%60)
            tag.contents[0].replace_with(minutes)

    svg = soup.prettify("utf-8")
    with open(filename.split('.')[0] + '_fixed.svg', 'w') as fp:
        fp.write(svg)


if __name__ == '__main__':
    main(sys.argv[1])

# -*- coding: utf-8 -*-
"""
Retrieves 100 most popular movies from IMDb sorted by ranking.
"""
import argparse
import curses

import requests

from bs4 import BeautifulSoup


def get_chart(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
                f'Error retrieving, status code: {response.status_code}')

    chart = BeautifulSoup(response.text, 'lxml')
    chart = chart.body.table.tbody

    # this cryptic generator returns tuples of tv/movie title and its rating
    # NOTE: processing only rated titles
    return ((x.contents[3].a.get_text(), x.contents[5].strong.get('title'))
            for x in chart.find_all('tr') if x.contents[5].strong)


def get_url(args):
    return ('http://www.imdb.com/chart/tvmeter'
            if args.type == 'tv' else
            'http://www.imdb.com/chart/moviemeter')


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', choices=['movie', 'tv'],
                        default='tv', help='chart type')

    return parser.parse_args()


def main(stdscr, retreive_url):
    """ Just playing with curses """
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    middle = round(width / 2)
    row = 0
    delimiter = ' ⇒ '

    # splitting output in two columns here that everything gets on screen
    for title, rate in get_chart(retreive_url):
        if row < height:
            stdscr.addstr(row, 0, delimiter.join([title, rate]))
        else:
            stdscr.addstr(row % height, middle, delimiter.join([title, rate]))

        row += 1

    stdscr.refresh()

    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP or key == ord('k'):
            y, x = stdscr.getyx()
            stdscr.move((y - 1) % height, x)
        elif key == curses.KEY_DOWN or key == ord('j'):
            y, x = stdscr.getyx()
            stdscr.move((y + 1) % height, x)
        elif key == curses.KEY_LEFT or key == ord('h'):
            y, x = stdscr.getyx()
            stdscr.move(y, (x - 1) % width)
        elif key == curses.KEY_RIGHT or key == ord('l'):
            y, x = stdscr.getyx()
            stdscr.move(y, (x + 1) % width)


if __name__ == '__main__':
    retreive_url = get_url(parse())
    curses.wrapper(main, retreive_url)

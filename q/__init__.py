#!/usr/bin/env python3
import sys
import urllib.parse
import webbrowser

import termcolor

from q import spotify, github


def main():
    if sys.argv[1] == 'du':
        webbrowser.open("https://duckduckgo.com/?q=" + urllib.parse.quote_plus(" ".join(sys.argv[2:])))
        exit(0)

    if sys.argv[1] == 'gh':
        if sys.argv[2] == 'notif':
            github.print_notifications()
            exit(0)

        webbrowser.open("https://github.com/" + sys.argv[2])
        exit(0)

    if sys.argv[1] == 'hv':
        webbrowser.open("https://github.com/HedvigInsurance/" + sys.argv[2])
        exit(0)

    if sys.argv[1] == 'sp':
        client = spotify.Spotify()

        if sys.argv[2] == 'current':
            current = client.currently_playing().json()
            print('Playing on: ' + current['device']['name'])
            print(termcolor.colored(current['item']['name'], color='magenta'))
            print('by '
                  + termcolor.colored(', '.join(map(lambda artist: artist['name'], current['item']['artists'])),
                                      color='green')
                  + ' on '
                  + termcolor.colored(
                f"{current['item']['album']['name']} ({current['item']['album']['release_date'][0:4]})",
                color='green'))
            exit(0)

        if sys.argv[2] == 'play':
            client.play()
            exit(0)

        if sys.argv[2] == 'pause':
            client.pause()
            exit(0)

        if sys.argv[2] == 'next':
            client.next()
            exit(0)

        print('No such Spotify command ' + sys.argv[2])
        exit(1)

    print("No such command " + sys.argv[1])
    exit(1)

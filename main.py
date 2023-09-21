import tkinter as tk
import os
import pandas as pd

# list of listened albums
albums = list()


def add_album():
    """add listened albums to list of dictionaries. Each dictionary will contain the following data
    - artist: artist name
    - album - album name
    - year - year of publishing"""

    artist = input('Input Artist name: ')
    album = input('Input Album name: ')
    year = input('Input Year of publishing: ')

    # check that year is a number
    try:
        year = int(year)
    except ValueError:
        print('Year must be a number.')
        year = input('Input Year of publishing: ')
        return

    # add album to the list
    albums.append({
        'artist': artist,
        'album': album,
        'year': year
    })

    print('Album successfully added to the list of listened albums')


def search_album():
    """function for album searching"""

    query = input('What are you searching? ')

    # search album by the name of artist, album or publishing year
    result = list()

    for album in albums:
        if query in album['artist'] or query in album['album'] or query in album['year']:
            result.append(album)

    # return the result of searching
    if len(result) == 0:
        print('Album not found')
    else:
        for album in result:
            print(f'{album["artist"]} - {album["album"]} ({album["year"]})')


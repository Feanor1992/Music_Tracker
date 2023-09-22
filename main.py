import tkinter as tk
import os
import pandas as pd

# dataframe of listened albums
albums = pd.DataFrame(columns=['artist', 'album', 'year'])


def read_albums():
    global albums
    albums = pd.read_csv('albums.csv', dtype={'year': int})
    if albums.empty:
        albums = pd.DataFrame(columns=['artist', 'album', 'year'])


def add_album():
    """add listened albums to dataframe, that contains the following data
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

    # check that album exists
    for existing_album in albums.to_dict(orient='records'):
        if existing_album['artist'] == artist and existing_album['album'] == album and existing_album['year'] == year:
            print('You have listened this album')

    # add album to the dataframe
    albums.loc[len(albums)] = {
        'artist': artist,
        'album': album,
        'year': year
    }

    # save album to dataframe
    albums.to_csv('albums.csv', index=False)

    print('Album successfully added to the list of listened albums')


def search_album():
    """function for album searching"""

    query = input('What are you searching? ')

    # search album by the name of artist, album or publishing year
    albums_found = albums.loc[albums['album'].str.contains(query)]
    if not albums_found.empty:
        print('Found this albums: ')
        for album in albums_found.to_dict(orient='records'):
            print(f'{album["artist"]} - {album["album"]} ({album["year"]}')
    else:
        print('Album not found')


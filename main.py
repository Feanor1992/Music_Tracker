import tkinter as tk
import os
import pandas as pd

# dataframe of listened albums
albums = pd.DataFrame(columns=['artist', 'album', 'year'])


def read_albums():
    global albums
    if albums.empty:
        albums = pd.DataFrame(columns=['artist', 'album', 'year'])
    else:
        albums = pd.read_csv('albums.csv', dtype={'year': int})


def add_album():
    """add listened albums to dataframe, that contains the following data
    - artist: artist name
    - album - album name
    - year - year of publishing"""

    artist = input('Input Artist name: ').lower()
    album = input('Input Album name: ').lower()
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

    query = input('What are you searching? ').lower()

    # search album by the name of artist, album or publishing year
    albums_found = albums.loc[albums['album'].str.contains(query)]
    if not albums_found.empty:
        print('Found this albums: ')
        for album in albums_found.to_dict(orient='records'):
            print(f'{album["artist"]} - {album["album"]} ({album["year"]})')
    else:
        print('Album not found')


def main():
    read_albums()
    # read_books()

    while True:
        print('What you want to do?')
        print('1. Add album')
        # print('2. Add book')
        print('3. Search album')
        # print('4. Search book')
        print('5. Exit')

        choice = input()

        if choice == '1':
            add_album()
        elif choice == '3':
            search_album()
        elif choice == '5':
            break
        else:
            print('You must print numbers 1-5')
            choice = input()


if __name__ == '__main__':
    main()



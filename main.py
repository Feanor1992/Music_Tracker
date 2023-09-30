import tkinter as tk
import os
import pandas as pd

# dataframe of listened albums
albums = pd.DataFrame(columns=['artist', 'album', 'year'])

# dataframe of books read
books = pd.DataFrame(columns=['author', 'cycle', 'book'])


def read_albums():
    global albums
    if not os.path.isfile('albums.xlsx'):
        albums = pd.DataFrame(columns=['artist', 'album', 'year'])
    else:
        albums = pd.read_excel('albums.xlsx', dtype={'year': int})


def read_books():
    global books
    if not os.path.isfile('books.xlsx'):
        books = pd.DataFrame(columns=['author', 'cycle', 'book'])
    else:
        books = pd.read_excel('books.xlsx')


def add_album():
    """add albums to dataframe, that contains the following data
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
            return

    # add album to the dataframe
    albums.loc[len(albums)] = {
       'artist': artist,
       'album': album,
       'year': year
    }

    # save album to dataframe
    albums.to_excel('albums.xlsx', index=False)
    print('Album successfully added to the list of listened albums')


def add_book():
    """add books that you have read to dataframe, that contains the following data
    - author: author name
    - cycle - name of cycle to which the book belongs
    - book - book name"""

    author = input('Input Author name: ').lower()
    cycle = input('Input Cycle name: ').lower()
    book = input('Input Book name: ').lower()

    # check that book exists
    for existing_book in books.to_dict(orient='records'):
        if existing_book['author'] == author and existing_book['cycle'] == cycle and existing_book['book'] == book:
            print('You have read this book')
            return

    books.loc[len(books)] = {
        'author': author,
        'cycle': cycle,
        'book': book
    }

    # save album to dataframe
    books.to_excel('books.xlsx', index=False)
    print('Book successfully added to the list')


def search_album():
    """function for searching albums in the list"""

    query = input('What are you searching? ').lower()

    # search album by the name of artist, album or publishing year
    albums_found = albums.loc[albums['album'].str.contains(query)]
    if not albums_found.empty:
        print('Found this albums: ')
        for album in albums_found.to_dict(orient='records'):
            print(f'{album["artist"]} - {album["album"]} ({album["year"]})')
    else:
        print('Album not found')


def search_book():
    """function for searching books in the list"""

    query = input('What are you searching? ').lower()

    # search book by the name of author, cycle or book name
    books_found = books.loc[books['book'].str.contains(query)]
    if not books_found.empty:
        print('Found this albums: ')
        for book in books_found.to_dict(orient='records'):
            print(f'{book["author"]} - {book["cycle"]}: ({book["book"]})')
    else:
        print('Book not found')


def show_albums():
    """function for showing albums in the list"""

    if not albums.empty:
        print('List of albums: ')
        for album in albums.to_dict(orient='records'):
            print(f'{album["artist"]} - {album["album"]} ({album["year"]})')
    else:
        print('Albums list is empty or not found')


def show_books():
    """function for showing books in the list"""

    if not books.empty:
        print('List of books: ')
        for book in books.to_dict(orient='records'):
            print(f'{book["artist"]} - {book["album"]} ({book["year"]})')
    else:
        print('Books list is empty or not found')


def main():
    read_albums()
    read_books()

    while True:
        print('What you want to do?')
        print('1. Add album')
        print('2. Add book')
        print('3. Search album')
        print('4. Search book')
        print('5. Show list of albums')
        print('6. Show list of books')
        print('7. Exit')

        choice = input()

        if choice == '1':
            add_album()
        elif choice == '2':
            add_book()
        elif choice == '3':
            search_album()
        elif choice == '4':
            search_book()
        elif choice == '5':
            show_albums()
        elif choice == '6':
            show_books()
        elif choice == '7':
            break
        else:
            print('You must print numbers 1-7')


if __name__ == '__main__':
    main()



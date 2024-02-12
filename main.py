import tkinter as tk
from tkinter import ttk
import os
import pandas as pd

# dataframe of listened albums
albums = pd.DataFrame(columns=['artist', 'album', 'year'])

# will be using it in another app
# dataframe of books read
# books = pd.DataFrame(columns=['author', 'cycle', 'book'])

root = tk.Tk()
root.title('Music and Book Tracker')
root.geometry('1240x800')


def read_albums():
    global albums
    if not os.path.isfile('albums.csv'):
        albums = pd.DataFrame(columns=['artist', 'album', 'year'])
    else:
        albums = pd.read_csv('albums.csv')

# will be using it in another app
# def read_books():
#    global books
#    if not os.path.isfile('books.xlsx'):
#        books = pd.DataFrame(columns=['author', 'cycle', 'book'])
#    else:
#        books = pd.read_csv('books.csv')


def add_album():
    """add albums to dataframe, that contains the following data
    - artist: artist name
    - album - album name
    - year - year of publishing"""

    artist_label = tk.Label(root, text='Input Artist name: ')
    artist_entry = tk.Entry(root)
    album_label = tk.Label(root, text='Input Album name: ')
    album_entry = tk.Entry(root)
    year_label = tk.Label(root, text='Input Year of publishing: ')
    year_entry = tk.Entry(root)

    artist_label.grid(row=0, column=0)
    artist_entry.grid(row=0, column=1, columnspan=3)
    album_label.grid(row=1, column=0)
    album_entry.grid(row=1, column=1, columnspan=3)
    year_label.grid(row=2, column=0)
    year_entry.grid(row=2, column=1, columnspan=3)

    def add_album_to_csv():
        """save album to dataframe"""
        global albums

        artist = str(artist_entry.get())
        album = str(album_entry.get())
        year = str(year_entry.get())

        # Create a Series with album information
        album_data = pd.Series({'artist': artist, 'album': album, 'year': year})

        # Check if the album already exists in the dataframe
        if album_data['album'] in list(albums['album']):
            listened_album = tk.Label(root, text='You have listened this album yet')
            listened_album.grid(row=4, column=0, columnspan=2)
            artist_entry.delete(0, tk.END)
            album_entry.delete(0, tk.END)
            year_entry.delete(0, tk.END)
            artist_entry.focus()
            return

        # Add new album to the dataframe
        albums.loc[len(albums)] = album_data

        # save updated dataframe to the excel file
        albums.to_csv('albums.csv', index=False)

        # display success message
        album_successfully_add = tk.Label(root, text=f'Album "{album}" successfully added to the list of listened albums')
        album_successfully_add.grid(row=4, column=0, columnspan=3)

        artist_entry.delete(0, tk.END)
        album_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        artist_entry.focus()

    add_button = tk.Button(root, text='Add', command=add_album_to_csv)
    add_button.grid(row=3, column=0, columnspan=2)


# will be using it in another app
# def add_book():
#    """add books that you have read to dataframe, that contains the following data
#    - author: author name
#    - cycle - name of cycle to which the book belongs
#    - book - book name"""
#
#    author_label = tk.Label(root, text='Input Author name: ')
#    author_entry = tk.Entry(root)
#    cycle_label = tk.Label(root, text='Input Cycle name: ')
#    cycle_entry = tk.Entry(root)
#    book_label = tk.Label(root, text='Input Book name: ')
#    book_entry = tk.Entry(root)
#
#    author_label .grid(row=0, column=0)
#    author_entry.grid(row=0, column=1, columnspan=3)
#    cycle_label.grid(row=1, column=0)
#    cycle_entry.grid(row=1, column=1, columnspan=3)
#    book_label.grid(row=2, column=0)
#    book_entry.grid(row=2, column=1, columnspan=3)
#
#    def add_book_to_csv():
#        """save book to dataframe"""
#        global books
#
#         author = str(author_entry.get())
#         cycle = str(cycle_entry.get())
#         book = str(book_entry.get())
#
#         # Create a Series with book information
#         book_data = pd.Series({'author': author, 'cycle': cycle, 'book': book})
#
#         # Check if the book already exists in the dataframe
#         if book_data['book'] in list(books[books['cycle'] == cycle]['book']):
#             read_book = tk.Label(root, text='You have read this book yet')
#             read_book.grid(row=4, column=0, columnspan=2)
#             return
#
#         # Add new book to the dataframe
#         books.loc[len(books)] = book_data
#
#         # save updated dataframe to the csv file
#         books.to_csv('books.csv', index=False)
#
#         # display success message
#         book_successfully_add = tk.Label(root, text=f'Book {book} successfully added to the list')
#         book_successfully_add.grid(row=4, column=0, columnspan=3)
#
#         author_entry.delete(0, tk.END)
#         cycle_entry.delete(0, tk.END)
#         book_entry.delete(0, tk.END)
#         author_entry.focus()
#
#     add_button = tk.Button(root, text='Add', command=add_book_to_csv)
#     add_button.grid(row=3, column=0, columnspan=2)


def search_album():
    """function for searching albums in the list"""

    album_label = tk.Label(root, text='Input Album name: ')
    album_entry = tk.Entry(root)

    album_label.grid(row=0, column=0)
    album_entry.grid(row=0, column=1, columnspan=3)

    def search_album_in_df():
        album = str(album_entry.get())
        album_data = pd.Series({'album': album})

        # Check if the album already exists in the dataframe
        if album_data['album'] in list(albums['album']):
            listened_album = tk.Label(root, text=f'You have listened {album} yet')
            listened_album.grid(row=2, column=0, columnspan=3)
            album_entry.delete(0, tk.END)
            album_entry.focus()
        elif album_data['album'] not in list(albums['album']):
            listened_album = tk.Label(root, text=f'You have not listen {album}')
            listened_album.grid(row=2, column=0, columnspan=3)
            album_entry.delete(0, tk.END)
            album_entry.focus()

    add_button = tk.Button(root, text='Search', command=search_album_in_df)
    add_button.grid(row=1, column=0, columnspan=2)


# will be using it in another app
# def search_book():
#     """function for searching books in the list"""
#
#     book_label = tk.Label(root, text='Input Book name: ')
#     book_entry = tk.Entry(root)
#
#     book_label.grid(row=0, column=0)
#     book_entry.grid(row=0, column=1, columnspan=3)
#
#     def search_book_in_df():
#         book = str(book_entry.get())
#         book_data = pd.Series({'abook': book})
#
#         # Check if the album already exists in the dataframe
#         if book_data['book'] in list(books['book']):
#             read_book = tk.Label(root, text=f'You have listened {book} yet')
#             read_book.grid(row=2, column=0, columnspan=3)
#             book_entry.delete(0, tk.END)
#             book_entry.focus()
#         elif book_data['book'] not in list(books['book']):
#             read_book = tk.Label(root, text=f'You have not read {book}')
#             read_book.grid(row=2, column=0, columnspan=3)
#             book_entry.delete(0, tk.END)
#             book_entry.focus()
#
#     add_button = tk.Button(root, text='Search', command=search_book_in_df)
#     add_button.grid(row=1, column=0, columnspan=2)


def show_albums():
    """function for showing albums in the list"""

    if not albums.empty:
        table_albums = ttk.Treeview(root, columns=['artist', 'album', 'year'])
        table_albums.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # add name of columns
        for column in albums.columns:
            table_albums.heading(column, text=column)

        # add values to table
        for row in albums.iterrows():
            table_albums.insert('', 'end', values=row)
    else:
        empty_df = tk.Label(root, text='File is empty')
        empty_df.grid(row=1, column=0, columnspan=2)


# will be using it in another app
# def show_books():
#     """function for showing books in the list"""
#
#     if not books.empty:
#         print('List of books: ')
#         for book in books.sort_values(by=['author'], ascending=True).to_dict(orient='records'):
#             print(f'{book["author"]} - {book["cycle"]}: ({book["book"]})')
#     else:
#         print('Books list is empty or not found')

# def main():
#    read_albums()
#    read_books()
#
#    while True:
#        print('What you want to do?')
#        print('1. Add album')
#        print('2. Add book')
#        print('3. Search album')
#        print('4. Search book')
#        print('5. Show list of albums')
#        print('6. Show list of books')
#        print('7. Exit')
#
#        choice = input()
#
#        if choice == '1':
#            add_album()
#        elif choice == '2':
#            add_book()
#        elif choice == '3':
#            search_album()
#        elif choice == '4':
#            search_book()
#        elif choice == '5':
#            show_albums()
#        elif choice == '6':
#            show_books()
#        elif choice == '7':
#            break
#        else:
#            print('You must print numbers 1-7')


def show_gui():
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    root.config(menu=file_menu)
    file_menu.add_command(label="Add Album", command=add_album)
    # file_menu.add_command(label="Add Book", command=add_book)
    file_menu.add_command(label="Search Album", command=search_album)
    # file_menu.add_command(label="Search Book", command=search_book)
    # file_menu.add_command(label="Show Albums", command=show_albums)


def main():
    read_albums()
    # read_books()

    show_gui()
    # add_album()
    # add_book()

    root.mainloop()


if __name__ == '__main__':
    main()

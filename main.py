import tkinter as tk
from tkinter import ttk
import os
import pandas as pd

# dataframe of listened albums
albums = pd.DataFrame(columns=['artist', 'album', 'year'])

root = tk.Tk()
root.title('Music and Book Tracker')
root.geometry('1240x800')

table_albums = None
add_widgets = []
search_widgets = []


def read_albums():
    global albums
    if not os.path.isfile('albums.csv'):
        albums = pd.DataFrame(columns=['artist', 'album', 'year'])
    else:
        albums = pd.read_csv('albums.csv')


def add_album():
    """add albums to dataframe, that contains the following data
    - artist: artist name
    - album - album name
    - year - year of publishing"""
    global table_albums, search_widgets

    # Destroy previous widgets if they exist
    if table_albums:
        table_albums.destroy()
    for widget in search_widgets:
        widget.destroy()

    artist_label = tk.Label(root, text='Input Artist name: ')
    artist_entry = tk.Entry(root)
    album_label = tk.Label(root, text='Input Album name: ')
    album_entry = tk.Entry(root)
    year_label = tk.Label(root, text='Input Year of publishing: ')
    year_entry = tk.Entry(root)

    artist_label.place(x=10, y=10)
    artist_entry.place(x=150, y=10, width=200)
    album_label.place(x=10, y=40)
    album_entry.place(x=150, y=40, width=200)
    year_label.place(x=10, y=70)
    year_entry.place(x=150, y=70, width=200)

    add_widgets.extend([artist_label, artist_entry,
                        album_label, album_entry,
                        year_label, year_entry])

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
            listened_album.place(x=10, y=130)
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
        album_successfully_add.place(x=10, y=130)

        artist_entry.delete(0, tk.END)
        album_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        artist_entry.focus()

    add_button = tk.Button(root, text='Add', command=add_album_to_csv)
    add_button.place(x=10, y=100)
    add_widgets.append(add_button)


def search_album():
    """function for searching albums in the list"""
    global table_albums, add_widgets

    # Destroy previous widgets if they exist
    if table_albums:
        table_albums.destroy()
    for widget in add_widgets:
        widget.destroy()

    album_label = tk.Label(root, text='Input Album name: ')
    album_entry = tk.Entry(root)

    album_label.place(x=10, y=10)
    album_entry.place(x=150, y=10, width=200)

    search_widgets.extend([album_label, album_entry])

    def search_album_in_df():
        album = str(album_entry.get())
        album_data = pd.Series({'album': album})

        # Check if the album already exists in the dataframe
        if album_data['album'] in list(albums['album']):
            listened_album = tk.Label(root, text=f'You have listened {album} yet')
            listened_album.place(x=10, y=70)
            album_entry.delete(0, tk.END)
            album_entry.focus()
        elif album_data['album'] not in list(albums['album']):
            listened_album = tk.Label(root, text=f'You have not listen {album}')
            listened_album.place(x=10, y=70)
            album_entry.delete(0, tk.END)
            album_entry.focus()

    add_button = tk.Button(root, text='Search', command=search_album_in_df)
    add_button.place(x=10, y=40)
    search_widgets.append(add_button)


def show_albums():
    """function for showing albums in the list"""
    global table_albums, add_widgets, search_widgets
    # Destroy previous widgets if they exist
    for widget in add_widgets:
        widget.destroy()
    for widget in search_widgets:
        widget.destroy()
    if table_albums:
        table_albums.destroy()

    if not albums.empty:
        table_albums = ttk.Treeview(root, columns=['artist', 'album', 'year'], show='headings')
        table_albums.place(x=10, y=10, width=1220, height=780)

        # add name of columns
        for column in albums.columns:
            table_albums.heading(column, text=column)

        # add values to table
        for _, row in albums.iterrows():
            table_albums.insert('', 'end', values=row.tolist())

        # Adjust column widths to fit the window size
        for col in table_albums['columns']:
            table_albums.column(col, width=root.winfo_width() // len(table_albums['columns']))

        # Make the table resizable
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
    else:
        empty_df = tk.Label(root, text='File is empty')
        empty_df.place(x=10, y=10)


def show_gui():
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    root.config(menu=file_menu)
    file_menu.add_command(label="Add Album", command=add_album)
    file_menu.add_command(label="Search Album", command=search_album)
    file_menu.add_command(label='Show Albums', command=show_albums)


def main():
    read_albums()
    show_gui()
    root.mainloop()


if __name__ == '__main__':
    main()

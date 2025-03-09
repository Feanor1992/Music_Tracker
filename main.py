import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import os
import pandas as pd
from datetime import datetime


class DataManager:
    """
    A class responsible for handling album data, including reading from
    and writing to a CSV file, as well as adding, updating, and deleting records.
    """
    def __init__(self, filename='albums.csv'):
        self.filename = filename
        # Initialize DataFrame with columns for artist, album, and year
        self.albums = pd.DataFrame(columns=['artist', 'album', 'year'])
        self.read_albums()

    def read_albums(self):
        """
        Reads album data from the CSV file.
        If the file doesn't exist or an error occurs, an empty DataFrame is created.
        """
        if os.path.isfile(self.filename):
            try:
                self.albums = pd.read_csv(self.filename)
            except Exception as e:
                messagebox.showerror('Error', f'Error reading file: {e}')
                self.albums = pd.DataFrame(
                    columns=['artist', 'album', 'year']
                )
        else:
            self.albums = pd.DataFrame(
                columns=['artist', 'album', 'year']
            )

    def save_albums(self):
        """
        Saves the current album DataFrame to the CSV file.
        """
        try:
            self.albums.to_csv(self.filename, index=False)
        except Exception as e:
            messagebox.showerror('Error', f'Error saving file: {e}')

    def add_album(self, artist, album, year):
        """
        Adds a new album to the DataFrame after checking for duplicates.
        Returns a tuple (success, message).
        """
        # Check if the album already exists for the given artist
        if not self.albums[(self.albums['artist'] == artist) & (self.albums['album'] == album)].empty:
           return False, 'Album already exists.'
        new_entry = pd.Series({
            'artist': artist,
            'album': album,
            'year': year
        })
        self.albums.loc[len(self.albums)] = new_entry
        self.save_albums()
        return True, 'Album added successfully.'

    def update_album(self, row_index, column, new_value):
        """
        Updates a specific cell in the DataFrame and saves the changes.
        """
        self.albums.at[row_index, column] = new_value
        self.save_albums()

    def delete_album(self, row_index):
        """
        Deletes a record from the DataFrame and saves the changes.
        """
        self.albums = self.albums.drop(index=row_index).reset_index(drop=True)
        self.save_albums()


class MusicTrackerApp:
    """
    A class for creating and managing the graphical user interface (GUI)
    for the Music Tracker application.

    The application uses a sidebar for navigation and a main content area
    for displaying different views (adding, searching, displaying albums).
    """
    def __init__(self, root):
        self.root = root
        self.root.title('Modern Music Tracker')
        self.root.geometry('1240x800')

        # Set CustomTkinter appearance and color theme
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('blue')

        # Initialize DataManager to handle album data
        self.data_manager = DataManager()

        # Create a sidebar for navigation and a content area for views
        self.sidebar_frame = ctk.CTkFrame(
            self.root,
            width=200
        )
        self.sidebar_frame.grid(
            row=0,
            column=0,
            sticky='ns'
        )
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.grid(
            row=0,
            column=1,
            sticky='nsew'
        )

        # Configure grid weights for proper resizing
        self.root.grid_columnconfigure(
            1,
            weight=1
        )
        self.root.grid_rowconfigure(
            0,
            weight=1
        )

        self.create_sidebar()

    def create_sidebar(self):
        """
        Creates the sidebar with navigation buttons and theme selector.
        """
        add_button = ctk.CTkButton(
            self.sidebar_frame,
            text='Add Album',
            command=self.show_add_album
        )
        add_button.grid(
            row=0,
            column=0,
            padx=20,
            pady=10,
            sticky='ew'
        )

        search_button = ctk.CTkButton(
            self.sidebar_frame,
            text='Search Album',
            command=self.show_search_album
        )
        search_button.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky='ew'
        )

        show_button = ctk.CTkButton(
            self.sidebar_frame,
            text='Show Albums',
            command=self.show_albums
        )
        show_button.grid(
            row=2,
            column=0,
            padx=20,
            pady=10,
            sticky='ew'
        )

        # Theme selection option menu
        tk.Label(self.sidebar_frame, text='Choose Theme:').grid(
            row=3,
            column=0,
            padx=20,
            pady=(20, 5)
        )
        theme_options = ['Dark', 'Light', 'System']
        self.theme_option_menu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=theme_options,
            command=self.change_theme
        )
        self.theme_option_menu.set('Dark')
        self.theme_option_menu.grid(
            row=4,
            column=0,
            padx=20,
            pady=10,
            sticky='ew'
        )

    def change_theme(self, theme):
        """
        Changes the appearance mode of the application.
        """
        ctk.set_appearance_mode(theme)

    def clear_content(self):
        """
        Clears the main content area.
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_add_album(self):
        """
        Displays the 'Add Album' view in the main content area.
        Uses grid layout for positioning widgets.
        """
        self.clear_content()
        frame = ctk.CTkFrame(self.content_frame)
        frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky='nsew'
        )

        # Labels and entry fields for album details
        tk.Label(frame, text='Artist:').grid(row=0, column=0, sticky='w')
        artist_entry = ctk.CTkEntry(frame)
        artist_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(frame, text='Album:').grid(row=1, column=0, sticky='w')
        album_entry = ctk.CTkEntry(frame)
        album_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(frame, text='Year:').grid(row=2, column=0, sticky='w')
        year_entry = ctk.CTkEntry(frame)
        year_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        # Label for displaying validation or success messages
        message_label = tk.Label(frame, text='', fg='red')
        message_label.grid(
            row=3,
            column=0,
            columnspan=2
        )

        def on_add():
            """
            Callback for the 'Add Album' button.
            Validates the input and attempts to add the album via DataManager.
            """
            artist = artist_entry.get().strip()
            album = album_entry.get().strip()
            year_text = year_entry.get().strip()

            # Validate that all fields are provided
            if not artist or not album or not year_text:
                message_label.config(
                    text='All fields are required.',
                    fg='red'
                )
                return
            try:
                year = int(year_text)
                current_year = datetime.now().year
                if year < 1000 or year > current_year:
                    message_label.config(
                        text=f'Year must be between 1000 and {current_year}.',
                        fg='red'
                    )
                    return
            except ValueError:
                message_label.config(
                    text='Year must be a valid number.',
                    fg='red'
                )

            success, msg = self.data_manager.add_album(artist, album, year)
            if success:
                message_label.config(text=msg, fg='green')
                artist_entry.delete(0, tk.END)
                album_entry.delete(0, tk.END)
                year_entry.delete(0, tk.END)
            else:
                message_label.config(text=msg, fg='red')

        add_button = ctk.CTkButton(
            frame,
            text='Add Album',
            command=on_add
        )
        add_button.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=10
        )

    def show_search_album(self):
        """
        Displays the 'Search Album' view in the main content area.
        Allows the user to search for an album by its name.
        """
        self.clear_content()
        frame = ctk.CTkFrame(self.content_frame)
        frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky='nsew'
        )

        tk.Label(frame, text='Album:').grid(row=0, column=0, sticky='w')
        album_entry = ctk.CTkEntry(frame)
        album_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        result_label = tk.Label(frame, text='', fg='blue')
        result_label.grid(
            row=1,
            column=0,
            columnspan=2
        )

        def on_search():
            """
            Callback for the 'Search Album' button.
            Searches for the album and displays the result.
            """
            album = album_entry.get().strip()
            if not album:
                result_label.config(text='Please enter an album name.', fg='red')
                return
            if album in self.data_manager.albums['album'].values:
                result_label.config(text=f'You have already listened to "{album}".', fg='green')
            else:
                result_label.config(text=f'You have not listened to "{album}".', fg='orange')

        search_button = ctk.CTkButton(frame, text='Search Album', command=on_search)
        search_button.grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

    def show_albums(self):
        """
        Displays the 'Show Albums' view with filtering, sorting,
        and a table (Treeview) of album records.

        Also includes a button to open an extended edit window for the selected record.
        """
        self.clear_content()

        # --- Filter and sort frame at the top ---
        filter_frame = ctk.CTkFrame(self.content_frame)
        filter_frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky='ew'
        )

        # Filter fields for artist and year
        tk.Label(filter_frame, text='Filter by Artist:').grid(row=0, column=0, sticky='w')
        artist_filter = ctk.CTkEntry(filter_frame)
        artist_filter.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(filter_frame, text='Filter by Year:').grid(row=0, column=2, sticky='w')
        year_filter = ctk.CTkEntry(filter_frame)
        year_filter.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        # Sort option using CTkOptionMenu (without additional fields)
        tk.Label(filter_frame, text='Sort by:').grid(row=1, column=0, sticky='w')
        sort_options = ['artist', 'album', 'year']
        sort_by = ctk.CTkOptionMenu(filter_frame, values=sort_options)
        sort_by.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # --- Treeview (table) frame ---
        tree_frame = ctk.CTkFrame(self.content_frame)
        tree_frame.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky='nsew'
        )
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        columns = ['artist', 'album', 'year']
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        tree.grid(
            row=0,
            column=0,
            sticky='nsew'
        )
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(
            row=0,
            column=1,
            sticky='ns'
        )

        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=150)

        def populate_tree(data):
            """
            Clears and populates the Treeview with data from the given DataFrame.
            """
            for row in tree.get_children():
                tree.delete(row)
            for index, row in data.iterrows():
                tree.insert(
                    '',
                    'end',
                    iid=index,
                    values=[
                        row['artist'],
                        row['album'],
                        row['year']
                    ]
                )

        # Initially populate the table with all records
        df_filtered = self.data_manager.albums.copy()
        populate_tree(df_filtered)

        def apply_filters():
            """
            Applies filters based on the inputs and updates the Treeview.
            """
            df = self.data_manager.albums.copy()
            a_filter = artist_filter.get().strip().lower()
            y_filter = year_filter.get().strip()
            if a_filter:
                df = df[df['artist'].str.lower().str.contains(a_filter)]
            if y_filter:
                df = df[df['year'].astype(str).str.contains(y_filter)]
            populate_tree(df)

        def apply_sort():
            """
            Sorts the filtered DataFrame by the selected column and updates the Treeview.
            """
            sort_column = sort_by.get()
            df = self.data_manager.albums.copy()
            a_filter = artist_filter.get().strip().lower()
            y_filter = year_filter.get().strip()
            if a_filter:
                df = df[df['artist'].str.lower().str.contains(a_filter)]
            if y_filter:
                df = df[df['year'].astype(str).str.contains(y_filter)]
            populate_tree(df)

        # Buttons to apply/reset filters and sort data
        filter_button = ctk.CTkButton(
            filter_frame,
            text='Apply Filters',
            command=apply_filters
        )
        filter_button.grid(
            row=0,
            column=4,
            padx=5,
            pady=5
        )

        reset_button = ctk.CTkButton(
            filter_frame,
            text='Reset Filters',
            command=lambda: [artist_filter.delete(0, tk.END),
                             year_filter.delete(0, tk.END),
                             populate_tree(self.data_manager.albums)]
        )
        reset_button.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )

        sort_button = ctk.CTkButton(
            filter_frame,
            text='Sort',
            command=apply_sort
        )
        sort_button.grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

        # --- Extended Editing and Deletion ---
        def open_edit_window():
            """
            Opens a new window for extended editing of the selected record.
            Allows updating all fields or deleting the record.
            """
            selected = tree.selection()
            if not selected:
                messagebox.showinfo(
                    'Info',
                    'Please select a record to edit.'
                )
                return
            record_index = int(selected[0])
            record = self.data_manager.albums.loc[record_index]

            # Create a new Toplevel window for editing
            edit_win = ctk.CTkToplevel(self.root)
            edit_win.title('Edit Record')

            # Layout in the edit window using grid
            tk.Label(edit_win, text='Artist:').grid(row=0, column=0, sticky='w')
            artist_edit = ctk.CTkEntry(edit_win)
            artist_edit.grid(
                row=0,
                column=1,
                padx=5,
                pady=5
            )
            artist_edit.insert(0, record['artist'])

            tk.Label(edit_win, text='Album:').grid(row=1, column=0, sticky='w')
            album_edit = ctk.CTkEntry(edit_win)
            artist_edit.grid(
                row=1,
                column=1,
                padx=5,
                pady=5
            )
            album_edit.insert(0, record['album'])

            tk.Label(edit_win, text='Year:').grid(row=2, column=0, sticky='w')
            year_edit = ctk.CTkEntry(edit_win)
            year_edit.grid(
                row=2,
                column=1,
                padx=5,
                pady=5
            )
            year_edit.insert(0, record['year'])

            edit_message = tk.Label(
                edit_win,
                text='',
                fg='red'
            )
            edit_message.grid(
                row=3,
                column=0,
                columnspan=2
            )

            def save_changes():
                """
                Validates and saves changes to the selected record.
                """
                new_artist = artist_edit.get().strip()
                new_album = album_edit.get().strip()
                new_year_text = year_edit.get().strip()

                if not new_artist or not new_album or not new_year_text:
                    edit_message.config(
                        text='All fields are required.',
                        fg='red'
                    )
                    return
                try:
                    new_year = int(new_year_text)
                    current_year = datetime.now().year
                    if new_year < 1000 or new_year > current_year:
                        edit_message.config(
                            text=f'Year must be between 1900 and {current_year}.',
                            fg='red'
                        )
                        return
                except ValueError:
                    edit_message.config(
                        text=f'Year must be a valid number.',
                        fg='red'
                    )
                    return

                # Update all fields in DataManager
                self.data_manager.update_album(
                    record_index,
                    'artist',
                    new_artist
                )
                self.data_manager.update_album(
                    record_index,
                    'album',
                    new_album
                )
                self.data_manager.update_album(
                    record_index,
                    'year',
                    new_year
                )

                # Refresh the Treeview
                populate_tree(self.data_manager.albums)
                edit_message.config(
                    text='Record updated successfully.',
                    fg='green'
                )

            def delete_record():
                """
                Deletes the selected record after confirmation.
                """
                if messagebox.askyesno('Confirm', 'Are you sure you want to delete this record?'):
                    self.data_manager.delete_album(record_index)
                    populate_tree(self.data_manager.albums)
                    edit_win.destroy()

            save_button = ctk.CTkButton(
                edit_win,
                text='Save Changes',
                command=save_changes
            )
            save_button.grid(
                row=4,
                column=0,
                padx=5,
                pady=5
            )

            delete_button = ctk.CTkButton(
                edit_win,
                text='Delete Record',
                command=delete_record
            )
            delete_button.grid(
                row=4,
                column=1,
                padx=5,
                pady=5
            )

        edit_selected_button = ctk.CTkButton(
            self.content_frame,
            text='Edit Selected',
            command=open_edit_window
        )
        edit_selected_button.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )

    def run(self):
        """
        Runs the main application loop.
        """
        self.root.mainloop()


def main():
    """
    Main function to initialize and run the Music Tracker application.
    """
    root = ctk.CTk()
    app = MusicTrackerApp(root)
    app.run()


if __name__ == '__main__':
    main()

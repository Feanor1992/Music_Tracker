# Music Tracker
This application is a simple GUI-based tracker for managing a list of music albums you have listened to.
It allows you to add new albums, search for existing albums, and display all the albums in a table format.
The GUI is built using the tkinter library, and the album data is stored in a CSV file using pandas.

### Features ###
- Add Album: Input details about a new album and add it to the list.
- Search Album: Search for an album in the existing list.
- Show Albums: Display all the albums in a table format.

### Code Overview ###
**Dependencies**
The code relies on the following libraries:
- tkinter: For creating the GUI.
- pandas: For managing the album data in a DataFrame and saving it to a CSV file.

**Main Components**
Global Variables
- albums: A pandas DataFrame to store album information.
- table_albums: A variable to reference the table widget.
- add_widgets: A list to store widgets related to adding an album.
- search_widgets: A list to store widgets related to searching for an album.

**Functions**
- read_albums(): Reads the album data from a CSV file. If the file does not exist, it initializes an empty DataFrame.
- add_album(): Displays input fields for adding a new album. Also handles the logic for adding the album to the DataFrame and saving it to the CSV file.
- search_album(): Displays input fields for searching an album. Checks if the album exists in the DataFrame and displays a message accordingly.
- show_albums(): Displays a table of all the albums in the DataFrame. Adjusts the table size to fit the window.
- show_gui(): Sets up the menu bar with options to add, search, and show albums.
- main(): The main function that initializes the album data, sets up the GUI, and starts the main loop.

**Widget Placement**
- Widgets are placed using the place method for precise control over their position.
- The input fields and buttons are placed at specific coordinates to ensure they stay fixed when switching between views.

**Next Steps**
- Add Edit Functionality: Implement the ability to edit existing albums in the list.

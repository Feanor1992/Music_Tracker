# Music Tracker
This project is a modern GUI-based application for tracking music albums that a user has listened to. The application is built using Python with the CustomTkinter framework to provide a sleek, modern interface, combined with standard tkinter widgets for additional functionality. The code is organized into two main classes to promote modularity and maintainability:

### 1. DataManager ###
  - **Purpose:** Handles all data operations, including reading from and writing to a CSV file (`albums.csv`), and provides methods to add, update, and delete album records.
  - **Key Features:**
    - ***Initialization:*** Creates a pandas DataFrame with the columns `artist`, `album`, and `year`. It then attempts to read existing records from the CSV file. If the file is missing or an error occurs, it initializes an empty DataFrame.
    - ***Error Handling:*** Uses tkinter's `messagebox` to display errors if file reading or writing fails.
    - ***Data Operations:***
      - *add_album:* Checks for duplicate records (by both artist and album) before adding a new entry, returning a success/failure message.
      - *update_album:* Updates a specific cell in the DataFrame and immediately saves the changes.
      - *delete_album:* Deletes an album record and resets the DataFrame index, followed by saving the updated data.

### 2. MusicTrackerApp ###
  - **Purpose:** Manages the graphical user interface (GUI) of the application and handles user interactions.
  - **User Interface Design:**
    - ***Appearance Settings:*** The app is set to use a dark theme by default via CustomTkinter, with the option for the user to switch between Dark, Light, and System themes using an option menu located on the sidebar.
    - ***Layout:*** The interface is split into a sidebar (for navigation) and a main content area (for displaying various views). The grid layout manager is used throughout for a responsive and flexible design.
  - **Main Views:**
    - ***Add Album View:*** Provides form fields for entering an artist, album name, and release year. User input is validated to ensure all fields are filled and that the year is a valid number (within a specified range). Upon successful validation, the album is added via the DataManager.
    - ***Search Album View:*** Allows users to search for an album by name. The application displays whether the album has already been added to the collection.
    - ***Show Albums View:*** Displays all album records in a table using a `ttk.Treeview`.
      - *Filtering & Sorting:* Users can filter records by artist and year, and sort the table by artist, album, or year.
      - *Extended Editing:* An "Edit Selected" button opens a new window for the selected record, allowing users to update all fields or delete the record. The editing window validates the new data before saving changes through the DataManager.

### 3. Additional Details ###
  - **Modularity:** The separation of data handling (DataManager) from user interface logic (MusicTrackerApp) makes the code easy to extend and maintain.
  - **Error & Input Validation:** Input fields are validated with clear error messages, ensuring that users are informed of any issues during data entry.
  - **Packaging:** The code is designed to be packaged into an executable using tools like PyInstaller or auto-py-to-exe. Specific instructions for including CustomTkinter assets (like theme JSON files) are provided to ensure a smooth build process.
### 4.Usage ###
  - **Entry Point:** The application is started by calling the `main()` function, which creates a `CTk` root window, initializes the `MusicTrackerApp`, and enters the main event loop.
  - **Deployment:** To build an executable (e.g., using PyInstaller), make sure to include the CustomTkinter assets by specifying the appropriate `--add-data` arguments.

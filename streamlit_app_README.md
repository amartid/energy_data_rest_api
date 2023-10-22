# streamlit_app.py

## Introduction

This Python script and Streamlit application provide a user-friendly interface for parsing and aggregating energy data from XLSX files. The application allows users to select a specific date or manually enter a date in the format "YYYYMMDD." Additionally, it ensures that users enter a valid date with additional checks. In this modification of the code, the date picker allows the user to select a date from January 1st to the current date.

It then retrieves and processes the corresponding energy data from the ENEX Group's website (https://www.enexgroup.gr). The data is fetched from URLs generated based on the selected date.

## Key Functionalities

- Provides an option to manually enter a date.
- Downloads energy data in XLSX format from the ENEX Group website.
- Filters the data to select records with the "Sell" side description and "Imports" classification.
- Aggregates the total trades for different periods of trade (SORT).
- Converts the aggregated data to JSON format and displays it in a user-friendly manner.
- Checks if a given JSON string is valid using a custom function.
- Saves the bar and line charts as image files and displays them.
- Includes an additional `date_summary` element to display the selected date.
- Generates and displays bar and line plots for visualizing the total trades vs. SORT.
- The processed data is saved in a user-defined output folder for the selected date.

## Usage Instructions

1. **Running the Code**:
Ensure you have the necessary Python libraries installed, including Streamlit.

2. Start the Streamlit Server:
    ```bash
    streamlit run streamlit_app.py

    ```
3. Access the App in Your Browser.

4. To stop your Streamlit app, go back to the terminal where it's running and press Ctrl + C.
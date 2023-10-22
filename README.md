# Python Script DataEngineer01.py

## Introduction

This Python script serves as a versatile tool designed to automate data retrieval, parsing, aggregation, and post-processing. It functions as a RESTful API service and offers the option to save processed data to a file. The script provides robust error handling and clear HTTP status codes.

## Tasks Performed by the Script

### Automated Data Retrieval

**Automated Data Download:**
- This script can automatically fetch an Excel (XLSX) file from a specified link. It accepts a target date query parameter and handles the download process for the provided date.

**Error Handling:**
- Comprehensive error handling is in place to gracefully manage issues such as incorrect date formats or missing files for the specified date.

### Data Parsing & Pre-processing

**Data Parsing:**
- The script parses the downloaded file, filtering out rows where the "side" is labeled as "Sell" and the "classification" as "Imports."

### Data Aggregation & Post-processing

**Data Aggregation:**
- For each "sort," the script calculates the sum of the "total trades" column, presenting the data in a user-friendly format.

**JSON Conversion:**
- The filtered data is converted into JSON format, suitable for various data interchange needs.

**Optional Data Storage:**
- Users have the flexibility to save the JSON data to a file for future reference.

## Prerequisites

Before using this script, ensure you have the following prerequisites:

- Python 3.x installed on your system.

- The necessary Python libraries installed, including requests, pandas, json, os, seaborn, and matplotlib.

## Usage Instructions

1. **Running the Code**:

   - Open your terminal or command prompt.

   - Navigate to the directory where the Python file is located.

   - Run the script using the following command:
     ```bash
     DataEngineer01.py
     ```

2. **Follow the Prompts**:

   - The script initiates with user interaction and data input, prompting you to enter a date in the YYYYMMDD format.

   - Ensure the entered date is in the correct format (8 digits).

   - Verify that the year is 2023 or above, the month is between 1 and 12, and the day is between 1 and 31.

3. **Download Data**:

   - The script constructs a URL based on your input and continuously checks for available file versions. For each version, it:

     - Downloads the file.

     - Filters the data based on specific criteria.

     - Converts the filtered data into JSON format.

     - Offers the option to save the JSON data to a file.

     - Creates bar and line plots for the filtered data.

4. **Note**:

   - You can include pie chart visualization by removing the "#" character in front of the relevant lines in the script.


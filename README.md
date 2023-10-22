# flask_app.py

## API Endpoints

The API provides the following endpoints:

### GET /

- **Description**: A welcome endpoint that serves an HTML template.
- **Usage**: Accessing this endpoint will display a welcome message or a user interface if an HTML template is provided.

### POST /process_data
- Retrieve and process energy data based on a specified date. 
- You can use the `/process_data` endpoint to send a GET or POST request to specify the date you want to process:
- **Description**: Processes energy data for a specific date.
- **Usage**: You can send a POST request with a JSON payload to specify the date for which you want to process the energy data. The date should be in the format "YYYYMMDD."
- You can use the `/process_data` endpoint to send a GET or POST request to specify the date you want to process:

**Using a GET Request with Query Parameters**

To use the GET method, you can pass the desired date as a query parameter in the URL. For example:

http://127.0.0.1:5000/process_data?date=YYYYMMDD

[http://127.0.0.1:5000/process_data?date=20230522](http://127.0.0.1:5000/process_data?date=20230522)

In this case, the date "20230522" is included as a query parameter.

**Retrieving Date Information**

When a GET request is made, the `/process_data` route retrieves the date from the query parameters present in the URL. In the provided example URL, "20230522" is extracted as the date for data processing.

**Using a POST Request**

Additionally, the endpoint can also process data through a POST request. This can be done using an HTML form on the web page, as shown in the provided HTML. In this case, the date is retrieved from the JSON request data submitted through the POST method.

**Request Payload**

You can use the /process_data endpoint to send a GET or POST request with a JSON payload specifying the date you want to process. Here is an example of the request payload:

```json
{
  "date": "20231022"
}
```

## Data Processing

The data processing involves several steps:

1. **Date Validation**: The application validates the format of the selected date to ensure it's in "YYYYMMDD" format.

2. **File Download**: It downloads the energy data in XLSX format from the ENEX Group website based on the provided date.

3. **Data Filtering**: The application filters the data to select records with the "Sell" side description and "Imports" classification.

4. **Data Aggregation**: It aggregates the total trades for different periods of trade (SORT).

5. **Data Conversion**: The aggregated data is converted to JSON format.

6. **Chart Generation**: Bar and line charts are generated for visualizing the total trades vs. SORT.

7. **Output Files**: The processed data, JSON, and charts are saved in an output folder.
       
## Response   

A successful response will include information about the processed data, including selected date, data URL, and paths to output files and charts.

```json
{
  "status": "success",
  "message": "Data processed successfully",
  "data": {
    "selected_date": "20231022",
    "selected_date_url": "https://www.enexgroup.gr/documents/20126/200106/20231022_EL-DAM_Results_EN_v01.xlsx",
    "json_data": [...],  # Processed JSON data
    "date_folder": "output_data/20231022",
    "files": {
      "xlsx_file": "output_data/20231022/20231022_EL-DAM_Results_EN_v01.xlsx",
      "filtered_xlsx_file": "output_data/20231022/20231022_EL-DAM_Results_EN_v01_f.xlsx",
      "json_data_file": "output_data/20231022/20231022_EL-DAM_Results_EN_v01.json",
      "charts": {
        "bar_chart": "output_data/20231022/bar_plot_20231022.png",
        "line_chart": "output_data/20231022/line_plot_20231022.png"
      }
    }
  }
}
```

HTML file (`index.html`):
HTML document creates a user interface for selecting a date, triggering data processing, and displaying the results. It uses JavaScript to facilitate user interactions and communicates with a backend API for data processing. 

**Date Selection:**
- Users can select a date using an HTML `input` element of type `date`. The date range is limited between "2023-01-01" and the current date.

**Manual Date Input:**
- Users can manually enter a date in the "YYYYMMDD" format in an HTML `input` element. Input is restricted to 8 digits.

**Process Button:**
- A "Process Date" button allows users to trigger the data processing operation based on the selected or manually entered date.

**Result Display:**
- The processed data and API response are displayed below the "Process Date" button. The data is presented as a well-formatted JSON string.

**JavaScript Functions:**
- JavaScript functions are defined to handle user interactions and process the selected or manually entered date.
- Functions include clearing the manual input and date picker, and submitting the selected date for processing.

### Notes

* The API performs validation checks to ensure the format of the selected date is correct.
* Error responses will include a status code (e.g., 400 for Bad Request, 500 for Internal Server Error).
* You can customize the output folder path and other settings based on your requirements.

from flask import Flask, request, jsonify, render_template
from datetime import date
import json
import requests
import pandas as pd
import os
import shutil
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from openpyxl import Workbook
from collections import OrderedDict
from pathlib import Path

app = Flask(__name__, template_folder="templates")

# Suppress the "Workbook contains no default style" warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

# Define base URL
base_url = "https://www.enexgroup.gr/documents/20126/200106/YYYYMMDD_EL-DAM_Results_EN_v##.xlsx"

# Define folder to save files
output_folder = "output_data"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define functions
def download_file(link, output_folder="."):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            file_name = os.path.join(output_folder, link.split("/")[-1])
            with open(file_name, 'wb') as file:
                file.write(response.content)
            return file_name
        return None
    except Exception as e:
        return None
    
def save_chart_as_png(chart, folder, file_name):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file_name)
    chart.savefig(file_path)
    return file_path
# Download a file from a URL and save it

def filter_file(file_name):
    xlsx_file = file_name
    df = pd.read_excel(xlsx_file)
    filtered_df = df[(df['SIDE_DESCR'] == 'Sell') & (df['CLASSIFICATION'] == 'Imports')]
    sum_of_total_trades = filtered_df.groupby('SORT')['TOTAL_TRADES'].sum().reset_index()
    return sum_of_total_trades

def df_to_json(df):
    try:
        json_data = df.to_json(orient='records', indent=4)
        return json_data
    except Exception as e:
        return None

def create_bar_plot(df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='SORT', y='TOTAL_TRADES', data=df)
    plt.xlabel('SORT (Period of Trade)')
    plt.ylabel('TOTAL_TRADES (Sum of Trades)')
    plt.title('Bar Plot: Total Trades vs. Sort')
    return plt

def create_line_plot(df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='SORT', y='TOTAL_TRADES', data=df, marker='o')
    plt.xlabel('SORT (Period of Trade)')
    plt.ylabel('TOTAL_TRADES (Sum of Trades)')
    plt.title('Line Plot: Total Trades vs. Sort')
    return plt

# Define folder to save files
output_folder = "output_data"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define functions (keep them as they are)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    # selected_date = request.json.get('date', None)
    # selected_date = request.args.get('date')
    if request.method == 'GET':
        # Handle GET request, which may include a date in the query parameters
        selected_date = request.args.get('date', None)
    elif request.method == 'POST':
        # Handle POST request, which includes a JSON payload with the date
        selected_date = request.json.get('date', None)
    if not selected_date:
        # Return an error response with a 400 Bad Request status code
        return jsonify({'error': 'Invalid date format. Please provide a date in YYYYMMDD format.'}), 400

    # Server-side validation for the format and length of the selected_date
    if len(selected_date) == 8 and selected_date.isdigit():
        year = int(selected_date[:4])
        month = int(selected_date[4:6])
        day = int(selected_date[6:8])
        date_folder = os.path.join(output_folder, f"{year}{month}{day}")
    else:
        # Return an error response for an invalid date format
        return jsonify({'error': 'Invalid date format. Please provide a date in YYYYMMDD format.'}), 400

    version = "01"
    formatted_url = base_url.replace("YYYY", str(year)).replace("MM", str(month).zfill(2)).replace("DD", str(day).zfill(2)).replace("##", version)
    downloaded_file = download_file(formatted_url)

    if downloaded_file:
        filtered_data = filter_file(downloaded_file)
        new_file_name = downloaded_file.replace(".xlsx", "_f.xlsx")
        filtered_data.to_excel(new_file_name, index=False)
        json_data = df_to_json(filtered_data)
        output_file_name = f"{downloaded_file[:-5]}.json"
        with open(output_file_name, 'w') as file:
            file.write(json_data)
        
        

        
        # Move the downloaded files (XLSX and JSON) to the folder for the selected date
        # Create the folder path for the output files
        date_folder = os.path.join(output_folder, f"{year}{month}{day}")

        # Ensure that the date_folder exists
        os.makedirs(date_folder, exist_ok=True)
        bar_plot = create_bar_plot(filtered_data)
        bar_chart_file = save_chart_as_png(bar_plot, date_folder, f"bar_plot_{year}{month}{day}.png")
        line_plot = create_line_plot(filtered_data)
        line_plot_file = save_chart_as_png(line_plot, date_folder, f"line_plot_{year}{month}{day}.png")
        
        # Move the files to the date-specific folder
        shutil.move(downloaded_file, os.path.join(date_folder, os.path.basename(downloaded_file)))
        shutil.move(output_file_name, os.path.join(date_folder, os.path.basename(output_file_name)))
        shutil.move(new_file_name, os.path.join(date_folder, os.path.basename(new_file_name)))
        json_data = json.loads(json_data)
        # Create your custom JSON response

        response = OrderedDict([
            ('status', 'success'),
            ('message', 'Data processed successfully'),
            ('data', OrderedDict([
                ('selected_date', selected_date),
                ('selected_date_url', formatted_url),  # Add this line
                ('json_data', json_data),
                ('date_folder', f"{date_folder}"),
                ('files', OrderedDict([
                    ('xlsx_file', f"{os.path.join(date_folder, os.path.basename(downloaded_file))}"),
                    ('filtered_xlsx_file', f"{os.path.join(date_folder, os.path.basename(output_file_name))}"),
                    ('json_data_file', f"{os.path.join(date_folder, os.path.basename(new_file_name))}"),
                    ('charts', OrderedDict([
                        ('bar_chart', f"{os.path.join(date_folder, f'bar_plot_{year}{month}{day}.png')}"),
                        ('line_chart', f"{os.path.join(date_folder, f'line_plot_{year}{month}{day}.png')}")
                    ]))
                ]))
            ]))
        ])

        response_dict = dict(response)

        # Return a success response with a 200 OK status code
        return jsonify(response_dict), 200, print("Data processed successfully:")
    
    else:
        # Return an error response for download failure with a 500 Internal Server Error status code
        return jsonify({'error': 'Error occurred during data processing. Unable to download the file.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
import streamlit as st
import requests
import pandas as pd
import json
import os
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
import shutil

# Define base URL
base_url = "https://www.enexgroup.gr/documents/20126/200106/YYYYMMDD_EL-DAM_Results_EN_v##.xlsx"

# Define folder to save files
output_folder = "output_data"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define functions
def write_json_to_file(json_data, file_name):
    try:
        with open(file_name, 'w') as file:
            file.write(json_data)
        st.success(f"JSON data has been written to {file_name} successfully.")
    except Exception as e:
        st.error(f"An error occurred while writing to the file: {e}")

def save_chart_as_png(chart, folder, file_name):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file_name)
    chart.savefig(file_path)
    return file_path
# Download a file from a URL and save it
def download_file(link, output_folder="."):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            file_name = os.path.join(output_folder, link.split("/")[-1])
            with open(file_name, 'wb') as file:
                file.write(response.content)
            st.success(f'File Download Complete: {file_name}')
            return file_name
        else:
            if response.status_code == 404:
                st.error(f'File not found (404 Error) for the specified date: {link}')
            else:
                st.error(f'Error occurred during download ({response.status_code} Error) for the specified date: {link}')
            return None
    except Exception as e:
        st.error(f'Error: {e}')
        return None
# Filter data from an XLSX file
def filter_file(file_name):
    xlsx_file = file_name
    df = pd.read_excel(xlsx_file)
    filtered_df = df[(df['SIDE_DESCR'] == 'Sell') & (df['CLASSIFICATION'] == 'Imports')]
    sum_of_total_trades = filtered_df.groupby('SORT')['TOTAL_TRADES'].sum().reset_index()
    st.text(sum_of_total_trades.to_string(index=False))
    return sum_of_total_trades

def df_to_json(df):
    try:
        json_data = df.to_json(orient='records', indent=4)
        if is_valid_json(json_data):
            st.write("JSON Data:")
            st.json(json_data)
            return json_data
        else:
            st.error("Not valid JSON data")
            return None
    except Exception as e:
        st.error(f'Error during JSON conversion: {e}')
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
# Check if a given JSON string is valid
def is_valid_json(my_json):
    try:
        json.loads(my_json)
        return True
    except json.JSONDecodeError:
        return False
# Process data for a given year, month, and day
def process_data(year, month, day):
    version = "01"
    formatted_url = base_url.replace("YYYY", str(year)).replace("MM", str(month).zfill(2)).replace(
        "DD", str(day).zfill(2)).replace("##", version)
    downloaded_file = download_file(formatted_url)
    if downloaded_file is not None:
        filtered_data = filter_file(downloaded_file)
        new_file_name = downloaded_file.replace(".xlsx", "_f.xlsx")
        st.write(f'Changes saved successfully: {new_file_name}')
        filtered_data.to_excel(new_file_name, index=False)
        json_str = df_to_json(filtered_data)
        output_file_name = f"{downloaded_file[:-5]}.json"
        write_json_to_file(json_str, output_file_name)
        bar_plot = create_bar_plot(filtered_data)
        bar_chart_file = save_chart_as_png(bar_plot, os.path.join(output_folder, f"{year}{month}{day}"), "bar_chart.png")
        line_plot = create_line_plot(filtered_data)
        line_chart_file = save_chart_as_png(line_plot, os.path.join(output_folder, f"{year}{month}{day}"), "line_chart.png")
        # Move the downloaded files (XLSX and JSON) to the folder for the selected date
        date_folder = os.path.join(output_folder, f"{year}{month}{day}")
        shutil.move(downloaded_file, os.path.join(date_folder, downloaded_file.split("/")[-1]))
        shutil.move(output_file_name, os.path.join(date_folder, output_file_name.split("/")[-1]))
        shutil.move(new_file_name, os.path.join(date_folder, new_file_name))

        st.image([bar_chart_file])
        st.image([line_chart_file])

# Streamlit app
st.title("ENEX Data Analysis")
st.header("Select by Date", divider=True)

# Initialize the selected date with today's date
# Add a date picker for selecting a date
selected_date = st.date_input("Select a date:", min_value=date(2023, 1, 1), max_value=date.today())
manual_date_input = st.text_input("Enter a date manually (YYYYMMDD):")
date_summary = st.empty()

if st.button("Pick a Date", key="pick_date_button", type="primary"):
    if selected_date:
        year = selected_date.year
        month = selected_date.month
        day = selected_date.day
        date_summary.text(f"Selected Date: {year}/{month}/{day}")
        process_data(year, month, day)

if manual_date_input and len(manual_date_input) == 8 and manual_date_input.isdigit():
    year = int(manual_date_input[:4])
    month = int(manual_date_input[4:6])
    day = int(manual_date_input[6:8])
    if year is not None and month is not None and day is not None:
        date_summary.text(f"Selected Date: {year}/{month}/{day}")
        process_data(year, month, day)

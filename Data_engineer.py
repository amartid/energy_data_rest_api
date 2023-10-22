import requests
import pandas as pd
import json
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Define functions

def download_file(link, output_folder="."):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            file_name = os.path.join(output_folder, link.split("/")[-1])
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f'File Download Complete: {file_name}')
            return file_name
        else:
            if response.status_code == 404:
                print(f'File not found (404 Error) for the specified date: {link}')
            else:
                print(f'Error occurred during download ({response.status_code} Error) for the specified date: {link}')
            return None
    except Exception as e:
        print(f'Error: {e}')
        return None

def filter_file(file_name):
    xlsx_file = file_name
    df = pd.read_excel(xlsx_file)
    filtered_df = df[(df['SIDE_DESCR'] == 'Sell') & (df['CLASSIFICATION'] == 'Imports')]
    sum_of_total_trades = filtered_df.groupby('SORT')['TOTAL_TRADES'].sum().reset_index()
    print(sum_of_total_trades.to_string(index=False))

    user_response = input("Do you want to save the changes to a new XLSX file? (yes/no): ")

    if user_response.lower() == "yes":
        new_file_name = file_name.replace(".xlsx", "_f.xlsx")
        filtered_df.to_excel(new_file_name, index=False)
        print(f'Changes saved successfully: {new_file_name}')
    else:
        print('Changes not saved.')
    return sum_of_total_trades

def df_to_json(df, print_json=True):
    try:
        json_data = df.to_json(orient='records', indent=4)                
        print()
        if is_valid_json(json_data):  # Check for valid JSON data
            print("Valid JSON data")
            if print_json:
                print("Aggregated Data in JSON Format:")
                print(json_data)
            return json_data
        else:
            print("Not valid JSON data")
            return None
    except Exception as e:
        print(f'Error during JSON conversion: {e}')
        return None

def create_bar_plot(df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='SORT', y='TOTAL_TRADES', data=df)
    plt.xlabel('SORT (Period of Trade)')
    plt.ylabel('TOTAL_TRADES (Sum of Trades)')
    plt.title('Bar Plot: Total Trades vs. Sort')
    plt.show()

def create_line_plot(df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='SORT', y='TOTAL_TRADES', data=df, marker='o')
    plt.xlabel('SORT (Period of Trade)')
    plt.ylabel('TOTAL_TRADES (Sum of Trades)')
    plt.title('Line Plot: Total Trades vs. Sort')
    plt.show()

def create_pie_chart(df):
    data = df['TOTAL_TRADES']
    labels = df['SORT']
    title = 'Distribution of SORT by Total Trades'
    colors = sns.color_palette('pastel')[0:len(data)]
    plt.pie(data, labels=labels, colors=colors, autopct='%.0f%%')
    plt.title(title)
    plt.axis('equal')
    plt.show()

def write_json_to_file(json_data, file_name):
    try:
        with open(f"{file_name}.json", 'w') as file:
            file.write(json_data)
        print(f"JSON data has been written to {file_name}.json successfully.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")  # "ValueError," "IOError," or "RequestException,"
        print(f'An error of type {type(e).__name__} occurred: {str(e)}')

def is_valid_json(my_json):
    try:
        json.loads(my_json)
        return True
    except json.JSONDecodeError:
        return False

if __name__ == "__main__":
    base_url = "https://www.enexgroup.gr/documents/20126/200106/YYYYMMDD_EL-DAM_Results_EN_v##.xlsx"

    user_input = input("Enter a date in YYYYMMDD format: ")

    if len(user_input) != 8 or not user_input.isdigit():
        print("Invalid date format. Please use the format YYYYMMDD with 8 digits.")
    else:
        year = int(user_input[:4])
        month = int(user_input[4:6])
        day = int(user_input[6:8])

        try:
            if year < 2023:
                raise ValueError("Invalid Year. Please use a valid year, 2023 or above (YYYY).")

            if not 1 <= month <= 12:
                raise ValueError("Invalid month. Please use a valid month (MM).")

            if not 1 <= day <= 31:
                raise ValueError("Invalid day. Please use a valid day (DD)")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
        else:
            version = '01'
            while True:
                formatted_url = base_url.replace("YYYY", str(year)).replace("MM", str(month).zfill(2)).replace("DD", str(day).zfill(2)).replace("##", version)
                downloaded_file = download_file(formatted_url)

                if downloaded_file is not None:
                    filtered_data = filter_file(downloaded_file)
                    # print_json = True 

                    # user_response = input("Do you want to print the JSON data? (yes/no): ")
                    # if user_response.lower() == "yes":
                    #     print_json = True
                    # else :
                    #     print_json = False
                    json_str = df_to_json(filtered_data)
                    print()
  

                    user_response = input("Do you want to write the JSON data to a file? (yes/no): ")
                    if user_response.lower() == "yes":
                        output_file_name =  f"{downloaded_file[:-5]}"  # remove xlsx file extension
                        write_json_to_file(json_str, output_file_name)
                    print("Data Visualization:")
                    print(f"Bar Plot: Total Trades vs. Sort")
                    create_bar_plot(filtered_data)
                    print(f"Line Plot: Total Trades vs. Sort")
                    create_line_plot(filtered_data)
                    # print(f"Pie Chart: Distribution of SORT by Total Trades")
                    # create_pie_chart(filtered_data)

                next_version = f'v{int(version[1:]) + 1:02d}'
                next_version_exists = requests.head(base_url.replace("YYYY", str(year)).replace("MM", str(month).zfill(2)).replace("DD", str(day).zfill(2)).replace("##", next_version))

                if next_version_exists.status_code == 200:
                    user_response = input(f"Do you want to check version {next_version}? (yes/no): ")
                    if user_response.lower() == "yes":
                        version = next_version
                    else:
                        break
                else:
                    print(f"No more versions available for the given date.")
                    break

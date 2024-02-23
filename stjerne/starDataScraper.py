import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

url = 'https://app.aavso.org/webobs/results/?star=000-BCQ-471&num_results=200&page=200' # side med ønsket stjernedata

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    observations_dict = {}

    observation_rows = soup.find_all('tr', class_=['obs tr-even', 'obs tr-odd'])

    for row in observation_rows:
        calendar_date = row.find_all('td')[3].text.strip()
        magnitude_link = row.find('a')
        magnitude = magnitude_link.text.strip() if magnitude_link else "N/A"

        observations_dict[calendar_date] = magnitude

    print(observations_dict)
else:
    print(f"Failed to retrieve webpage, status code {response.status_code}")


def convert_date(date_str):
    parts = date_str.rsplit('.', 1)
    date_part = parts[0] 
    fractional_day = parts[1]
    
    parsed_date = datetime.strptime(date_part, '%Y %b. %d')
    
    seconds_in_day = 24 * 60 * 60
    seconds = float(f"0.{fractional_day}") * seconds_in_day
    additional_time = timedelta(seconds=seconds)
    
    final_datetime = parsed_date + additional_time
    
    return final_datetime.strftime('%Y-%m-%d %H:%M:%S')


original_date_str = "2024 Jan. 02.94733"
converted_date = convert_date(original_date_str)
print(f"Original: {original_date_str} -> Converted: {converted_date}")


filename = './starData3.csv'

with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['Calendar Date', 'Magnitude']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for calendar_date, magnitude in observations_dict.items():
        writer.writerow({'Calendar Date': convert_date(calendar_date), 'Magnitude': magnitude})

print(f"Data successfully written to {filename}")

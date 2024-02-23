import random
from bs4 import BeautifulSoup
import requests
from datetime import datetime

current_date = datetime.now().strftime('%Y-%m-%d')

# dato format 2024-02-16.

# I utgangspungtet laget for å bli importert i main.py og kjørt som en enhet, kjøres separat i praksis.

# noen temp verdier er listet som N/A dersom scriptet ikke finner passende tallverdi, mulig brannmur sak hos yr
# på grunn av mange requests samme IP

class Scraper:
    def __init__(self, start_date:str, end_date:str, csv) -> None:
        self.csv_base = csv
        self.all_dates = []
        self.temperatures = []

        self.output_dates = []
        self.output_temps = []

        self.start_date = start_date
        self.end_date = end_date
        self.data_path = f"./historiskVærdataFra{self.start_date}--til--{self.end_date}.csv"
        self.base_url = "https://www.yr.no/nb/historikk/graf/1-92416/Norge/Vestland/Bergen/Bergen?q=" # 1-92416 leddet i URLen er for bergen


    def generate_dates_list(self):
        months_with_31_days = ["01","03","05","07","08","10","12",]
        months_with_30_days = ["04","06","09","11"]
        year,month,day = self.start_date.split("-")
        

        while f"{year}-{month}-{day}" != self.end_date:
            last_of_regular_month = (day == "32" and month in months_with_31_days) or (day == "31" and month in months_with_30_days)
            last_of_february = (day == "29" and month == "02") or (day == "30" and month == "02" and year % 4 == 0)

            if last_of_regular_month or last_of_february:
                day = "01"
                
                if month == "12":                    
                    year = str(int(year)+1)
                    month = "01"
                    day = "01"
                
                else:
                    month = str(int(month)+1)
                    if len(month) == 1:
                        month = "0"+month
                    day = "01"

            self.all_dates.append(f"{year}-{month}-{day}")
            
            day = str(int(day)+1)
            if len(day) == 1:
                day = "0"+day

    def write_to_csv(self, year:str, file_prefix="", YBY=False):

        file_path = f"./data/{file_prefix}temps.csv" if YBY else self.csv_base
        with open(file_path, "w") as file:
            for i in range(len(self.all_dates)):
                if year in self.all_dates[i]:

                    temp = self.temperatures[i] if i < len(self.temperatures) else "N/A"
                    date = self.all_dates[i]
                    file.write(f"{date},{temp}\n")


    def scrape(self):
        if len(self.all_dates) == 0:
            self.generate_dates_list()
        print("done generating dates")

        for date in self.all_dates:
            rqst = requests.get(self.base_url+date)

            if rqst.status_code != 200:
                print("status code error") # i tilfelle 403 grunnet IP svarteliste
                return

            soup = BeautifulSoup(rqst.content, 'html.parser')
    
            temp_container = soup.find('span', class_='temperature')
            
            if temp_container:
                temperature = temp_container.text.strip()
                self.temperatures.append(temperature.replace("°","").replace("Temperatur","").replace(",","."))

                self.output_temps.append(temperature.replace("°","").replace("Temperatur","").replace(",","."))
                self.output_dates.append(date)

            else:
                self.temperatures.append("N/A") # ved ALLE tilfeller hvor temp ikke registreres skrives N/A
            

            if "12-31" in date or True:
                print("writing to file for year: " + date.split("-")[0])
                year = date.split("-")[0]
                self.write_to_csv(year,file_prefix=f"{year}-",YBY=True)
                self.output_temps = []
                self.output_dates = []
    

scraper = Scraper("2024-01-01",current_date,"./bergen-air-temp.csv")
scraper.scrape()

#for temp in scraper.temperatures:
#    print(temp)
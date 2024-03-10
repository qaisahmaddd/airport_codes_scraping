import requests
from bs4 import BeautifulSoup
import pandas as pd


base_url = 'https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_'

data = []

# Loop dari halaman A sampai Z
for letter in range(ord('A'), ord('Z') + 1):
    url = f'{base_url}{chr(letter)}'
    print(f"Memproses halaman: {url}") 
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        
        if table:
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    row_data = [col.get_text(strip=True) for col in columns]
                    data.append(row_data)
        else:
            print(f'Tidak ditemukan tabel di halaman {chr(letter)}')
    else:
        print(f'Gagal mengakses {chr(letter)}')

column_names = ['origin_station_code', 'icao', 'origin_station_name', 'origin_station_location', 'time', 'dst']  

airport_list = pd.DataFrame(data, columns=column_names)
airport_list.to_csv('airport_list.csv', index=False)

print("Scraping selesai. Data disimpan ke 'airport_list.csv'")
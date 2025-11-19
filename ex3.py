import time
import re
import ast

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt

def read_html_file(file_path : str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def process_num(value):
    # 1. Si value est une string représentant une liste → la convertir
    if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
        try:
            value = ast.literal_eval(value)  # transforme "['1823.0']" en ['1823.0']
        except:
            pass

    # 2. Si value est une liste Python → prendre le premier élément
    if isinstance(value, list):
        if len(value) == 0:
            return None  # ou 0.0 selon ton besoin
        value = value[0]

    # 3. Convertir en string (sécurisé)
    value = str(value)

    # 4. Nettoyage : ne garder que chiffres, virgules, points, tirets
    cleaned = re.sub(r'[^0-9.,-]', '', value)

    # 5. Retirer les virgules séparateurs de milliers
    cleaned = cleaned.replace(',', '')

    # 6. Conversion finale
    try:
        return float(cleaned)
    except ValueError:
        return None  # selon tes besoins

depression_filename = 'epidemiology_of_depression.html'
sunshine_filename = 'city_sunshine_duration.html'

depression_html = read_html_file(depression_filename)
depression_soup = BeautifulSoup(depression_html, 'html.parser')

depression_rate = [] # preparing list to contain the different depression rates
depression_countries = [] #preparing list to contain the different country names

country_position_in_dep_table = 0
rate_position_in_dep_table = 2

def extract_depression_rates(soup : BeautifulSoup):
    tables = soup.find_all('table')  # Extract all tables in the html file soup
    #print(tables)
    depression_table = tables [0] # Select the first table (index 0) which contains depression data
    #print(depression_table)

    #Loop over rows 
    table_rows = depression_table.find_all('tr') # Extract all rows in the depression table
    for row in table_rows :
        table_cells = row.find_all('td') #Extract all cells (column) in the current row
        
        if(len(table_cells) > 1): # Check if the row contains data cells (not header or empty rows)
            country = table_cells[country_position_in_dep_table] # Extract country name based on the number of the column
            depression_countries.append(country.text.strip()) # Append country name to the list
           
            rate = table_cells[rate_position_in_dep_table] # Extract depression rate
            depression_rate.append(round(float(rate.text.strip()))) # Append depression rate to the list
    return pd.DataFrame(depression_rate, index=depression_countries, columns=['DALY Rate'])

df_depression = extract_depression_rates(depression_soup)
print(df_depression)

extract_depression_rates(depression_soup)
print(f'Extracted depression rates for {df_depression.shape[0]} countries.')

print("-------------------------------")
print("Create sunshine table")

sunshine_html = read_html_file(sunshine_filename)
sunshine_soup = BeautifulSoup(sunshine_html, 'html.parser')

country_sunshine ={} #create a dictionary to contain country names and their sunshine duration
country_position_in_sun_table =0
sunshine_position_in_sun_table =-2

def extract_monthly_sunshine_hours(soup : BeautifulSoup):
    sunshine_tables = soup.find_all('table')  # Extract all tables in the html file soup
    
    #loop over tables
    for table in sunshine_tables:

        if len(table)>1:
            #loop over rows
            table_rows = table.find_all('tr') # Extract all rows in the current table
            for row in table_rows[1:]: # Skip the header row:
                table_cells = row.find_all('td') #Extract all cells (column) in the current row
                
                country = table_cells[country_position_in_sun_table].text.strip() # Extract country name based on the number of the column
                yearly_sun_hours = table_cells[sunshine_position_in_sun_table].text.split() # Extract sunshine duration
                yearly_sun_hours = process_num(yearly_sun_hours)
                monthly_sun_hours = yearly_sun_hours / 12 # Calculate monthly sunshine duration

                #record hours for every city in the country
                if country in country_sunshine:
                    country_sunshine[country].append(monthly_sun_hours)
                else : country_sunshine[country] = [monthly_sun_hours]
    
    #finally take the average for every country            
    for country in country_sunshine:
        country_sunshine[country] = round(np.average(country_sunshine[country]))
    return pd.DataFrame.from_dict(country_sunshine, orient='index', columns=['Monthly Sunshine Hours'])

df_sunshine = extract_monthly_sunshine_hours(sunshine_soup)
print(f'Extracted sunshine duration for {df_sunshine.shape[0]} countries.')
print(df_sunshine)

#Compare depression to sunshine
df_joined = df_depression.join(df_sunshine)
df_joined = df_joined[~df_joined.isnull().any(axis=1)]

print(f'Having both depression adn sunshine information for {df_joined.shape[0]} countries.')
print(df_joined.head())
df_joined.to_csv('depression_vs_sunshine.csv')

correlation = df_joined.corr().iloc[0,1]
sns.scatterplot(
    data=df_joined,
    x='DALY Rate',
    y='Monthly Sunshine Hours'
).set_title(f'Pearson Correlation : {correlation:5.2f})')

plt.show()

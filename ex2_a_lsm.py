import requests 
from datetime import date, timedelta
from bs4 import BeautifulSoup

#exercice 2_a_lsm

hp1_html = requests.get("https://www.themoviedb.org/movie/671")
print(hp1_html.status_code)
print(hp1_html.text[:500])  # Print the first 500 characters of the HTML content

lord_of_the_rings_html = requests.get("https://www.themoviedb.org/movie/120")
print(lord_of_the_rings_html.status_code)
print(lord_of_the_rings_html.text[:500])  # Print the first 500 characters of the HTML content

#exercice 2_b_lsm
latitude = 50.4549
longitude = 3.9518
tomorrow = date.today() #+ timedelta(days=1)
tomorrow_str=tomorrow.strftime('%Y-%m-%d')

url = (
    "https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    "&hourly=temperature_2m,precipitation"
    f"&start_date={tomorrow_str}&end_date={tomorrow_str}"
)

response = requests.get(url)
data=response.json()

temperature = data['hourly']['temperature_2m']
precipitation = data['hourly']['precipitation']
hours=data['hourly']['time']

print(f"Weather forecast for FUCAM campus on {tomorrow_str}: \n")

for t,temp,rain in zip(hours, temperature, precipitation):
    print(f"{t}: {temp}°C, precipitation = {rain} mm")

#exercice 2_c_lsm
soup_hp1 = BeautifulSoup(hp1_html.text, 'html.parser')
soup_lord_of_the_rings_html= BeautifulSoup(lord_of_the_rings_html.text, 'html.parser')

def get_synopsis_tmdb(movie_url):
        response = requests.get(movie_url)
        response.raise_for_status()  # Ensure we got a successful response

        soup = BeautifulSoup(response.text, 'html.parser')
        overview_div = soup.find('div', class_='overview')
        
        if not overview_div:
            return "Synopsis not found."
        p = overview_div.find('p')

        if not p:
            return "Synopsis not found."
        return p.get_text(strip=True)

hp1_synopsis = get_synopsis_tmdb("https://www.themoviedb.org/movie/671")
lord_of_the_rings_synopsis = get_synopsis_tmdb("https://www.themoviedb.org/movie/120")

print("\nHarry Potter and the Philosopher's Stone Synopsis:")
print(hp1_synopsis)
print("\nThe Lord of the Rings: The Fellowship of the Ring Synopsis:")
print(lord_of_the_rings_synopsis)
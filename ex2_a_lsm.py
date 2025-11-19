import requests 

hp1_html = requests.get("https://www.themoviedb.org/movie/671")
print(hp1_html.status_code)
print(hp1_html.text[:500])  # Print the first 500 characters of the HTML content

lord_of_the_rings_html = requests.get("https://www.themoviedb.org/movie/120")
print(lord_of_the_rings_html.status_code)
print(lord_of_the_rings_html.text[:500])  # Print the first 500 characters of the HTML content

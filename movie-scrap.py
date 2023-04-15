import csv
import requests
from bs4 import BeautifulSoup

# Set the URL for the first page of the movie listings
base_url = 'https://movies.yahoo.com.tw/movie_thisweek.html'
response = requests.get(url=base_url)

# Create a list to hold the data from each page
movie_data = []

# Parse the HTML content of the first page
soup = BeautifulSoup(response.text, 'lxml')
info_items = soup.find_all('div', 'release_info')

# Loop through the movies on the first page and extract their data
for item in info_items:
    name = item.find('div', 'release_movie_name').a.text.strip()
    english_name = item.find('div', 'en').a.text.strip()
    release_time = item.find('div', 'release_movie_time').text.split('：')[-1].strip()
    level = item.find('div', 'leveltext').span.text.strip()
    movie_data.append([name, english_name, release_time, level])
    print('{}({}) 上映日：{} 期待度：{}'.format(name, english_name, release_time, level))

# Get the total number of pages of movie listings
total_pages = int(soup.find('div', 'page_numbox').find_all('a')[-2].text)

# Loop through the remaining pages of movie listings and extract their data
for page_num in range(2, total_pages+1):
    # Construct the URL for the current page of movie listings
    current_url = f'{base_url}?page={page_num}'
    response = requests.get(url=current_url)
    soup = BeautifulSoup(response.text, 'lxml')
    info_items = soup.find_all('div', 'release_info')
    
    # Loop through the movies on the current page and extract their data
    for item in info_items:
        name = item.find('div', 'release_movie_name').a.text.strip()
        english_name = item.find('div', 'en').a.text.strip()
        release_time = item.find('div', 'release_movie_time').text.split('：')[-1].strip()
        level = item.find('div', 'leveltext').span.text.strip()
        movie_data.append([name, english_name, release_time, level])
        print('{}({}) 上映日：{} 期待度：{}'.format(name, english_name, release_time, level))

# Write the data to a CSV file
with open('movie_data.csv', 'w', encoding='utf-8', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['電影片名', '電影英文片名', '上映時間', '網友期待度'])
    for row in movie_data:
        csv_writer.writerow(row)

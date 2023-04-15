import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://movies.yahoo.com.tw/movie_thisweek.html'
response = requests.get(url=url)

soup = BeautifulSoup(response.text, 'lxml')

info_items = soup.find_all('div', 'release_info')

data = []

for item in info_items:
    name = item.find('div', 'release_movie_name').a.text.strip()
    english_name = item.find('div', 'en').a.text.strip()
    release_time = item.find('div', 'release_movie_time').text.split('：')[-1].strip()
    level = item.find('div', 'leveltext').span.text.strip()

    data.append([name, english_name, release_time, level])
    print('{}({}) 上映日：{} 期待度：{}'.format(name, english_name, release_time, level))

df = pd.DataFrame(data, columns=['電影片名', '電影英文片名', '上映時間', '網友期待度'])
df.to_excel('本週新片.xlsx', index=False, engine='xlsxwriter')

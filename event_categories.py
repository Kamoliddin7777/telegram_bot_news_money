import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
#------------------Послдение кинопремьеры--------------------
def get_movies():
    base_url='https://iticket.uz/ru'
    lst_movies=[]
    HEADER={
    'User-Agent':"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.3"
    }
    html=requests.get('https://iticket.uz/ru/events/concerts',headers=HEADER).text
    soup=BeautifulSoup(html,'html.parser')
    main=soup.find('div',class_='grid sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-10')
    events=main.find_all('a',class_='event-list-item')
    print(events)
    for event in events:
        title = event.get('title')
        link = 'https://www.iticket.uz' + event['href']
        data=event.find('div',class_='event-date').get_text(strip=True)
        img_tag=event.find('img',class_='bg')
        img_url = 'https://www.iticket.uz' + (img_tag.get('data-src') or img_tag.get('src'))
        print(img_url)


    # for block in blocks[:5]:
    #     title=block.find('h2',class_='itemTitle').get_text(strip=True).replace(' ',' ')
    #     content = block.find('div', class_='txt').get_text().replace(' ',' ')
    #     photo = block.find('img', 'lazy')
    #     photo=photo.get('data-src')
    #     phot_addres=urljoin(base_url,photo)
    #     data_time=block.find('div',class_='itemData').get_text(strip=True)
    #     day,rest = data_time.split(', ')
    #     time=rest[:5]
    #     new_data_time=f'{day}, {time}'
    #     link_tag=block.find('a')
    #     url=urljoin(base_url,link_tag['href']) if link_tag else base_url
    #
    #
    #     lst_movies.append({
    #         'title':title,
    #         'content':content,
    #         'photo':phot_addres,
    #         'data_time':new_data_time,
    #         'url':url
    #     })


get_movies()
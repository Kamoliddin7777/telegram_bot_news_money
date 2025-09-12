import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
def get_news(quantity):
    base_url='https://www.spot.uz/ru/'
    lst_news=[]
    HEADER={
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/139.0.0.0 Safari/537.36"
    }
    html=requests.get('https://www.spot.uz/ru/',headers=HEADER).text
    soup=BeautifulSoup(html,'html.parser')
    main=soup.find('div',class_='colp10-8')
    blocks=soup.find_all('div',class_='itemCols')
    for block in blocks[:quantity]:
        title=block.find('h2',class_='itemTitle').get_text(strip=True).replace(' ',' ')
        content = block.find('div', class_='txt').get_text().replace(' ',' ')
        photo = block.find('img', 'lazy')
        photo=photo.get('data-src')
        phot_addres=urljoin(base_url,photo)
        data_time=block.find('div',class_='itemData').get_text(strip=True)
        day,rest = data_time.split(', ')
        time=rest[:5]
        new_data_time=f'{day}, {time}'
        link_tag=block.find('a')
        url=urljoin(base_url,link_tag['href']) if link_tag else base_url


        lst_news.append({
            'title':title,
            'content':content,
            'photo':phot_addres,
            'data_time':new_data_time,
            'url':url
        })
    return lst_news







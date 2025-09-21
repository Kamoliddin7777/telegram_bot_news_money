import requests
from selenium import webdriver
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
#------------------Послдение кинопремьеры--------------------
def get_concerts():
    base_url='https://iticket.uz/ru'
    lst_concerts=[]

    HEADER={
    'User-Agent':"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.3"
    }
    html=requests.get('https://iticket.uz/ru/events/concerts',headers=HEADER).text
    soup=BeautifulSoup(html,'html.parser')
    blocks = soup.find_all('div',class_='content-container')
    concerts_container = blocks[2]
    concerts=concerts_container.find_all('a',class_='event-list-item')
    for concert in concerts[:5]:
        title = concert.get('title')
        link = base_url + concert.get('href')
        url = base_url + concert.get('href')
        img_tag = concert.find('img')
        img = img_tag.get('data-src')
        date = concert.find('div', class_='event-date').text.strip()
        venue = concert.find('div', class_='venue-name').text.strip()
        lst_concerts.append({
        'title': title,
        'url': url,
        'img': img,
        'date': date,
        'venue': venue
    })
    return lst_concerts
def get_teaters():
    base_url='https://iticket.uz/ru'
    lst_concerts=[]

    HEADER={
    'User-Agent':"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.3"
    }
    html=requests.get('https://iticket.uz/ru/events/theaters-tashkent',headers=HEADER).text
    soup=BeautifulSoup(html,'html.parser')
    blocks = soup.find_all('div',class_='content-container')
    concerts_container = blocks[2]
    concerts=concerts_container.find_all('a',class_='event-list-item')
    for concert in concerts[:5]:
        title = concert.get('title')
        link = base_url + concert.get('href')
        url = base_url + concert.get('href')
        img_tag = concert.find('img')
        img = img_tag.get('data-src')
        date = concert.find('div', class_='event-date').text.strip()
        venue_tag = concert.find('div', class_='venue-name')
        venue = venue_tag.text.strip() if venue_tag else "Место не указано"
        lst_concerts.append({
        'title': title,
        'url': url,
        'img': img,
        'date': date,
        'venue': venue
    })
    return lst_concerts

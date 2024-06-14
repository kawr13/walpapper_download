from typing import Tuple

import httpx
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from icecream import ic

from scrapping.config import date_dict

client = httpx.AsyncClient()
IMG_SIZE: Tuple[str] = ('1920x1080', '1920x1440', '1920x1200', '2560x1440')


async def get_soup(url):
    lst_url = []
    ic(url)
    response = await client.get(url)
    soup = bs(response.text, 'lxml')
    all_data = soup.find_all('ul')
    for i in all_data:
        urls = i.find_all('a')
        lst_url.extend([url_img.get('href') for url_img in urls if url_img.text in IMG_SIZE])

    ic(lst_url)
    return lst_url

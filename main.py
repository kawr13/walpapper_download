import asyncio
from scrapping.config import date_dict
from scrapping.dwnl_img import get_downloads
from scrapping.parser import get_soup
from multiprocessing import Process
import re

ACTIONS = {
    "1": get_soup,
}

URL = 'https://www.smashingmagazine.com/{}/{}/desktop-wallpaper-calendars-{}-{}/'
january = {
    'january': '12',
}

patterm = re.compile(r'\d{4} \d{2}')


def create_saync_process(url_list):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_downloads(url_list))


async def main():
    while True:
        action = input("Enter action ((1)download, (2)exit): ")

        if action == "2":
            break
        if action not in ACTIONS:
            print("Invalid action")
            continue
        else:
            text = input('укажите год месяц в виде цыфр\n (01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12) черех пробел (2024 05): ')
            math = re.match(patterm, text)
            if math is None:
                print("Invalid date")
                continue
            year, month = text.split(' ')
            year1 = year
            if date_dict.get(month) is None:
                print("Invalid month")
                continue
            month_str = date_dict[month]
            if january.get(month_str):
                month = january[month_str]
                year1 = str(int(year1) - 1)
            else:
                month = str(int(month) - 1)
                if len(month) == 1:
                    month = '0' + month
            url = URL.format(year1, month, month_str, year)
            soup = await ACTIONS[action](url)
            p = Process(target=create_saync_process, args=(soup,))
            p.start()


if __name__ == '__main__':
    asyncio.run(main())
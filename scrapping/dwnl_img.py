import asyncio, aiofiles
from typing import List
from pathlib import Path
import httpx
from icecream import ic
import sys

time_out = 30
FOLDER = 'images/'
client = httpx.AsyncClient(timeout=time_out)
min_size = 400 * 1024


async def sav_img(data: bytes, numbers: int):
    if Path(FOLDER).exists() is False:
        Path(FOLDER).mkdir()
    if len(data) < min_size:
        pass
    else:
        async with aiofiles.open(f'{FOLDER}{numbers}.jpg', mode='wb') as f:
            await f.write(data)


async def get_downloads(url_list: List[str]):
    task = [asyncio.create_task(client.get(url)) for url in url_list]
    response = await asyncio.gather(*task)
    task2 = [asyncio.create_task(sav_img(value.content, i)) for i, value in enumerate(response)]
    await asyncio.gather(*task2)
    ic('Done')

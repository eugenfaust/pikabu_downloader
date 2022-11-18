import re
import traceback

import aiohttp
from bs4 import BeautifulSoup


class PikabuParser:
    _headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/107.0.0.0 Safari/537.36'}

    def __init__(self, url):
        self.url = url
        self.bs = None

    async def load_content(self):
        s = aiohttp.ClientSession(headers=self._headers)
        try:
            response = await s.get(self.url)
        except Exception as e:
            raise Exception(f'Request error: {e}\nWith link: {self.url}')
        if response and response.status == 200:
            self.bs = BeautifulSoup(await response.text(), 'html.parser')

        await s.close()
        if not self.bs:
            raise Exception(f'Bad response: {response.status}')

    async def parse_title(self):
        if not self.bs:
            await self.load_content()
        try:
            return self.bs.find('span', class_='story__title-link').text
        except Exception as e:
            raise Exception(f'Can\'t find title on link: {self.url}')

    async def parse_video(self):
        if not self.bs:
            await self.load_content()
        try:
            player = self.bs.find('div', {'class': 'player', 'data-type': 'video-file'})
            res = player['data-source'] + '.mp4'
            duration = int(player['data-duration'])
            async with aiohttp.ClientSession(headers=self._headers) as s:
                resp = (await s.head(res)).headers['Content-Length']
            return res, int(resp), duration
        except Exception as e:
            raise Exception(f'Video parsing error: {traceback.format_exc()}\nWith link: {self.url}')

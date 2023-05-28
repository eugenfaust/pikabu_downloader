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

    async def parse_content(self):
        if not self.bs:
            await self.load_content()
        story = self.bs.find('div', class_='story__content-inner')
        blocks = story.find_all('div', class_='story-block')
        for b in blocks:
            classes = b.get('class')
            if 'story-block_type_text' in classes:
                print(b.find('p').text)
            elif 'story-block_type_image' in classes:
                print(b.find('a')['href'])
            elif 'story-block_type_video' in classes:
                print(b.find('div', {'class': 'player', 'data-type': 'video-file'})['data-source'])
            else:
                print(b)


    async def parse_title(self):
        if not self.bs:
            await self.load_content()
        try:
            return self.bs.find('span', class_='story__title-link').text
        except Exception as e:
            raise Exception(f'Can\'t find title on link: {self.url}')

    async def parse_images(self):
        if not self.bs:
            await self.load_content()
        links = []
        try:
            story = self.bs.find('div', class_='page-story__story')
            images = story.find_all('div', class_='story-image__content')
            for img in images:
                try:
                    links.append(img.find('a', class_='image-link')['href'])
                except Exception as e:
                    continue
        except Exception as e:
            raise Exception(f'Can\'t find images on link: {self.url}')
        return links

    async def parse_video(self):
        if not self.bs:
            await self.load_content()
        try:
            story = self.bs.find('div', class_='page-story__story')
            player = story.find('div', {'class': 'player', 'data-type': 'video-file'})
            if not player:
                return None, None, None
            res = player['data-source'] + '.mp4'
            duration = int(player['data-duration'])
            async with aiohttp.ClientSession(headers=self._headers) as s:
                resp = (await s.head(res)).headers['Content-Length']
            return res, int(resp), duration
        except Exception as e:
            raise Exception(f'Video parsing error: {traceback.format_exc()}\nWith link: {self.url}')

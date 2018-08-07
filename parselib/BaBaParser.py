# -*- coding: utf-8 -*-
# !/usr/bin/python3
from pyquery import PyQuery as pq
import urllib
from parselib.parser import Parser
import parselib.book as bk
import aiohttp

class BaBaParser(Parser):

    def __init__(self, name, option):
        super().__init__(name, option)
        self.parser_name = '八八'
        self.search_root_url = 'https://www.88dus.com/search/so.php?search_field=0&q='

    def search_parser(self, search_url):
        name = None
        url = None
        a = pq(search_url)('.block_txt')('p')('a')
        name = a('h2').text()
        url = 'https://www.88dus.com' + a.attr('href')
        book = bk.Book()
        book.url = url
        book.name = name
        return book

    def chapter_list_parser(self, book_url):
        chapter_eles = pq(url=book_url, encoding='gbk')('.mulu')('li').items()
        chapter_list = []
        for chapter_ele in chapter_eles:
            name = chapter_ele('a').text()
            url = urllib.parse.urljoin(book_url, chapter_ele('a').attr('href'))
            if not name:
                continue
            chapter = bk.Chapter()
            chapter.name = name
            chapter.url = url
            chapter_list.append(chapter)
        return chapter_list

    async def chapter_parser(self, chapter_url):
        async with aiohttp.request('GET', url=chapter_url) as response:
            response_str = await response.text(encoding='gbk', errors='ignore')
            # print(response_str)
            ele = pq(response_str)('.yd_text2')
            # ele = pq(url=chapter_url, encoding='gbk')('.yd_text2')
            content = ele.html().replace('&#13;', '')
            # print(content)
            return content

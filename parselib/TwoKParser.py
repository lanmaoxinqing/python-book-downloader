# -*- coding: utf-8 -*-
# !/usr/bin/python3
from pyquery import PyQuery as pq
import urllib
from parselib.parser import Parser
import parselib.book as bk
import aiohttp

class TwoKParser(Parser):

    def __init__(self, name, option):
        super().__init__(name, option)
        self.parser_name = '2K'
        self.search_root_url = 'https://www.2kxs.com/modules/article/search.php?searchtype=keywords&searchkey='

    def search_url(self):
        return self.search_root_url + urllib.parse.quote(self.keyword.encode('gbk'))

    def search_parser(self, search_url):
        name = None
        url = None
        html = pq(search_url,encoding='gbk')
        a = html('.odd')('a')
        #搜索结果,递归解析到封面页
        if a:
            tmp_url = a.attr('href')
            return self.search_parser(tmp_url)
        #直接进封面页
        else:
            a = html("#title")('h2')('a')
            name = a.html()
            url = a.attr('href')
        book = bk.Book()
        book.url = url
        book.name = name
        return book

    def chapter_list_parser(self, book_url):
        html = pq(url=book_url, encoding='gbk')('.book')('dd')
        chapter_eles = html.items()
        chapter_list = []
        for index, chapter_ele in enumerate(chapter_eles):
            # 略过最新章节头
            if index < 4:
                continue
            name = chapter_ele('a').text()
            url = urllib.parse.urljoin(book_url, chapter_ele('a').attr('href'))
            if not name:
                continue
            chapter = bk.Chapter()
            chapter.name = name
            chapter.url = url
            chapter_list.append(chapter)
        return chapter_list

    def chapter_parser(self, chapter_url):
        ele = pq(url=chapter_url, encoding='gbk')('.Text')
        ele('a').remove()
        ele('font').remove()
        ele('strong').remove()
        ele('script').remove()
        content = ele.html()\
            .replace('&#13;', '')\
            .replace('<br>', '\n')\
            .replace('2k小说阅读网', '')
        # print(content)
        return content


    async def chapter_parser(self, chapter_url):
        async with aiohttp.request('GET', url=chapter_url) as response:
            response_str = await response.text(encoding='gbk', errors='ignore')
            # print(response_str)
            ele = pq(response_str)('.Text')
            ele('a').remove()
            ele('font').remove()
            ele('strong').remove()
            ele('script').remove()
            content = ele.html() \
                .replace('&#13;', '') \
                .replace('<br>', '\n') \
                .replace('2k小说阅读网', '')
            # print(content)
            return content


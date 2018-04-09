# -*- coding: utf-8 -*-
# !/usr/bin/python3
from pyquery import PyQuery as pq
from html import escape
import urllib
from parselib.parser import Parser
import parselib.book as bk


class BiQuParser(Parser):

    def __init__(self, name, option):
        super().__init__(name, option)
        self.parser_name = '笔趣'
        self.search_root_url = 'http://zhannei.baidu.com/cse/search?s=1393206249994657467&q='

    def search_parser(self, search_url):
        name = None
        url = None
        a = pq(search_url,encoding='utf-8')('.result-game-item-title-link')('a')
        name = a.attr('title')
        url = a.attr('href')
        book = bk.Book()
        book.url = url
        book.name = name
        return book

    def chapter_list_parser(self, book_url):
        chapter_eles = pq(book_url,encoding='utf-8')('dd').items()
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

    def chapter_parser(self, chapter_url):
        ele = pq(chapter_url,encoding='utf-8')('#content')
        ele('script').remove()
        content = ele.html().replace('&#13;', '')
        # print(content)
        return content

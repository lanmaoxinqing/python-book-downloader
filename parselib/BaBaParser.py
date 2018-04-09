# -*- coding: utf-8 -*-
# !/usr/bin/python3
from pyquery import PyQuery as pq
from html import escape
import urllib
from parselib.Parser import Parser


class BaBaParser(Parser):
    def displayName(self):
        return '八八'

    def searchURL(self):
        return 'https://www.88dus.com/search/so.php?search_field=0&q=+'

    def searchParser(self, searchURL):
        print ("搜索URL\n" + searchURL)
        name = None
        url = None
        a = pq(searchURL)('.block_txt')('p')('a')
        name = a('h2').text()
        url = 'https://www.88dus.com' + a.attr('href')
        return [name, url]

    def chapterListParser(self, bookURL):
        chapterEles = pq(url=bookURL, encoding='gbk')('.mulu')('li').items()
        chapterNames = []
        chapterURLs = []
        for chapterEle in chapterEles:
            chapterName = chapterEle('a').text()
            chapterURL = urllib.parse.urljoin(bookURL, chapterEle('a').attr('href'))
            if not chapterName:
                continue
            chapterNames.append(chapterName)
            chapterURLs.append(chapterURL)

        return [chapterNames, chapterURLs]

    def chapterParser(self, chapterURL):
        contentEle = pq(url=chapterURL, encoding='gbk')('.yd_text2')
        content = contentEle.html().replace('&#13;', '')
        # print (content)
        return content

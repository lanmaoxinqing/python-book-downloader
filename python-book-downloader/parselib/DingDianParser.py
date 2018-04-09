# -*- coding: utf-8 -*-
#!/usr/bin/python3
from pyquery import PyQuery as pq
from html import escape
import urllib
from parselib.Parser import Parser

class DingDianParser(Parser):
    def displayName(self) :
        return '顶点'

    def searchURL(self):
        return 'http://zhannei.baidu.com/cse/search?s=1682272515249779940&q='

    def searchParser(self, searchURL):
        print ("搜索URL\n" + searchURL)
        name = None
        url = None
        for a in pq(searchURL)('.result-game-item-title-link').items() :
            name = a.attr('title')
            url = a.attr('href')
            break
        return [name,url]

    def chapterListParser(self, bookURL):
        chapterEles = pq(bookURL)('dd').items()
        chapterNames = []
        chapterURLs = []
        for chapterEle in chapterEles :
            chapterName = chapterEle('a').text()
            chapterURL = urllib.parse.urljoin(bookURL, chapterEle('a').attr('href'))
            if not chapterName :
                continue
            chapterNames.append(chapterName)
            chapterURLs.append(chapterURL)

        return [chapterNames, chapterURLs]


    def chapterParser(self, chapterURL):
        contentEle = pq(chapterURL)('#content')
        contentEle('script').remove()
        content = contentEle.html()
        # print (content)
        return content

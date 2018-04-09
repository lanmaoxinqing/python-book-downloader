# -*- coding: utf-8 -*-
#!/usr/bin/python3
import os
from pyquery import PyQuery as pq
from html import escape
import urllib
import shutil
import copy

class Parser:

    def displayName(self):
        return '未知'

    def searchURL(self):
        return 'http://zhannei.baidu.com/cse/search?s=1393206249994657467&q='

    def folderPath(self):
        return self.bookName

    def pathForChapterAtIndex(self, i):
        return self.folderPath() + '/' + str(i).zfill(5)

    def searchParser(self, searchURL):
        pass

    def chapterListParser(self, bookURL):
        pass

    def chapterParser(self, chapterURL):
        pass

    def saveChapter(self, path, content):
        file = open(path, 'a')
        file.write(content)
        file.close()

    def merge(self):
        book = open(self.bookName + '.txt', 'w')
        for fileName in os.listdir(self.folderPath()) :
            # print (fileName)
            file = open(self.folderPath() + '/' + fileName, 'r')
            book.write(file.read() + '\n')
            file.close()
        book.close()
        shutil.rmtree(self.folderPath())


    def start(self, name, option):
        if option == 0 :
            self.bookName = name
            searchURLStr = self.searchURL() + urllib.parse.quote(name)
            bookEle = self.searchParser(searchURLStr)
            bookName = bookEle[0]
            bookURL = bookEle[1]
            if bookName :
                print (bookName + '\n' + bookURL)
            if not bookURL or not bookName == name:
                print ("未找到指定小说")
                return
        else :
            self.bookName = name.replace('/', '')
            bookURL = name

        if not os.path.exists(self.folderPath()) :
            os.makedirs(self.folderPath())

        chapterListEle = self.chapterListParser(bookURL)
        chapterNames = copy.deepcopy(chapterListEle[0])
        chapterURLs = copy.deepcopy(chapterListEle[1])
        count = len(chapterNames)
        #章节去重
        lastName = None
        for i in range(count) :
            name = chapterListEle[0][i]
            if not lastName or lastName != name :
                lastName = name
            else :
                chapterNames.pop(i)
                chapterURLs.pop(i)

        print ('最新章节:' + chapterNames[-1])

        count = len(chapterNames)
        for i in range(count) :
            filePath = self.pathForChapterAtIndex(i)
            chapterName = chapterNames[i]
            chapterURL = chapterURLs[i]
            if os.path.exists(filePath) :
                print (chapterName+'(' + str(i) + '/' + str(count) + ')已存在')
                continue
            content = self.chapterParser(chapterURL)
            content = content.replace('<br />', '\n')
            content = content.replace('<br/>', '\n')
            print ('正在保存' + chapterName + '(' + str(i) + '/' + str(count) + ')')
            self.saveChapter(filePath, chapterName + '\n' + content)
        #删除预览文件
        dsFile = self.folderPath() + '/.DS_Store'
        if os.path.exists(dsFile) :
            os.remove(dsFile)
        if len(os.listdir(self.folderPath())) >= len(chapterURLs) :
            print ('正在合并')
            self.merge()

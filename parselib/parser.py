# -*- coding: utf-8 -*-
# !/usr/bin/python3
import os
from pyquery import PyQuery as pq
from html import escape
import urllib
import shutil
import copy
import parselib.book as bk


class Parser:

    download_root_directory = './Downloads/'
    parser_name = '未知'
    search_root_url = ''

    def __init__(self, name, option):
        self.keyword = name
        self.option = option
        self.book = None
        # 创建目录
        if not os.path.exists(Parser.download_root_directory):
            os.makedirs(Parser.download_root_directory)

    def start(self):
        if self.option == 0:
            search_url_str = self.search_url()
            print('搜索URL\n'+search_url_str)
            self.book = self.search_parser(search_url_str)
            if not self.book:
                print("搜索失败")
                return
            if self.book.name != self.keyword:
                print("未找到指定小说")
                print(self.book.name)
                print(self.book.url)
                return
            else:
                print(self.book.name + '\n' + self.book.url)
        else:
            self.book = bk.Book()
            self.book.name = keyword.replace('/', '')
            self.book.url = keyword

        if not os.path.exists(self.download_temp_path()):
            os.makedirs(self.download_temp_path())
        # 解析章节目录
        self.book.chapter_list = self.chapter_list_parser(self.book.url)
        # 章节去重
        self.book.dereplication()
        print('最新章节:' + self.book.chapter_list[-1].name)
        count = len(self.book.chapter_list)
        # 下载章节
        for i in range(count):
            chapter_path = self.path_for_chapter_at_index(i)
            chapter = self.book.chapter_list[i]
            chapter.path = chapter_path
            # 文件检查
            if os.path.exists(chapter_path):
                print(chapter.name+'(' + str(i + 1) + '/' + str(count) + ')已存在')
                continue
            content = self.chapter_parser(chapter.url)
            content = content.replace('<br />', '\n')
            content = content.replace('<br/>', '\n')
            chapter.content = content
            print('正在保存' + chapter.name + '(' + str(i + 1) + '/' + str(count) + ')')
            self.save_chapter(chapter)
        # 删除预览文件
        ds_file = self.download_temp_path() + '.DS_Store'
        if os.path.exists(ds_file):
            os.remove(ds_file)
        # 全部章节下载完成后,合并
        if len(os.listdir(self.download_temp_path())) >= len(self.book.chapter_list):
            print('正在合并')
            self.merge(self.book)

    # tools
    def search_url(self):
        return self.search_root_url + urllib.parse.quote(self.keyword)

    def download_temp_path(self):
        return self.download_root_directory + self.book.name + '/'

    def path_for_chapter_at_index(self, i):
        return self.download_temp_path() + str(i).zfill(5)

    def search_parser(self, search_url):
        return self.book

    def chapter_list_parser(self, book_url):
       return self.book.chapter_list

    def chapter_parser(self, chapter_url):
        return ''

    def save_chapter(self, chapter):
        file = open(chapter.path, 'a')
        file.write(chapter.content)
        file.close()

    def merge(self, book):
        file = open(Parser.download_root_directory + book.name + '.txt', 'w')
        for chapter in book.chapter_list:
            content = open(chapter.path)
            file.write(chapter.name + '\n' + content.read() + '\n')
        file.close()
        shutil.rmtree(self.download_temp_path())


# -*- coding: utf-8 -*-
# !/usr/bin/python3


class Book:
    url = ''
    name = ''
    chapter_list = []

    def __init__(self):
        pass

    def dereplication(self):
        last_name = None
        result = []
        for i in range(len(self.chapter_list)):
            chapter = self.chapter_list[i]
            name = chapter.name
            if not last_name or last_name != name:
                last_name = name
                result.append(chapter)
        self.chapter_list = result


class Chapter:
    url = ''
    name = ''
    path = ''

    def __init__(self):
        pass

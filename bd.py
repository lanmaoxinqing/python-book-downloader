# -*- coding: utf-8 -*-
#!/usr/bin/python3
from parselib import BiQuParser
from parselib import DingDianParser
from parselib import BaBaParser
import sys
import argparse

parser_list = [
    'BaBaParser',
    'BiQuParser',
    'DingDianParser',
    'TwoKParser',
]

def create_instance(module_name, class_name, *args, **kwargs):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj


opt_parser = argparse.ArgumentParser()
opt_parser.add_argument('name', help='书名或URL')
opt_parser.add_argument('-n', help='书名或URL', dest='name')
opt_parser.add_argument('-c', help='0八八, 1笔趣, 2顶点, 3 2K,', dest='channel')
opt_parser.add_argument('-opt', help='0书名, 1URL', dest='option')

args = opt_parser.parse_args()
keyword = args.name
channel = 0 if not args.channel else args.channel
option = 0 if not args.option else args.option
# print(keyword, channel, option)

parser_name = parser_list[int(channel)]
parser = create_instance('parselib.' + parser_name, parser_name, keyword, option)

# print(parser.parser_name)
parser.start()


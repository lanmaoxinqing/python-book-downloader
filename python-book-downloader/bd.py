# -*- coding: utf-8 -*-
#!/usr/bin/python3
from parselib import BiQuParser
from parselib import DingDianParser
from parselib import BaBaParser
import sys
import argparse

parserList = [
    'BaBaParser',
    'BiQuParser',
    'DingDianParser',
]

def parserByName(className) :
    module = __import__('parselib')
    parserModule = getattr(module, className)
    # print (parserModule)
    parser = getattr(parserModule, className)()
    # print (parser)
    return parser


optParser = argparse.ArgumentParser()
optParser.add_argument('name', help = '书名或URL')
optParser.add_argument('-n', help = '书名或URL', dest = 'name')

optParser.add_argument('-c', help = '0八八, 1笔趣, 2顶点', dest = 'channel')

optParser.add_argument('-opt', help = '0书名, 1URL', dest = 'option')

args = optParser.parse_args()
bookName = args.name
parserType = 0 if not args.channel else args.channel
option = 0 if not args.option else args.option
print (bookName, parserType, option)

parserName = parserList[int(parserType)]
parser = parserByName(parserName)
print (parser.displayName())

parser.start(bookName, option)



# bookName = sys.argv[1]
# parserType = 0
# if len(sys.argv) > 2 :
#     parserType = str(sys.argv[2])
#
#
# try :
#     parser.start(bookName)
# except :
#     parser.start(bookName)

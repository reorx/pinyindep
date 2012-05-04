#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pymongo import Connection


conn = Connection()


def rerecord():
    conn.drop_database('chinesecode')
    with open('Uni2Pinyin', 'r') as f:
        for i in f:
            if i.startswith('#'):
                continue
            i = i[:-1]
            mapList = i.split('\t')
            print mapList
            if len(mapList) == 0:
                continue
            code = mapList.pop(0)
            char = eval("u'\u" + code + "'")
            doc = {
                'code': code,
                'ord': ord(char)
            }
            if len(mapList) > 0:
                doc['pinyins'] = mapList
            else:
                doc['pinyins'] = []
            print doc
            conn.chinesecode.uni2pinyin.insert(doc, safe=True)

def explore():
    for i in conn.chinesecode.uni2pinyin.find():
        print i['code'], i['ord'], i['pinyins']

def backup():
    os.popen('mongodump -d chinesecode -o chinesecode')
    os.popen('tar czf chinesecode.tar.gz chinesecode')
    os.popen('mv chinesecode.tar.gz ~/Dropbox/nodemix/dev/')
    os.popen('rm chinesecode* -rf')

if __name__ == '__main__':
    print 'what do you want to do?'
    act = raw_input()
    if act == 'rerecord':
        rerecord()
    elif act == 'explore':
        explore()
    elif act == 'backup':
        backup()

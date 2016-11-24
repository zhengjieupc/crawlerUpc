#!/usr/bin/env python
# -*- encoding:utf-8 -*-

'''获取638台设备的设备name和id号
作用:爬出分类页面的资源url，获取name和id
更新频率：仅更新一次，除非设备发生变动或是担心设备发生变动
xpath:u"//li[@class='Equipment-Name']/a[@id='EquipmentName']/@onclick"
url:http://dxyqsb.upc.edu.cn/Equipment/PaginationList?ShowType=Icon&isHome=true&isManage=false&isOpen=true&order=asc&page=1&rows=6&sort=Name&date=Fri%20Nov%2018%202016%2023:28:30%20GMT%200800
'''

import re
import requests
import sys
from lxml import etree
import os
import json
import sys
import chardet


def getHtml(html,idlistfileName):
    novelcontent = requests.get(html).content
    source= etree.HTML(novelcontent)
    listname = source.xpath(u"//li[@class='Equipment-Name']/a[@id='EquipmentName']/@onclick")
    if len(listname)<=600:print '获取id的函数有问题，可能是网络延时，获取到了%d个id' %(len(listname))
    fd=open(idlistfileName,'w')
    fd.write(json.dumps(listname))
    fd.close()

def cleanData(listtr):
    nameid=set()
    for line in listtr:
        lst=re.split(r',',re.search(r'\((.*)\)',line).group(1))
        id=lst[0].strip("'")
        nameid.add(id)
    return nameid

if __name__=='__main__':
    #url有用参数解释：date 时间  rows展现多少内容，此处直接638
    url="http://dxyqsb.upc.edu.cn/Equipment/PaginationList?ShowType=Icon&isHome=true&isManage=false&isOpen=true&order=asc&page=1&rows=638&sort=Name&date=Fri%20Nov%2018%202016%2023:28:30%20GMT%200800"
    idlistfileName=os.getcwd()+'/../data/idlist'
    idfileName=os.getcwd()+'/../data/id'
    #获取id和html，并且存入idlistfilename
#    getHtml(url,idlistfileName)
    fd=open(idlistfileName,'r')
    namestr=json.loads(fd.read())
    fd.close()
    nameid=cleanData(namestr)
    if os.path.exists(idfileName):
        os.remove(idfileName)
    fd=open(idfileName,'w')
    print '一共获取了%d个id' %(len(nameid))
    fd.write(json.dumps(list(nameid)))
    fd.close()

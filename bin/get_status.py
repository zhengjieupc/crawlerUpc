#!/usr/bin/env python
# -*- encoding:utf-8 -*-


import Queue
import json
import requests
import sys
from lxml import etree
import os
import threading
import time

def getid(filename):
    with open(filename,'r') as fd:
        return json.loads(fd.read())

def getstatus(url,id,status,statuscount):
    url=url+id
    time.sleep(6)
    #dict=json.loads(requests.request(url))
    dict={"EquipmentStatus":1}
    EquipmentStatus=dict["EquipmentStatus"]
    status[id]=EquipmentStatus
    if EquipmentStatus in statuscount:
        statuscount[EquipmentStatus]=statuscount[EquipmentStatus]+1
    else:
        statuscount[EquipmentStatus]=1

if __name__=='__main__':
    #url有用参数解释：id为id号，date设置成默认的201 需要观察是否会随着时间变化
    num=sys.argv[1]
    start=time.clock()
    url="http://dxyqsb.upc.edu.cn/Equipment/GetEquipmentCurStatusInfo?date=201&Id="
    idfileName=os.getcwd()+'/../data/id'
    idlist=getid(idfileName)
    status={}
    statuscount={}
    threads=Queue.Queue()
    for id in idlist:
        threads.put(threading.Thread(target=getstatus, args=(url,id,status,statuscount,)))
    while (not threads.empty()):
        try:
            active_count=threading.active_count()
        except:
            active_count=0
        cur_active=int(num)-int(active_count)
        if cur_active>0:
            tmp=Queue.Queue()
            for i in range(cur_active):
                t=threads.get()
                t.start()
                print threading.active_count()
                tmp.put(t)
            # 主线程中等待所有子线程退出
            for i in range(int(num)-int(active_count)):
                tmp.get().join()
#    print status
#    print statuscount
    end=time.clock()
#    print "read: %f s" % (end - start)
        

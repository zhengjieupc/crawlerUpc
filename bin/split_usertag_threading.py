#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import Queue
import sys
import threading
import time
import os

'''
python this,py $BASE_DIR/../data/user_tag $BASE_DIR/../user_tag_data
python split_usertag_threading.py  /home/datamining/data/zhengjie/Recommend/threading_test /home/datamining/data/zhengjie/Recommend/result_test 3
用于更快的分解特征矩阵到不同的数据目录下面
基础方法:
/home/datamining/data/zhengjie/Recommend/threading_test/x00 供多线程读入的split的数据

'''

def makeQueue(user_tag_file_dir):
    tmp=Queue.Queue()
    for filename in os.listdir(user_tag_file_dir):
        tmp.put(user_tag_file_dir+'/'+filename)
    return tmp

def main(user_tag_file_dir,filedir,num):
    threads = Queue.Queue()
    fileQueue=makeQueue(user_tag_file_dir)
    while (not fileQueue.empty()):
        user_tag_file=fileQueue.get()
        # 先创建线程对象
        threads.put(threading.Thread(target=split_data, args=(user_tag_file,filedir,)))
    # 每次只启动5个线程,threading.active_count():
    while (not threads.empty()):
        try:
            active_count=threading.active_count()
        except:
            active_count=0
        tmp=Queue.Queue()
        for i in range(int(num)-int(active_count)):
            t=threads.get()
            t.start()
            print threading.active_count()
            tmp.put(t)
        # 主线程中等待所有子线程退出
        for i in range(int(num)-int(active_count)):
            tmp.get().join()
        #print threading.active_count()
        time.sleep(4)

def split_data(user_tag_file,filedir):
    fd=open(user_tag_file)
    for line in fd:
        list=line.strip('\n').split('\t')
        if len(list)!=2:continue
        username,tagjson=list
        filename=filedir+'/'+sign_username(username)
        writefile(filename,username,tagjson)

def writefile(filename,username,tagjson):
    fd=open(filename,'a')
    fd.write(username+'\t'+tagjson+'\n')

def sign_username(username):
    sign=str(username)[-4:]
    try:
        int(sign)
        return sign
    except:
        return "capital_name"

if __name__=="__main__":
    user_tag_file,filedir,num=sys.argv[1:]
    main(user_tag_file,filedir,num)

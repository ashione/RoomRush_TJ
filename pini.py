#!/usr/bin/python
# -*- coding:utf-8 -*-
#desc: use to read ini

import sys,os,time
import ConfigParser


class Config:
    def __init__(self, path):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)
    def get(self, field, key):
        result = ""
        try:
            result = self.cf.get(field, key)
        except:
            result = ""
        return result
    def set(self, filed, key, value):
        try:
            self.cf.set(field, key, value)
            cf.write(open(self.path,'w'))
        except:
            return False
        return True
            
            

def read_config(config_file_path, field, key): 
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        result = cf.get(field, key)
    except:
        sys.exit(1)
    return result

def write_config(config_file_path, field, key, value):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        cf.set(field, key, value)
        cf.write(open(config_file_path,'w'))
    except:
        sys.exit(1)
    return True

if __name__ == "__main__":
    config_file_path = 'data.ini'
    id = read_config(config_file_path,'USERINFO','id')
    pwd = read_config(config_file_path,'USERINFO','pwd')
    roomNum = int(read_config(config_file_path,'ROOM','roomNum'))
    mylist = []
    for i in range(1,roomNum):
        temp = read_config(config_file_path,'ROOM','room'+str(i)).split(':')
        mylist.append(temp)

    print 'your id and password are %s,%s' %(id,pwd),'\nu choice list is ',mylist


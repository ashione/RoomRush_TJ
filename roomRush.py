#!/usr/bin/python
# -*- coding: utf8 -*-
import urllib2
import urllib
import cookielib
import pini
from time import sleep,ctime
class RoomRush:
	cookiejar=cookielib.CookieJar()
	urlopener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
	urllib2.install_opener(urlopener)

	urlopener.addheaders.append(('Referer', 'http://zcc.tongji.edu.cn/index.portal'))
	urlopener.addheaders.append(('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2'))
	urlopener.addheaders.append(('Host', 'zcc.tongji.edu.cn'))
	urlopener.addheaders.append(('User-Agent', 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0'))
	urlopener.addheaders.append(('Connection', 'Keep-Alive'))
        config_file_path = 'data.ini'
        id = ''
        pwd = ''
        gender = 'MALE'
        campus = 'JIADINGCAMPUS'
        mylist = []
        LY = {}
        tryNum = 0
        def __init__(self,config_file_path='data.ini'):
            self.config_file_path = config_file_path

	def login(self):
	    #values={'Login.Token1':username, 'Login.Token2':password}
	    values={'IDToken1':self.id, 'IDToken2':self.pwd}
	    url = 'http://tjis.tongji.edu.cn:58080/amserver/UI/Login?goto=http://zcc.tongji.edu.cn/index.portal&gotoOnFail=http://zcc.tongji.edu.cn/index.portal?.flag=fail'
	    print 'Now Login...'
	    while True:
		try:
		    urlcontent=self.urlopener.open(urllib2.Request(url, urllib.urlencode(values)))
		except urllib2.URLError :
		    print 'Request time out,now try again!'
		    sleep(1)
		    continue
		if urlcontent.getcode() == 200:
		    break
		else:
		    print 'return code is %d ,now try again' % urlcontent.getcode()
		    sleep(1)
	    
	    if urlcontent.geturl().endswith('fail'):
		print 'Login failed with username=%s,password=%s' % (self.id, self.pwd)
		return False
	    else:
		print 'Login succeeded!'
		return True

	def apply(self):
	    url = 'http://zcc.tongji.edu.cn/detach.portal?.pa=aT1QMzM4ODE4JnQ9YSZzPW1heGltaXplZCZtPXZpZXc%3D&act=save&extInfo=1'
	    for choice in self.mylist:
		values = {'buildingID':self.LY[choice[0]],'doorPlate':choice[1]}
		while True:
		    try:
		        urlcontent=self.urlopener.open(urllib2.Request(url,urllib.urlencode(values)))
		    except urllib2.URLError:
		        print 'Error,Request time out,now try again afer 2 seconds'
		        sleep(1)
		        continue
		    if urlcontent.getcode() == 200:
		        break
		    else:
		        print 'return code is %d ,now try again' % urlcontent.getcode()
		        sleep(1)
		page = urlcontent.read(5000)
		print page
		if page.find('其它房间') >=0 :
		    print 'roomID is invalid!'
		elif page.find('不能重复申请') >=0 :
		    print 'you have done,please no repeat!'
		elif page.find('不能申请') >=0 :
		    print 'unpermit,choose invalid!'
		elif page.find('直接登录') >=0 :
			print 'Statement:Logout,Now,try to login again!'
			if self.login(): 
				print 'Logined! Resume Choosing!'
			
		else:
		    print 'Choose success!!! buildingname:%s,roomID:%s' %(choice[0],choice[1])
		       #print page
		    break
		print 'buildingname:%s,roomID:%s Choose failed,Now try next...' %(choice[0],choice[1])
	# inputparam :
	#            gender: user gender,MALE or FEMALE
	#            campus: default campus is JIADINGCAMPUS
	# outputparam:
	#            buildingList:avaliable buidling
	def getBuildingInfo(self,gender = 'MALE',campus= 'JIADINGCAMPUS' ):
	    buildingNum = int(pini.read_config(self.config_file_path,campus+gender,'buildingnum'))
	    buildingList= []
	    for i in range(1,buildingNum+1):
		temp = pini.read_config(self.config_file_path,campus+gender,'building'+str(i)).split(':')
		buildingList.append(temp)
	    return buildingList

	# inputparam : None,but user should set config_file_path at first
	# outputparam:
	#            id:userid
	#            pwd:userpassword
	#            mylist:Being post room data of user
	def getUserInfo(self):
	    self.id = pini.read_config(self.config_file_path,'USERINFO','id')
	    self.pwd = pini.read_config(self.config_file_path,'USERINFO','pwd')
	    roomNum = int(pini.read_config(self.config_file_path,'ROOM','roomNum'))
	    self.campus = pini.read_config(self.config_file_path,'USERINFO','campus')
	    self.gender = pini.read_config(self.config_file_path,'USERINFO','gender');
            self.mylist = []
	    for i in range(1,roomNum+1):
		temp = pini.read_config(self.config_file_path,'ROOM','room'+str(i)).split(':')
		self.mylist.append(temp)

        def loadData(self):
	    print 'loading data!'
	    self.getUserInfo()
	    self.LY = dict(self.getBuildingInfo(self.gender,self.campus))
	def run(self):
		print ctime()
		while True:
		        RoomRush.tryNum = RoomRush.tryNum+1
		        print 'we have tried %d,now launching %d' %(RoomRush.tryNum-1,RoomRush.tryNum)
		        self.apply()
		print ctime()

if __name__ == '__main__':
    rush = RoomRush() 
    rush.loadData()
    if rush.login():
        rush.run()

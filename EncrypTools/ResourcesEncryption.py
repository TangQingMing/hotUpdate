# -*- coding: utf-8 -*-
import os  
import sys  
import codecs  
#import chardet
import shutil
import json
import zipfile
import platform
systemType=platform.system()
if systemType=="Windows":
    systemName="ANDROID"
elif systemType=="Darwin":
    systemName="IOS"

def AddPath(first, second):
    return first + '/' + second

#初始化配置文件
def InitConfigJosn():
	global configJson
	if systemType=="Windows":
		CONFIG_PATH='e:/hotUpdate/EncrypTools'
	elif systemType=="Darwin":
		CONFIG_PATH='/Users/tuoshuai/Downloads/EncrypTools'
	file=open(CONFIG_PATH+"/config.json",'r')
	jObj=file.read()
	jObj=jObj.decode("utf-8-sig")
	configJson=json.loads(jObj)
	configJson["SECRET_KEY"]=configJson["SECRET_KEY"]["ANDROID"]
	configJson["SIGNATURE"]=configJson["SIGNATURE"]["ANDROID"]
	configJson["RESOURCES_PATH"]=AddPath(configJson["IN_ROOT_DIRECTORY"],configJson["RESOURCES_PATH"])
	tempStr=configJson["RESOURCES_OUT_PATH"]
	configJson["RESOURCES_OUT_PATH"]={}
	configJson["RESOURCES_OUT_PATH"]["ANDROID"]=AddPath(configJson["OUT_ROOT_DIRECTORY"]["ANDROID"],tempStr)
	configJson["RESOURCES_OUT_PATH"]["IOS"]=AddPath(configJson["OUT_ROOT_DIRECTORY"]["IOS"],tempStr)

#执行加密资源
def RunQuickBat():
	if os.path.isdir(configJson["QUICK_BIN_PATH"]):
		bat=os.path.join(configJson["QUICK_BIN_PATH"],configJson["RESOURCES_BAT"])
		if os.path.isfile(bat):
			if os.path.isdir(configJson["RESOURCES_OUT_PATH"]["ANDROID"]):
				shutil.rmtree(configJson["RESOURCES_OUT_PATH"]["ANDROID"])
			if os.path.isdir(configJson["RESOURCES_OUT_PATH"]["IOS"]):
				shutil.rmtree(configJson["RESOURCES_OUT_PATH"]["IOS"])		
			# str=bat + ' '
			# str=str + '-i ' + configJson["RESOURCES_PATH"] + ' '
			# str=str + '-o ' + configJson["RESOURCES_OUT_PATH"] + ' '
			# str=str + '-ek ' + configJson["SECRET_KEY"] + ' '
			# str=str + '-es ' + configJson["SIGNATURE"]
			# print(str)
			iPath=configJson["RESOURCES_PATH"]
			oPath=configJson["RESOURCES_OUT_PATH"]["ANDROID"]
			ekPath=configJson["SECRET_KEY"]
			esPath=configJson["SIGNATURE"]
			str=configJson["RESOURCES_COMMAND_LINE"] % (bat, iPath, oPath, ekPath, esPath)
			os.system(str) 
		CompressFiles()

def CompressFiles():
	dirs=os.listdir(configJson["RESOURCES_OUT_PATH"]["ANDROID"])
	os.path.join(configJson["RESOURCES_OUT_PATH"]["ANDROID"])
	for dir_ in dirs:
		path=configJson["RESOURCES_OUT_PATH"]["ANDROID"]+'/'+dir_
		newPath=path+'1'
		if os.path.isdir(path):
			os.rename(path,newPath)
			os.makedirs(path)
			shutil.move(newPath,path)
			os.rename(path+'/'+dir_+'1',path+'/'+dir_) 
			shutil.make_archive(path, 'zip', root_dir=path)
			shutil.rmtree(path)
	shutil.copytree(configJson["RESOURCES_OUT_PATH"]["ANDROID"],configJson["RESOURCES_OUT_PATH"]["IOS"])
	print("wancheng!")
InitConfigJosn()
RunQuickBat()
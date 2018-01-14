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
global systemName
if systemType=="Windows":
    systemName="ANDROID"
elif systemType=="Darwin":
    systemName="IOS"

def AddPath(first, second):
    return os.path.join(first,second)

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

    configJson["OUT_ROOT_DIRECTORY"]=configJson["OUT_ROOT_DIRECTORY"][systemName]
    configJson["SECRET_KEY"]=configJson["SECRET_KEY"][systemName]
    configJson["SIGNATURE"]=configJson["SIGNATURE"][systemName]
    configJson["SOURCE_BAT"]=configJson["SOURCE_BAT"][systemName]
    configJson["SOURCE_COMMAND_LINE"]=configJson["SOURCE_COMMAND_LINE"][systemName]
    configJson["OUT_ZIP_SUFFIX"]=configJson["OUT_ZIP_SUFFIX"][systemName]
    configJson["ADD_ORDER"]=configJson["ADD_ORDER"][systemName]

    configJson["SOURCE_PATH"]=AddPath(configJson["IN_ROOT_DIRECTORY"],configJson["SOURCE_PATH"])
    configJson["SOURCE_OUT_PATH"]=AddPath(configJson["OUT_ROOT_DIRECTORY"],configJson["SOURCE_OUT_PATH"])

#执行加密资源
def RunQuickBat():
    if os.path.isdir(configJson["QUICK_BIN_PATH"]):
        bat=os.path.join(configJson["QUICK_BIN_PATH"],configJson["SOURCE_BAT"])
        if os.path.isfile(bat):
            if os.path.isdir(configJson["SOURCE_OUT_PATH"]):
                shutil.rmtree(configJson["SOURCE_OUT_PATH"])
            os.makedirs(configJson["SOURCE_OUT_PATH"])
            dirs=os.listdir(configJson["SOURCE_PATH"])
            for dir_ in dirs:
                path_=os.path.join(configJson["SOURCE_PATH"],dir_)
                if os.path.isdir(path_) and dir_ != ".vscode" and dir_ != "luaIde" and dir_ != "LuaIdeDebug":
                    if (systemType=="Windows" and dir_!="launcher_64") or (systemType=="Darwin" and dir_!="launcher")  :
                        iPath=configJson["SOURCE_PATH"] + '/' + dir_
                        oPath=configJson["SOURCE_OUT_PATH"] + '/' + dir_ + '.zip'
                        if dir_!="launcher_64":
                            oPath=configJson["SOURCE_OUT_PATH"] + '/' + dir_ + configJson["OUT_ZIP_SUFFIX"] + '.zip'
                        ekPath=configJson["SECRET_KEY"]
                        esPath=configJson["SIGNATURE"]
                        pPath=dir_
                        bPath=configJson["ADD_ORDER"]
                        str=configJson["SOURCE_COMMAND_LINE"] % (bat, iPath, oPath, ekPath, esPath, pPath, bPath)
                        os.system(str)   
        print('wancheng!')                    
InitConfigJosn()
RunQuickBat()

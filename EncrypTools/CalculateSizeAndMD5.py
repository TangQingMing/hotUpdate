import os
import platform
import json
import shutil
import hashlib
_FILE_SLIM=100*1024*1024

systemType=platform.system()
global systemName
if systemType=="Windows":
    systemName="ANDROID"
elif systemType=="Darwin":
    systemName="IOS"

def AddPath(first, second):
    return os.path.join(first,second)

def NewPath(key):
    tempStr=configJson[key]
    configJson[key]={}
    configJson[key]["ANDROID"]=AddPath(configJson["OUT_ROOT_DIRECTORY"]["ANDROID"],tempStr)
    configJson[key]["IOS"]=AddPath(configJson["OUT_ROOT_DIRECTORY"]["IOS"],tempStr)

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

    NewPath("RESOURCES_OUT_PATH")
    NewPath("SOURCE_OUT_PATH")
    NewPath("COUNT_SIZE_OUT")

def SetTotalSize(fileName, platformName):
    path_resource=os.path.join(configJson["RESOURCES_OUT_PATH"][platformName], fileName + '.zip')
    path_source=os.path.join(configJson["SOURCE_OUT_PATH"][platformName], fileName + '.zip')
    size=0
    if os.path.isfile(path_resource):
        size+=os.path.getsize(path_resource)
    if os.path.isfile(path_source):
        size+=os.path.getsize(path_source)
    if size==0:
        return
    else:
        path_gamecfg=os.path.join(configJson["COUNT_SIZE_OUT"][platformName],fileName + '.txt')
        f=open(path_gamecfg,'w')
        f.write(str(size))
        f.write('\n')
        f.close()
        return size

def SetCountSizeAndMD5(fileName, platformName):
    path=os.path.join(configJson["OUT_ROOT_DIRECTORY"][platformName], fileName)
    temptr=""
    if os.path.isfile(path):
        size=os.path.getsize(path)
        md5=File_md5(path)
        temptr=configJson["fileInfoListModel"] % (fileName, md5, str(size))
    configJson["fileInfoList"][platformName]+=temptr

def WriteFlistTxt(platformName):
    if configJson["fileInfoList"][platformName]!="":
        fileInfoListStr=configJson["flist"] % configJson["fileInfoList"][platformName]
        fileName='flist.txt'
        if platformName=="IOS":
            fileName='flist_64.txt'
        path_flist=os.path.join(configJson["OUT_ROOT_DIRECTORY"][platformName], fileName)
        f=open(path_flist,'w')
        f.write(fileInfoListStr)
        f.close()

def CountSizeAndMD5():
    for fileName in configJson["COUNT_SIZE_MD5"]:
        SetCountSizeAndMD5(fileName, "ANDROID")
        SetCountSizeAndMD5(fileName, "IOS")
    WriteFlistTxt("ANDROID")
    WriteFlistTxt("IOS")
    

def CountSize():
    for fileName in configJson["COUNT_SIZE"]:
        SetTotalSize(fileName, "ANDROID")
        SetTotalSize(fileName, "IOS")

def File_md5(filename):  
    calltimes = 0     
    hmd5 = hashlib.md5()  
    fp = open(filename, "rb")  
    f_size = os.stat(filename).st_size 
    if f_size > _FILE_SLIM:  
        while (f_size > _FILE_SLIM):  
            hmd5.update(fp.read(_FILE_SLIM))  
            f_size /= _FILE_SLIM  
            calltimes += 1  # delete
        if (f_size > 0) and (f_size <= _FILE_SLIM):  
            hmd5.update(fp.read())  
    else:  
        hmd5.update(fp.read())  
    return hmd5.hexdigest()

InitConfigJosn()
CountSize()
CountSizeAndMD5()
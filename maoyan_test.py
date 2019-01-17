#!/bin/python
#coding=utf-8

import requests  # 需要pip install requests
import sys
import chardet   # 需要pip install chardet
import urllib
import json
import pymysql.cursors # 需要 pip install pymysql

reload(sys)
sys.setdefaultencoding('utf8')  

# 打开数据库连接
conn = pymysql.connect("localhost", "root", "0000", "python", charset='utf8' )
cur = conn.cursor()



# encoding = Windows-1254
url = "http://m.maoyan.com/mmdb/comments/movie/1208282.json?_v_=yes&offset=15"

def getMoveinfo(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)"
    }
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


jsonData = getMoveinfo("http://m.maoyan.com/mmdb/comments/movie/1208282.json?_v_=yes&offset=5")
# jsonData = getMoveinfo("")

# 把string转换成json对象。
jsonObject = json.loads(jsonData)   # 中文乱码

# 把json对象转换成string，编码使用非默认的ascii。
newJson = json.dumps(jsonObject,ensure_ascii=False)  

# 把处理好的json进行处理，为了得到中文。
newJsonObj = json.loads(newJson)  # 中文乱码

cmts = newJsonObj["cmts"]

# print(movieId + "=== " + startTime + "  ===  " + nickName + "  ====  " + score + " ---  " + content)
# 遍历json数组，获取对应的数据信息。
for i in range(0, len(cmts)):
	if str(cmts[i]["movieId"]).strip() != "" : movieId = str(cmts[i]["movieId"])
	if cmts[i]["startTime"].strip() != "" : startTime = cmts[i]["startTime"]
	if cmts[i]["nickName"].strip() != "" : nickName = cmts[i]["nickName"]
	if cmts[i]["cityName"].strip() != "" : cityName = cmts[i]["cityName"]
	if str(cmts[i]["score"]).strip() != "" : score = str(cmts[i]["score"])
	if cmts[i]["content"].strip() != "" : content = cmts[i]["content"]
	sql = " insert into maoyan(movieId, startTime, nickName, cityName, score, content) values('" + movieId + "','" + startTime + "','" + nickName + "','" + cityName + "','" + score + "','" + content + "') "
	cur.execute(sql)
conn.commit()

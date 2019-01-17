#!/bin/python
#coding=utf-8

import pymysql.cursors
import sys
import pyecharts
from pyecharts import Geo
import jieba
from wordcloud import WordCloud

"""
使用pyecharts需要做的准备工作
1、下载pyecharts列库 pip install puecharts
2、如果要使用地图，请下载地图相关的类库 
	pip install echarts-countries-pypkg
	pip install echarts-china-provinces-pypkg
	pip install echarts-china-cities-pypkg
	pip install echarts-china-counties-pypkg
	pip install echarts-china-misc-pypkg
3、分词，使用的是jieba分词
	pip install jieba
4、制作词云，需要下载Wordcloud
	pip install wordcloud
"""
# 

reload(sys)
sys.setdefaultencoding('utf8')  

# 打开数据库连接
conn = pymysql.connect("localhost", "root", "0000", "python", charset='utf8' )

cur = conn.cursor()  

# 生成条形图
queryCitySql = " select cityName, count(cityName) rate_count from maoyan group by cityName order by rate_count desc limit 5; "
cur.execute(queryCitySql)
cityTop5 = cur.fetchall()
listX = []
listY = []
for row in cityTop5:
	cityName = row[0]
	rate_count = row[1]
	listX.append(cityName)
	listY.append(rate_count)
bar = pyecharts.Bar("cityName")
bar.add("count", listX, listY)
bar.render("city_count.html")  # 指定数据图表到那个页面

# 生成条形图
queryScoreSql = " select score, count(score) rate_count from maoyan group by score order by rate_count desc "
cur.execute(queryScoreSql)
scoreTop = cur.fetchall()
scoreX = []
scoreY = []
for row in scoreTop:
	score = row[0]
	rate_count = row[1]
	scoreX.append(score)
	scoreY.append(rate_count)
bar = pyecharts.Bar("ScoreTop")
bar.add("Count", scoreX, scoreY)
bar.render("score_count.html")

# 生成地图分布
queryCitySql = " select cityName, count(cityName) rate_count from maoyan group by cityName; "
# order by rate_count desc limit 4
cur.execute(queryCitySql)
cityTop5 = cur.fetchall()
listData = []
for row in cityTop5:
	cityName = row[0]
	rate_count = row[1]
	if cityName != "藁城":
		listData.append((cityName, rate_count))
geo = Geo("地图分布", width=500, height=500, background_color="#fff")
attr, value = geo.cast(listData)
geo.add("", attr, value, visual_range=[0, 200], maptype='china')
geo.render("China_SKY.html")#生成html文件

# 生成词云图片
queryCitySql = " select content from maoyan; "
cur.execute(queryCitySql)
myContent = cur.fetchall()
content = ""
for row in myContent:
	content = content + " " + row[0]
myContent = " ".join(jieba.cut(content))
wordcloud = WordCloud(font_path="simsun.ttf").generate(myContent)  # 需要使用字体库
import matplotlib.pyplot as plt
plt.imshow(wordcloud)
plt.axis("off")
wordcloud.to_file('unknow_word_cloud.png')


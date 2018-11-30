# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:45:49 2018

@author: Administrator
"""

'''
爬猫眼网站TOP100的电影数据：
    http://maoyan.com/board/4?offset=0
    http://maoyan.com/board/4?offset=10
    http://maoyan.com/board/4?offset=20
    。。。
    http://maoyan.com/board/4?offset=90
'''
import requests
import json
import random
import re
import time
from multiprocessing import Pool
import functools
import myPymysql
import logging
import matplotlib.pyplot as plt

# 獲取logger的實例
logger = logging.getLogger("maoyan")
# 指定logger的輸出格式
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# 文件日志，終端日志
file_handler = logging.FileHandler("maoyan.txt")
file_handler.setFormatter(formatter)

# 設置默認的級別
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

def get_one_page(url):
    """
    發起Http請求，獲取Response的響應結果
    """
    ua_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"}
    reponse = requests.get(url,headers=ua_headers)
    if reponse.status_code == 200: #ok
        return reponse.text
    return None

def write_to_file(item):
    """
    把抓取到的數據寫入本地文件
    """
    with open("猫眼电影4.txt", 'a', encoding='utf-8') as f:
        # json encode -> json str 
        f.write(json.dumps(item,ensure_ascii=False)+'\n')
    #print(1)    

def write_to_sql(item):
    """
    把數據寫入數據庫
    """
    dbhelper = myPymysql.DBHelper()
    title_data = item['title']
    actor_data = item['actor']
    time_data = item['time']
    sql = "INSERT INTO testdb.maoyan(title,actor,time) VALUES (%s,%s,%s);"
    params = (title_data, actor_data, time_data)
    result = dbhelper.execute(sql, params)
    if result == True:
        print("插入成功")
    else:
        logger.error("execute: "+sql)
        logger.error("params: ",params)
        logger.error("插入失败")
        print("插入失败")

def parse_one_page(html):
    """
    從獲取到的html頁面中提取真實想要存儲的數據：
    電影名，主演，上映時間
    """
    pattern = re.compile('<p class="name">.*?title="([\s\S]*?)"[\s\S]*?<p class="star">([\s\S]*?)</p>[\s\S]*?<p class="releasetime">([\s\S]*?)</p>')
    items = re.findall(pattern,html)
    
    # yield在返回的時候會保存當前的函數執行狀態
    for item in items:
        yield {
                'title':item[0].strip(),
                'actor':item[1].strip(),
                'time':item[2].strip()
    }



def analysisCounry():
    # 從數據庫表中查詢出每個國家的電影數量來做分析
    dbhelper = myPymysql.DBHelper()
    # fetchCount
    Total = dbhelper.fetchCount("SELECT count(*) FROM `testdb`.`maoyan`;")
    Am = dbhelper.fetchCount('SELECT count(*) FROM `testdb`.`maoyan` WHERE time like "%美国%";')
    Ch = dbhelper.fetchCount('SELECT count(*) FROM `testdb`.`maoyan` WHERE time like "%中国%";')
    Jp = dbhelper.fetchCount('SELECT count(*) FROM `testdb`.`maoyan` WHERE time like "%日本%";')
    Other = Total[0] - Am[0] - Ch[0] - Jp[0]
    sizes = Am[0], Ch[0], Jp[0], Other
    labels = 'America','China','Japan','Others'
    colors = 'Blue','Red','Yellow','Green'
    explode = 0,0,0,0
    # 畫出統計圖表的餅狀圖
    plt.pie(sizes,explode=explode,labels=labels,
        colors=colors, autopct="%1.1f%%", shadow=True)
    plt.show()


def CrawlMovieInfo(lock, offset):
    """
    抓取電影的電影名，主演，上映時間
    """
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    # 抓取當前的頁面
    html = get_one_page(url)
    #print(html)
    
    # 這裏的for
    for item in parse_one_page(html):
        lock.acquire()
        write_to_file(item)
        write_to_sql(item)
        lock.release()
        
    # 每次下载完一个页面，随机等待1-3秒再次去抓取下一个页面
    #time.sleep(random.randint(1,3))
    

if __name__ == "__main__":
    analysisCounry()
    
    # 把页面做10次的抓取，每一个页面都是一个独立的入口
    from multiprocessing import Manager
    # # #from multiprocessing import Lock 进程池中不能用这个lock
    
    # # # 进程池之间的lock需要用Manager中lock
    manager = Manager()
    lock = manager.Lock()
    
    # # # 使用 functools.partial对函数做一层包装,从而把这把锁传递进进程池
    # # #这样进程池内就有一把锁可以控制执行流程
    partial_CrawlMovieInfo = functools.partial(CrawlMovieInfo, lock)
    pool = Pool()
    pool.map(partial_CrawlMovieInfo, [i*10 for i in range(10)])
    pool.close()
    pool.join()
    
#    for i in range(10):
#        CrawlMovieInfo(i*10) #offset -> 0,10,20,...90

logger.removeHandler(file_handler)
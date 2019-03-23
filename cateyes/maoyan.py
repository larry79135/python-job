# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:45:49 2018

@author: Administrator
"""

'''
爬貓眼網站TOP100的電影數據：
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


logger = logging.getLogger("maoyan")

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

file_handler = logging.FileHandler("maoyan.txt")
file_handler.setFormatter(formatter)


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
    with open("貓眼電影4.txt", 'a', encoding='utf-8') as f:
        # json encode -> json str 
        f.write(json.dumps(item,ensure_ascii=False)+'\n')
       

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
    
   
    for item in items:
        yield {
                'title':item[0].strip(),
                'actor':item[1].strip(),
                'time':item[2].strip()
    }



def analysisCounry():
    
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
   
    plt.pie(sizes,explode=explode,labels=labels,
        colors=colors, autopct="%1.1f%%", shadow=True)
    plt.show()


def CrawlMovieInfo(lock, offset):
    """
    抓取電影的電影名，主演，上映時間
    """
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    
    html = get_one_page(url)
    #print(html)
    
    
    for item in parse_one_page(html):
        lock.acquire()
        write_to_file(item)
        write_to_sql(item)
        lock.release()
        
   
    

if __name__ == "__main__":
    analysisCounry()
    
   
    from multiprocessing import Manager
   
    manager = Manager()
    lock = manager.Lock()
    
    
    partial_CrawlMovieInfo = functools.partial(CrawlMovieInfo, lock)
    pool = Pool()
    pool.map(partial_CrawlMovieInfo, [i*10 for i in range(10)])
    pool.close()
    pool.join()
    


logger.removeHandler(file_handler)

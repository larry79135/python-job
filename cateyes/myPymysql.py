import pymysql
import logging
from collections import deque


logger = logging.getLogger("myPymysql")

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

file_handler = logging.FileHandler("myPymysql.log")
file_handler.setFormatter(formatter)


logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

class DBHelper:
  def __init__(self, host="127.0.0.1", user='root', 
               pwd='a123456',db='testdb',port=3306,
               charset='utf-8'):
    self.host = host
    self.user = user
    self.port = port
    self.passwd = pwd
    self.db = db
    self.charset = charset
    self.conn = None
    self.cur = None

  def connectDataBase(self):
  
    try:

      self.conn =pymysql.connect(host="127.0.0.1",
        user='root',password="a123456",db="testdb",charset="utf8")

    except:
      logger.error("connectDataBase Error")
      return False

    self.cur = self.conn.cursor()
    return True

  def createData(self):
   
    #self.connectDataBase()
    sql = "create database if not exists "+self.db
    try:
      self.cur.execute(sql)
    except:
      logger.error("create database Error")
      return False
    return True

  def execute(self, sql, params=None):
    
    if self.connectDataBase() == False:
      return False

    try:
      if self.conn and self.cur:
        self.cur.execute(sql, params)
        self.conn.commit()
    except:
      logger.error("execute"+sql)
      logger.error("params",params)
      return False
    return True

  def fetchCount(self, sql, params=None):
      if self.connectDataBase() == False:
        return -1
      self.execute(sql, params)
      return self.cur.fetchone() 

  def myClose(self):
      if self.cur:
        self.cur.close()
      if self.conn:
        self.conn.close()
      return True


if __name__ == '__main__':
  dbhelper = DBHelper()
  #print(dbhelper.fetchCount("SELECT count(*) FROM `testdb`.`maoyan`;")[0])
  #print(dbhelper.fetchCount('SELECT count(*) FROM `testdb`.`maoyan` WHERE time like "%中国%";')[0])

  print(dbhelper.connectDataBase())
  # #dbhelper.createData()
  # #dbhelper.myClose()

  sql = "create table maoyan(title varchar(50),\
          actor varchar(200),\
          time  varchar(100));"
  result = dbhelper.execute(sql, None)
  if result == True:
    print("創建表成功")
  else:
    print("創建表失敗")
  dbhelper.myClose()

 


logger.removeHandler(file_handler)


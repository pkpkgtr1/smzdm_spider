import pymysql,configparser,os,datetime
import smtplib,pystache,re,time
from email.mime.text import MIMEText
from send_tg_bot import send_tg_bot


curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "config.ini")  # 读取到本机的配置文件
# 调用读取配置模块中的类
config = configparser.ConfigParser()
config.read(cfgpath, encoding="utf-8-sig")

user = config['Mysql']['user']
pwd = config['Mysql']['passwd']
host = config['Mysql']['host']
port = config['Mysql']['port']
db = config['Mysql']['db']
name_tag = config['email_dm']['tyeakind'].split(",")
#符号
#punctuation = '%_!,;:?"\''


def setmail_pust():
  curpath = os.path.dirname(os.path.realpath(__file__))
  cfgpath = os.path.join(curpath, "config.ini")  # 读取到本机的配置文件
  # 调用读取配置模块中的类
  config = configparser.ConfigParser()
  config.read(cfgpath, encoding="utf-8-sig")
  user = config['Mysql']['user']
  pwd = config['Mysql']['passwd']
  host = config['Mysql']['host']
  port = config['Mysql']['port']
  db = config['Mysql']['db']
  conn = pymysql.connect(host=host,port=int(port),user=user,password=pwd,database=db,charset="utf8")
  cursor = conn.cursor()
  sql = "UPDATE smzdm_sd SET push=1  WHERE time>'"+datetime.datetime.now().strftime('%Y-%m-%d')+"' AND push=0"

  try:
    tiao = cursor.execute(sql)
    conn.commit()
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +'   更新:',tiao,'条数据')
    cursor.close()
    conn.close()
  except Exception:
    print('sql写入push有异常')
    print(sql)

    cursor.close()
    conn.close()


def speed():
  conn = pymysql.connect(host=host,port=int(port),user=user,password=pwd,database=db,charset="utf8",cursorclass=pymysql.cursors.DictCursor)
  cursor = conn.cursor()
  sql = "SELECT title,-(-price) as price1,price,worthy,mall,tag,url,jpg_url,time from smzdm_sd WHERE time > '"+datetime.datetime.now().strftime('%Y-%m-%d')+"' and mall = \'京东\' and push = 0 and price > 0 and price <= 65"
  print(sql)
  try:
    re = cursor.execute(sql)
    ret = cursor.fetchall() 
    #print(ret)
   # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +'   更新:',re,'条数据')
    cursor.close()
    conn.close()
    for i in ret:
      send_tg_bot(i["tag"],i["title"],i["price"],i["mall"],i["url"],i["jpg_url"])
      time.sleep( 2 )
    setmail_pust()
  except Exception:
    print('sql写入push有异常')
    print(sql)

    cursor.close()
    conn.close()

speed()


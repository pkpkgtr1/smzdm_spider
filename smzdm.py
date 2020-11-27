#encoding :utf-8
import urllib.request,time,datetime,json,os,configparser
import re,pymysql

#昨天
def getYesterday():
  today = datetime.date.today()
  oneday = datetime.timedelta(days=1)
  yesterday = today - oneday
  return yesterday

# 转为时间数组
def time_Unix():
    '''
    获取当前时时间戳
    '''
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timeArray = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(timeArray))

#什么值得买get请求
def getHtml(timeout):
   weburl='http://www.smzdm.com/jingxuan/json_more?timesort='+timeout+"&filter=s0f0t0b0d0r0p0"
   webheader={'Connection': 'Keep-Alive','Accept': 'text/html, application/xhtml+xml, */*','Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0','Host': 'www.smzdm.com'}
   req=urllib.request.Request(url=weburl,headers=webheader)
   webpage=urllib.request.urlopen(req)
   contentBytes=webpage.read()
   str_=str(contentBytes.decode("unicode_escape"))#可直接获取相应的中文
   return str_


def get_tile():
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
  sql = "SELECT title FROM smzdm_massage WHERE time > '"+str(getYesterday())+"' GROUP BY title"
  #ret = cursor.fetchall()#
  #print(ret[0][11])#

  try:
    cursor.execute(sql)
    ret = cursor.fetchall()#
    cursor.close()
    conn.close()
    return ret
  except Exception:
    print('sql查询有异常')
    print(sql)
    cursor.close()
    conn.close()
    return ''
'''
#什么值得买数据整理写入数据库
'''
def getValue(data_time,writtime):

   str_=getHtml(data_time)#初始页面值
   str_unworthy=re.findall(r'(?<="article_unworthy":).+?(?=,)',str_,re.M)#不值得推荐数值
   str_title=re.findall(r'(?<="article_title":").+?(?=",)',str_,re.M)#商品名称
   str_worthy=re.findall(r'(?<="article_worthy":).+?(?=,)',str_,re.M)#值得推荐数值
   str_comment=re.findall(r'(?<="article_comment":).+?(?=,)',str_,re.M)#收藏数量
   str_collect=re.findall(r'(?<="article_collection":).+?(?=,)',str_,re.M)#评论数量
   str_price = re.findall(r'(?<="article_price":").+?(?=",)',str_,re.M)#价格
   str_mall = re.findall(r'(?<="article_mall":").+?(?=",)', str_, re.M)  # 活动商家
   str_article_jpg_url = re.findall(r'(?<="article_pic_url":").+?(?=",)', str_, re.M)#商品图片
   str_article_url = re.findall(r'(?<="article_url":").+?(?=",)', str_, re.M)#什么值得买链接
   str_tag = re.findall(r'(?<="article_tags2":).+?(?=,"p)', str_, re.M)  # 标签
   #根据timesort来不断循环所要的结果
   str_timesort = re.findall(r'(?<="article_timesort":)\d+',str_,re.M)

   curpath = os.path.dirname(os.path.realpath(__file__))
   cfgpath = os.path.join(curpath, "config.ini")  # 读取到本机的配置文件
   # 调用读取配置模块中的类
   config = configparser.ConfigParser()
   config.read(cfgpath, encoding="utf-8-sig")
   smzdm_timeStamp = config['smzdm']['smzdm_timeStamp']

   get_title = get_tile()
   title_list = []
   for x in range(len(get_title)):
       title_list.append(get_title[x][0])


   for x in range(0,len(str_title)):

       if (int(smzdm_timeStamp) >= int(str_timesort[x])):
           break
       else:
           str_ti = str(str_title[x])
           str_ti = str_ti.replace('\\/', '/')
           str_ti = str_ti.replace("'", '’')
           if str_ti in title_list:
               index = len(str_timesort) - 1

               print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"   "+str_ti+"      已存在")
           else:
               if (len(str_ti) > 200): str_ti = str_ti[0:150]
               index = len(str_timesort) - 1
               tag = json.loads(str_tag[x])
               if len(tag):
                   tag = tag[0]["name"]
               else:
                   tag = ""
               timeStamp = int(str_timesort[x])
               timeArray = time.localtime(timeStamp)
               totimeStamp = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
               print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"   "+str_ti)
               getDB(str_ti,str(str_worthy[x]),str(str_unworthy[x]),str(str_comment[x]),str(str_collect[x]),str(str_price[x]).replace('\\/', '/'),str(str_mall[x]),str(str_article_url[x]).replace('\\/', '/'),str(str_article_jpg_url[x]).replace('\\/', '/'),tag,totimeStamp)
   if (int(smzdm_timeStamp) >= int(str_timesort[19])):
       config.set('smzdm', 'smzdm_timeStamp', writtime)
       config.write(open("config.ini", "w"))
       print('--------end----------')
   else:
       print(smzdm_timeStamp,str_timesort[19])
       return getValue(str_timesort[index],writtime)


#数据库连接写入模块

def getDB(title,worthy,unworthy,comment,collect,price,mall,url,jpg_url,tag,timesort):
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
  sql = "INSERT INTO smzdm_massage ( title, worthy, unworthy, comment, collect, price, mall, url, jpg_url, tag,push, time) VALUES ('"+ title +"', " + worthy + ", "+unworthy+", "+comment+", "+collect+", '"+price+"', '"+mall+"', '"+url+"', '"+jpg_url+"', '"+tag+"',0,'"+timesort+"')"
  #ret = cursor.fetchall()#
  #print(ret[0][11])#

  try:
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
  except Exception:
    print('sql写入有异常')
    print(sql)
    cursor.close()
    conn.close()








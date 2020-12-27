import pymysql,configparser,os,datetime

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

setmail_pust()

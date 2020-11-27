import pymysql,configparser,os,datetime
import smtplib,pystache,re
from email.mime.text import MIMEText

curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "config.ini")  # 读取到本机的配置文件
# 调用读取配置模块中的类
config = configparser.ConfigParser()
config.read(cfgpath, encoding="utf-8-sig")
mail_user  = config['email_163']['sender']
mail_pass  = config['email_163']['psw']
port = config['email_163']['port']
mail_host  = config['email_163']['smtp_server']
receivers  = config['email_163']['receiver'].split(",")

user = config['Mysql']['user']
pwd = config['Mysql']['passwd']
host = config['Mysql']['host']
port = config['Mysql']['port']
db = config['Mysql']['db']
name_tag = config['email_dm']['tyeakind'].split(",")
#符号
punctuation = '%_!,;:?"\''

#去符号
def removePunctuation(text):
  text = re.sub(r'[{}]+'.format(punctuation), '', text)
  return text.strip().lower()
#设置推送 pust=1推送 0默认 2已推送
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
  sql = "UPDATE smzdm_9_9 SET push=2  WHERE time>'"+datetime.datetime.now().strftime('%Y-%m-%d')+"' AND push=0"

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

#edm生成模板并推送
def edm():
  conn = pymysql.connect(host=host,port=int(port),user=user,password=pwd,database=db,charset="utf8",cursorclass=pymysql.cursors.DictCursor)
  cursor = conn.cursor()
  sql = "SELECT title,-(-price) as price1,price,worthy,mall,tag,url,jpg_url,time from smzdm_massage WHERE time > '"+datetime.datetime.now().strftime('%Y-%m-%d')+"' and worthy > 5 and push = 0 and price > 0 and price <= 9.9"



  print(sql)
  re = cursor.execute(sql)

  ret = cursor.fetchall()  #
  data = {
      'header': '什么值得买9.9元精选',
      'items': ret
  }
  if re == 0:
      return ""
  else:
      try:
          t = open("edm.html", "r", encoding='UTF-8')  # 用文件作为模板
          filecontent = pystache.render(t.read(), data)
          #sql = "UPDATE smzdm_sd set push = 2 WHERE tag LIKE'" + name_tag + "' AND push = 1"
          cursor.execute(sql)
          conn.commit()
          cursor.close()
          conn.close()
          return filecontent
      except Exception:
          print('sql写入push有异常')
          print(sql)

          cursor.close()
          conn.close()
          return ""

html_data = edm()
print(receivers)


def sendEmail():
  title = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '  什么值得买优惠推送'
  message = MIMEText(html_data, 'html', 'utf-8')  # 内容, 格式, 编码
  message['From'] = "{}".format(mail_user)

  message['To'] = ",".join(receivers)
  message['Subject'] = title

  try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)  # 登录验证
    smtpObj.sendmail(mail_user, receivers, message.as_string())  # 发送
    print("mail has been send successfully.")
  except smtplib.SMTPException as e:
    print(e)


if len(html_data) == 0:
  pass
else:
  sendEmail()
  setmail_pust()

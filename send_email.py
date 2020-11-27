# coding:utf-8
import os,configparser,datetime
import smtplib,pystache,pymysql,re
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
#去符号
punctuation = '%_!,;:?"\''
def removePunctuation(text):
    text = re.sub(r'[{}]+'.format(punctuation),'',text)
    return text.strip().lower()
#email发送
def edm(name_tag):
  conn = pymysql.connect(host=host,port=int(port),user=user,password=pwd,database=db,charset="utf8",cursorclass=pymysql.cursors.DictCursor)
  cursor = conn.cursor()
  sql = "SELECT title,price,tag,mall,jpg_url,url FROM smzdm_sd WHERE tag LIKE'%" + name_tag + "%' AND push = 1 GROUP BY title order by price+0 ASC"
  re = cursor.execute(sql)

  ret = cursor.fetchall()  #
  data = {
      'header': removePunctuation(name_tag),
      'items': ret
  }
  if re == 0:
      return ""
  else:
      try:
          t = open("edm.html", "r", encoding='UTF-8')  # 用文件作为模板
          filecontent = pystache.render(t.read(), data)
          sql = "UPDATE smzdm_sd set push = 2 WHERE tag LIKE'%" + name_tag + "%' AND push = 1"
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

#html模板代码拼接
html_data = ""
for x in range(len(name_tag)):
    if '比上次发布低' in name_tag[x]:
        html_data = html_data + edm('%比上次发布低___%')
    else:
        html_data= html_data + edm(name_tag[x])

#print(edm("手慢无"))
#neirong= edm("手慢无")

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

if len(html_data)==0 :
    pass
else:
    sendEmail()

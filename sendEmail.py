import smtplib
import time
from email.mime.text import MIMEText

mail_server = "smtp.163.com"
# mail_port = 25
mail_port = 465
sender = "rzx991105@163.com"
sender_password = "URULCELYDGXSTQPK"  # 授权码
receivers = "1025744898@qq.com"

send_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
message = MIMEText("testing" + send_time, 'plain', 'utf-8')
message['From'] = sender
message['To'] = receivers

subject = '测试'
message['Subject'] = subject

try:
    smtp_obj = smtplib.SMTP_SSL(mail_server, mail_port)
    # smtp_obj.connect(mail_server, mail_port)
    smtp_obj.login(sender, sender_password)
    smtp_obj.sendmail(sender, [receivers], message.as_string())
    print('邮件发送成功!')
except smtplib.SMTPException as e:
    print('邮件发送失败!')
    print(e)
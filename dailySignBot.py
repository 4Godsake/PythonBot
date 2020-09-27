import base64

import requests
from selenium import webdriver
from PIL import Image
from pathlib import Path
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options


class User:
    def __init__(self, usn, psw, email):
        self.username = usn
        self.password = psw
        self.email = email

def sendEmail(receiver,content):
    mail_server = "smtp.163.com"
    mail_port = 25
    sender = "rzx991105@163.com"
    sender_password = "URULCELYDGXSTQPK"  # 授权码
    receivers = receiver

    send_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    message = MIMEText(content + send_time, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = receivers

    subject = '山财大疫情填报结果 noreply'
    message['Subject'] = subject

    try:
        smtp_obj = smtplib.SMTP()
        smtp_obj.connect(mail_server, mail_port)
        smtp_obj.login(sender, sender_password)
        smtp_obj.sendmail(sender, [receivers], message.as_string())
        print('邮件发送成功!')
    except smtplib.SMTPException as e:
        print('邮件发送失败!')
        print(e)
    return

def convert_img(img_url):
    with open(img_url, "rb") as f:  # 转为二进制格式
        base64_data = base64.b64encode(f.read())  # 使用base64进行加密
        # print(base64_data)
    return base64_data


def imgVerify(image):
    username = "1025744898@qq.com"
    password = "6627221lt"
    url_login = "http://www.damagou.top/apiv1/login.html"
    params_login = {"username": username, "password": password}
    res_get = requests.get(url=url_login, params=params_login)
    userKey = res_get.text
    url_post = "http://www.damagou.top/apiv1/recognize.html"
    params_post = {"image": image, "userkey": userKey}
    res_post = requests.post(url_post, params=params_post)
    answer = res_post.text
    print(answer)
    if answer == "识别失败，请重试":
        print("验证码截图出错，联系管理员")
    return answer


class VerificationCode():
    def __init__(self):

        chrome_options = Options()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.find_element = self.driver.find_element_by_css_selector
        self.driver.get('http://bcfl.sdufe.edu.cn/index/login')  # 打开登陆页面

        # Get the actual page dimensions using javascript
        width = self.driver.execute_script("return Math.max(document.body.scrollWidth,"
                                           "document.documentElement.clientWidth,"
                                           "document.documentElement.scrollWidth,"
                                           "document.documentElement.offsetWidth);")
        # height = self.driver.execute_script("return Math.max(document.body.scrollHeight,"
        #                                     "document.body.offsetHe,"
        #                                     "document.documentElement.clientHeight,"
        #                                     "document.documentElement.scrollHeight,"
        #                                     "document.documentElement.offsetHeight)")
        height=2500
        print(width)
        print(height)
        # resize
        self.driver.set_window_size(width, height)

    def get_pictures(self):
        i = 1
        scrpath = ".\\autoSign"  # 指定的保存目录
        capturename = '\\' + str(i) + '.png'  # 自定义命名截图
        wholepath = scrpath + capturename
        if Path(scrpath).is_dir():  # 判断文件夹路径是否已经存在
            pass
        else:
            Path(scrpath).mkdir()  # 如果不存在，创建文件夹
        while Path(wholepath).exists():  # 判断文件是否已经存在，也可使用is_file()判断
            i += 1
            capturename = '\\' + str(i) + '.png'
            wholepath = scrpath + capturename
        time.sleep(1)

        self.driver.save_screenshot(wholepath)  # 全屏截图
        page_snap_obj = Image.open(wholepath)
        img = self.driver.find_element_by_class_name('auth_code_img')  # 验证码元素位置
        time.sleep(1)
        location = img.location
        size = img.size  # 获取验证码的大小参数
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        page_snap_obj = page_snap_obj.crop((left, top, right, bottom))  # 按照验证码的长宽，切割验证码
        page_snap_obj.save(wholepath)
        # page_snap_obj.show()  # 打开切割后的完整验证码
        # self.driver.close()  # 处理完验证码后关闭浏览器
        print(wholepath)
        return wholepath


    # 登录验证码识别网站并传入数据

    def autoSign(self,User):
        image_url = self.get_pictures()
        img64 = convert_img(image_url)
        verifyCode = imgVerify(img64)
        self.driver.find_element_by_id("number").send_keys(User.username)
        self.driver.find_element_by_id("card").send_keys(User.password)
        self.driver.find_element_by_id("verify").send_keys(verifyCode)
        time.sleep(0.5)
        self.driver.find_element_by_id("sub_btn").click()
        time.sleep(1)
        try:
            alert = self.driver.switch_to.alert.text
            self.driver.switch_to.alert.accept()
            print(alert)
            self.driver.find_element_by_id("number").clear()
            self.driver.find_element_by_id("card").clear()
            self.driver.find_element_by_id("verify").clear()

        except NoAlertPresentException:
            self.driver.find_element_by_class_name("daka").click()
            time.sleep(1)
            print("验证通过")
            return True

        return False

    def fillForm(self):
        province = self.driver.find_element_by_id("province_id")
        Select(province).select_by_value("16")
        time.sleep(0.5)
        city = self.driver.find_element_by_id("city_id")
        Select(city).select_by_value("170")
        self.driver.find_element_by_class_name("auth_code_img").click()
        time.sleep(1)
        img_url = self.get_pictures()
        img_base64 = convert_img(img_url)
        verifyCode = imgVerify(img_base64)
        self.driver.find_element_by_id("verify").send_keys(verifyCode)
        self.driver.find_element_by_id("student_btn").click()
        time.sleep(1)
        try:
            alert = self.driver.switch_to.alert.text
            self.driver.switch_to.alert.accept()
            print(alert)
            self.driver.find_element_by_id("verify").clear()

        except NoAlertPresentException:
            self.driver.quit()
            print("验证通过")
            return True
        return False


def mainFunction(User):
    a = VerificationCode()
    loginStat = a.autoSign(User)
    i = 0
    while loginStat != True:
        loginStat = a.autoSign(User)
        i += 1
        if i > 20:
            print("连续登陆失败，有空加上发邮件提醒")
            sendEmail(User.email, "填报失败！请手动填报并联系管理员")
    print("登陆成功")

    submitStat = a.fillForm()
    j = 0
    while submitStat != True:
        submitStat = a.fillForm()
        j += 1
        if j > 20:
            print("连续提交失败，有空加上发邮件联系管理员")
            sendEmail(User.email, "填报失败！请手动填报并联系管理员")
    sendEmail(User.email, "今日疫情填报完成！")
    print("疫情填报成功")
    return

#               学号，     密码，      邮箱（用于接收结果）
rzx = User("20170667227", "051037", "1025744898@qq.com")

if __name__ == '__main__':
    mainFunction(rzx)

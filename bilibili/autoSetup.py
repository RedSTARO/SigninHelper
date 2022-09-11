# -*- coding: utf-8 -*-
import qrcode
import hashlib
from threading import Thread
import time
import requests
from io import BytesIO
import http.cookiejar as cookielib
from PIL import Image
import os
import json

configVersion = "2"

requests.packages.urllib3.disable_warnings()

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
           " AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/74.0.3729.169 Safari/537.36", 'Referer': "https://www.bilibili.com/"}
headerss = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/74.0.3729.169 Safari/537.36",  'Host': 'passport.bilibili.com', 'Referer': "https://passport.bilibili.com/login"}


class showpng(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        img = Image.open(BytesIO(self.data))
        img.show()


def islogin(session):
    try:
        session.cookies.load(ignore_discard=True)
    except Exception:
        pass
    loginurl = session.get(
        "https://api.bilibili.com/x/web-interface/nav", verify=False, headers=headers).json()
    if loginurl['code'] == 0:
        print('Cookies值有效，', loginurl['data']['uname'], '，已登录！')
        return session, True
    else:
        print('请使用手机bilibili扫描即将弹出的二维码登录')
        time.sleep(3)
        return session, False


def bzlogin():
    if not os.path.exists('bzcookies.txt'):
        with open("bzcookies.txt", 'w') as f:
            f.write("")
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='bzcookies.txt')
    session, status = islogin(session)
    if not status:
        getlogin = session.get(
            'https://passport.bilibili.com/qrcode/getLoginUrl', headers=headers).json()
        loginurl = requests.get(getlogin['data']['url'], headers=headers).url
        oauthKey = getlogin['data']['oauthKey']
        qr = qrcode.QRCode()
        qr.add_data(loginurl)
        img = qr.make_image()
        a = BytesIO()
        img.save(a, 'png')
        png = a.getvalue()
        a.close()
        t = showpng(png)
        t.start()
        tokenurl = 'https://passport.bilibili.com/qrcode/getLoginInfo'
        while 1:
            qrcodedata = session.post(tokenurl, data={
                                      'oauthKey': oauthKey, 'gourl': 'https://www.bilibili.com/'}, headers=headerss).json()
            if '-4' in str(qrcodedata['data']):
                print('二维码未失效，请扫码！')
            elif '-5' in str(qrcodedata['data']):
                print('已扫码，请确认！')
            elif '-2' in str(qrcodedata['data']):
                print('二维码已失效，请重新运行！')
            elif 'True' in str(qrcodedata['status']):
                print('已确认，登入成功！')
                session.get(qrcodedata['data']['url'], headers=headers)
                break
            else:
                print('其他：', qrcodedata)
            time.sleep(2)
        session.cookies.save()
    return session


def configSetup():
    if input("您是否需要配置微信推送通知?(y/n)") == "y":
        import webbrowser
        print("请使用微信在即将打开的网站中扫码登录并复制Sendkey，复制完成后即可关闭网站")
        time.sleep(2)
        webbrowser.open_new_tab('https://sct.ftqq.com/login')
        sever = input("请输入您刚刚复制的Sendkey并在此输入(输入n退出配置微信推送)：")
        if sever == "n":
            sever = None
        else:
            print("微信推送配置成功")
    else:
        print("您已选择不配置微信推送")
        sever = False
    coinnum = int(input("每次投入硬币数量0 或 1 或 2?(请直接输入阿拉伯数字):"))
    if input("投币时是否点赞?(y/n)") == "y":
        select_like = True
    else:
        select_like = False
    with open('bzcookies.txt', encoding='utf-8') as file_obj:
        contents = file_obj.read()
        contents = contents.rstrip().replace("#LWP-Cookies-2.0",
                                             "").replace("Set-Cookie3: ", "").replace(" ", "").replace("\n", ";")
        list = contents.split(";")
        file_obj.close()
    for i in list:
        if i != ['']:
            key = i.split("=")[0]
            value = i.split("=")
            if key == "bili_jct":
                bili_jct = value[1]
            if key == "SESSDATA":
                SESSDATA = value[1].replace('"', "")
            if key == "DedeUserID":
                DedeUserID = value[1]

    md5 = hashlib.md5()
    md5.update(str(31 * 188043 * 41227).encode(encoding='utf-8'))

    dict = {"sever": sever, "coinnum": coinnum, "select_like": select_like,
            "bili_jct": bili_jct, "SESSDATA": SESSDATA, "DedeUserID": DedeUserID, "timeLimit": md5.hexdigest(), " configVersion": configVersion}
    with open("将我发送到邮箱.json", "w") as f:
        json.dump(dict, f)
    print("加载文件完成..., 请查看软件目录下的“将我发送到邮箱.json”文件，将其作为附件通过邮箱发送到 bilibilicheckin@163.com")

if __name__ == '__main__':
    bzlogin()
    configSetup()

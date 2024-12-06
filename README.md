## 企业微信API Python封装

为方便将企业微信对接企业内部系统，所以对接口进行简单的封装

有四个文件

info文件

Company_ID为公司ID

Appsecret为应用的secret

如何查看，请看官方文档，这里不做赘述

```Txt
Company_ID=2345621
Appsecret=qwertyuisdfghscvwertyM
```

tokenfile文件

请按照如下填写到tokenfile文件，将时间改到当前时间之前2小时之前的时间即可，

```
tokenvalue=2024-12-06 17:07:03
```

WXWork.py

主要功能对Company_ID和secret以及获取token的值，比较简单

```python
from datetime import datetime, timedelta
import requests
class WXWork(object):
    def __init__(self):
        # 企业ＩＤ
        self.Company_ID = self.getCompany_ID()
        # 应用secret
        self.Appsecret = self.getAppsecret()
        self.token = self.wirtetoken()

    def getCompany_ID(self):
        with open("info","r") as f:
            flist = f.readlines()
            Company_ID = flist[0]
            Company_IDStr = Company_ID.split("=")[1].replace("\n","")
            f.close()
            return Company_IDStr

    def getAppsecret(self):
        with open("info","r") as f:
            flist = f.readlines()
            Appsecret = flist[1]
            AppsecretStr = Appsecret.split("=")[1].replace("\n","")
            f.close()
            return AppsecretStr
    def gettoken(self):
        res = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.Company_ID}&corpsecret={self.Appsecret}")
        if res.status_code == 200:
            try:
                resjson = res.json()
                print(resjson)
                return resjson.get("access_token")
            except:
                raise ValueError("获取token失败,请检查公司id和应用secret")
        else:
            raise ValueError("响应状态码不是200")
    def wirtetoken(self):
        with open("tokenfile","r+") as f:
            readlist = f.readlines()
            readtoken = readlist[0]
            tokentime = readtoken.split("=")[1]
            tokenstr = readtoken.split("=")[0]
            # 当前时间
            nowtime = datetime.now()
            # 转换后的时间
            tokentime_object = datetime.strptime(tokentime, '%Y-%m-%d %H:%M:%S')
            time_increase = timedelta(seconds=7200)
            increase_token = nowtime + time_increase
            increase_token = increase_token.strftime("%Y-%m-%d %H:%M:%S")
            if nowtime < tokentime_object:
                f.close()
                return tokenstr
            else:
                with open("tokenfile","w+") as fw:
                    newtoken = self.gettoken()
                    fw.write(f"{newtoken}={increase_token}")
                    fw.close()
                    return newtoken

if __name__ == '__main__':
    # print(1)
    wx= WXWork()
    print(wx.token)
```

wxworkapi.py

目前写了两个示例的代码，第一个为发送消息，第二个是使用邮箱获取用户id

```python

from WXWork import WXWork
import requests
class WeChatAPI(WXWork):
    def __init__(self):
        super().__init__()
    def send_message(self,touser:str,agentid:str,content:str):
        infojson = dict()
        # 用户的ID
        infojson['touser'] = touser
        # 消息类型
        infojson['msgtype'] = 'text'
        # 需要发送的应用ＩＤ
        infojson['agentid'] = agentid
        textdict = dict()
        # 消息内容
        textdict['content'] = content
        infojson["text"] = textdict
        infojson["safe"] = 0
        sendresquest = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.token}',json=infojson)
    # 使用邮件获取用户ID
    def getuserid(self,email:str):
        getuseridjson = dict()
        getuseridjson['email'] = email
        getuseridjson['email_type'] = 1
        sendresquest = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/user/get_userid_by_email?access_token={self.token}',json=getuseridjson)
        print(sendresquest.json())

if __name__ == '__main__':
    api = WeChatAPI()
    api.send_message("1234","45678","我就试一下")
    api.getuserid("34567@qq.com")

```

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



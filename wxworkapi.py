
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
    api.send_message("0000","000671","我就试一下")
    api.getuserid("123456543@qq.com")

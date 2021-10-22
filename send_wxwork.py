#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests, sys, json
import urllib3
urllib3.disable_warnings()

# Corpid企业号ID
Corpid = "ww956fb91b8644e9acd"

# Secret应用凭证密钥
Secret = "0B55fRp86ZkJt_2E47uw3yPRuY7C700KGcw94Vr8cO01"

# 自建应用ID
Agentid = "1000004"

# token_config文件放置路径
Token_config = r'/tmp/wechat_config.json'

def GetTokenFromServer(Corpid, Secret):
    """获取access_token"""
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid": Corpid,
        "corpsecret": Secret
    }
    r = requests.get(url=Url, params=Data, verify=False)
    print(r.json())
    if r.json()['errcode'] != 0:
        return False
    else:
        Token = r.json()['access_token']
        file = open(Token_config, 'w')
        file.write(r.text)
        file.close()
        return Token
		
def SendMessage(Partyid, Subject, Content):
    """发送消息"""
    # 获取token信息
    try:
        file = open(Token_config, 'r')
        Token = json.load(file)['access_token']
        file.close()
    except:
        Token = GetTokenFromServer(Corpid, Secret)

    # 发送消息
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": Userid,
        "msgtype": "text",
        "agentid": Agentid,
        "text": {"content": Subject + '\n' + Content},
        "safe": "0"
    }
    r = requests.post(url=Url, data=json.dumps(Data), verify=False)

    # 如果发送失败，将重试三次
    n = 1
    while r.json()['errcode'] != 0 and n < 4:
        n = n + 1
        Token = GetTokenFromServer(Corpid, Secret)
        if Token:
            Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
            r = requests.post(url=Url, data=json.dumps(Data), verify=False)
            print(r.json())

    return r.json()


if __name__ == '__main__':
    Userid = str(sys.argv[1])
    Subject = str(sys.argv[2])
    Content = str(sys.argv[3])
    Status = SendMessage(Userid, Subject, Content)
    print(Status)

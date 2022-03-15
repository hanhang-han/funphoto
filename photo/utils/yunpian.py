

import requests


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【李甲楠】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }
        # text必须要跟云片后台的模板内容 保持一致，不然发送不出去！
        r = requests.post(self.single_send_url, data=params)
        print(r)


if __name__ == '__main__':
    yun_pian = YunPian('APP_KEY')
    yun_pian.send_sms('1862', '17613701708')

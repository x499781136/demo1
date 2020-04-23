import time
from hashlib import md5
from json import dumps

import requests


API = 'https://api.mysubmail.com/message/xsend.json'
APPID = '48182'
APPKEY = '247e2bc349994db65be8e29d37e195b9'
PROJECT = '2OuxR3'


def make_signature(args):
    '''创建签名'''
    # 将所有参数拼接成字符串
    arg_lst = []
    for key in sorted(args.keys()):
        value = args[key]
        arg_lst.append(f'{key}={value}')
    args_str = '&'.join(arg_lst)

    # 创建待签名字符串
    app_str = f'{APPID}{APPKEY}'
    sign_str = f'{app_str}{args_str}{app_str}'.encode('utf8')

    # 签名
    signature = md5(sign_str).hexdigest()

    return signature


def send_sms(phone, vcode):
    '''发送短信'''
    args = {
        'appid': APPID,
        'project': PROJECT,
        'sign_type': 'md5',
        'timestamp': int(time.time()),
        'to': phone,
        'vars': dumps({'vcode': vcode}),
    }
    args['signature'] = make_signature(args)
    response = requests.post(API, data=args)

    if response.status_code:
        result = response.json()
        if result['status'] == 'success':
            return True
        else:
            print(result['msg'])

    return False

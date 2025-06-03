# -*- coding: utf-8 -*-
"""
@Author  : 江洁
@time: 2023/7/27 17:31
"""

import time
import requests
import yaml
from utils import *

# 假设config_data是从安全的配置管理系统获取
# 这里为了示例，我们使用一个模拟的配置加载函数
def load_config():
    return {
        "admin_name": config_data.get("account"),
        "password": config_data.get("password")
    }

def get_timestamp():
    return str(int(time.time() * 1000))


class BaseLogin:
    def __init__(self, url, method='PUT', headers=None, data=None):
        self.url = url
        self.method = method.upper()
        self.headers = headers if headers else {"Content-Type": "application/json;charset=UTF-8"}
        self.data = data if data else {}

    def get_token(self):
        try:
            if self.method == 'GET':
                res = requests.get(self.url, params=self.data, headers=self.headers)
            elif self.method == 'PUT':
                res = requests.put(self.url, json=self.data, headers=self.headers)
            else:
                print("请求方式错误")
                return None
            res.raise_for_status()  # 检查响应状态码
            return res.json()
        except requests.exceptions.RequestException as e:
            print(f"请求异常：{e}")
            return None


def update_token(token_file="token.yaml"):
    config = load_config()
    headers = {
        "x-k7-timestamp": get_timestamp()
    }
    method = 'PUT'
    url = "http://dev-dms.k7.cn/dms/login"
    data = {
        "admin_name": config_data.get("account"),
        "password": config_data.get("password")
    }
    login = BaseLogin(url, method, headers, data)
    res_json = login.get_token()
    if res_json and 'data' in res_json and 'token' in res_json['data']:
        token = res_json['data']['token']
        data = {"x-k7-token": token}
        with open(token_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False)
        print("Token已更新:", token)
    else:
        print("token更新失败或找不到'data'键")


if __name__ == '__main__':
    update_token()


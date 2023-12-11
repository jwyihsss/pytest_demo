# -*- coding: utf-8 -*-
"""
@Author  : 江洁
@time   : 2023/7/28 14:40
"""
import allure
import pytest
import time

import requests
import yaml


@allure.feature('任务配置模块')
@allure.title('任务关联查询接口')
@pytest.mark.datafile('test_data/quest_app/test_quest_app.yml')
def test_quest_app(core, env, case, inputs, expectation):
    filepath=r'C:\Users\Administrator\PycharmProjects\t2-api-autotest\test_cases\login\token.yaml'
    with open(filepath,'r',encoding='utf-8') as f:
        token=yaml.safe_load(f)["x-k7-token"]
    timestamp = int(time.time() * 1000)
    core.headers['x-k7-timestamp'] = str(timestamp)
    core.headers['Content-Type'] = 'application/json;charset=UTF-8'
    core.headers['x-k7-token']=token
    core.headers['action'] = 'relation'
    # core.requests: 返回请求方法对象
    # core.headers: 返回全局请求头
    # core.sql: 返回查询方法
    # core.cache: 返回缓存处理方法对象
    res = core.requests.request(env, params=inputs['params'], headers=core.headers).json()
    print(res)
    assert res == expectation

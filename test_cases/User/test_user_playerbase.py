#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025-05-28 10:01:39
import allure
import pytest
import yaml
import time


@allure.feature('User')
@pytest.mark.datafile('test_data/User/test_user_playerbase.yml')
def test_user_playerbase(core, env, case, inputs, expectation):
    filepath = r'C:\Users\Administrator\PycharmProjects\t2-api-autotest\token.yaml'
    with open(filepath, 'r', encoding='utf-8') as f:
        token = yaml.safe_load(f)["x-k7-token"]
    timestamp = int(time.time() * 1000)
    core.headers['x-k7-timestamp'] = str(timestamp)
    core.headers['Content-Type'] = 'application/json;charset=UTF-8'
    core.headers['x-k7-token'] = token
    res = core.requests.request(env, data=inputs['params'], headers=core.headers).json()
    with allure.step('接口响应断言'):
        assert res.get(inputs['assert_key']) in expectation['data']
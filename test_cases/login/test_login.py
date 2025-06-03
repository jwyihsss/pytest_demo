#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025-05-27 16:12:51
import allure
import pytest
import yaml
import time


@allure.feature('login')
@pytest.mark.datafile('test_data/login/test_login.yml')
def test_login(core, env, case, inputs, expectation):
    filepath = r'C:\Users\Administrator\PycharmProjects\t2-api-autotest\token.yaml'
    with open(filepath, 'r', encoding='utf-8') as f:
        token = yaml.safe_load(f)["x-k7-token"]
    timestamp = int(time.time() * 1000)
    core.headers['x-k7-timestamp'] = str(timestamp)
    core.headers['Content-Type'] = 'application/json;charset=UTF-8'
    core.headers['x-k7-token'] = token
    res = core.requests.request(env, json=inputs['data'], headers=core.headers).json()
    with allure.step('接口响应断言'):
        assert res.get(inputs['assert_key']) != expectation['data']
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025-03-28 16:49:20
import allure
import pytest
import yaml
import time


@allure.feature('recharge')
@pytest.mark.datafile('test_data/recharge/test_recharge_order.yml')
def test_recharge_order(core, env, case, inputs, expectation):
    filepath = r'C:\Users\Administrator\PycharmProjects\t2-api-autotest\token.yaml'
    with open(filepath, 'r', encoding='utf-8') as f:
        token = yaml.safe_load(f)["x-k7-token"]
    timestamp = int(time.time() * 1000)
    core.headers['x-k7-timestamp'] = str(timestamp)
    core.headers['Content-Type'] = 'application/json;charset=UTF-8'
    core.headers['x-k7-token'] = token
    res = core.requests.request(env, data=inputs['params'], headers=core.headers).json()
    with allure.step('接口响应断言'):
        assert res.get(inputs['assert_key']) in expectation['response']
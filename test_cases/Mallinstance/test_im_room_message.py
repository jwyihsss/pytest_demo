
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2023-04-24 17:07:07
import os
import json
import time
import logging
import yaml
from functools import lru_cache

import pytest
import allure

# 初始化日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 从环境变量读取配置信息，以提高灵活性和安全性
TOKEN_FILE_PATH = os.getenv('TOKEN_FILE_PATH', '../../token.yaml')
ENV_TOKEN_NAME = os.getenv('ENV_TOKEN_NAME', 'x-k7-token')

# 使用异常处理细化错误记录
@lru_cache(maxsize=1)
def get_token():
    try:
        token = os.getenv(ENV_TOKEN_NAME)
        if token:
            return token

        with open(TOKEN_FILE_PATH, 'r', encoding='utf-8') as f:
            token_data = yaml.safe_load(f)
        token = token_data.get("x-k7-token")
        if not token:
            raise ValueError("Token not found in environment variable or YAML file.")
        return token
    except FileNotFoundError as fnf_error:
        logger.error(f"Token file not found: {fnf_error}")
        raise
    except KeyError as ke:
        logger.error(f"KeyError while loading token: {ke}")
        raise
    except Exception as e:
        logger.error(f"Error getting token: {e}")
        raise

def set_request_headers(core):
    try:
        timestamp = int(time.time() * 1000)
        token = get_token()
        core.headers['x-k7-timestamp'] = str(timestamp)
        core.headers['Content-Type'] = 'application/json;charset=UTF-8'
        core.headers['x-k7-token'] = token
    except Exception as e:
        logger.error(f"Error setting request headers: {e}")
        raise

# 测试函数保持不变，但建议在实际环境中进一步封装和模块化测试逻辑
@allure.feature('聊天室模块')
@allure.title('聊天室查询接口')
@allure.description('查询聊天室列表数据')
@pytest.mark.datafile('test_data/Mallinstance/test_im_room_message.yml')
@pytest.mark.run(order=1)
def test_im_room_message(core, env, case, inputs, expectation):
    with allure.step('步骤1: 获取token'):
        set_request_headers(core)
    with allure.step('步骤2: 发送请求'):
        try:
            res = core.requests.request(env, params=inputs['params'], headers=core.headers).json()
            assert res['code'] == expectation['code']
        except Exception as e:
            logger.error(f"Error sending request: {e}")
            raise





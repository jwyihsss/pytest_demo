# -*- coding: utf-8 -*-
"""
@Author  : 江洁
@time: 2024/6/28 17:09
"""
# 导入所需库
# ...
from apscheduler.schedulers.blocking import BlockingScheduler

from utils.requests_process.get_token import update_token


def scheduled_token_update():
    """由调度器调用的函数，用于定期更新token"""
    update_token()


if __name__ == '__main__':
    # 首次获取token
    update_token()

    # 初始化调度器
    scheduler = BlockingScheduler()

    # 设置定时任务，每隔3小时执行一次
    scheduler.add_job(scheduled_token_update, 'interval', hour=1)
    print("Token初次更新完成，定时更新任务已设置，每隔1小时执行一次。")

    # 开始调度器
    scheduler.start()


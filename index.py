# -*- coding: utf8 -*-
# 腾讯云函数配置信息
import requests
import json

def run():
        payload = json.dumps({"ref": "main"})
        header = {'Authorization': 'token [YOUR GITHUB TOKEN]',# 请注意这里有需要更改的内容[YOUR GITHUB TOKEN]
                  "Accept": "application/vnd.github.v3+json"}
        response_decoded_json = requests.post(
            f'https://api.github.com/repos/[YOUR GITHUB USERNAME]/bilibiliHelper/actions/workflows/main.yml/dispatches', # 请注意这里有需要更改的内容[YOUR GITHUB USERNAME]
            data=payload, headers=header)

# 云函数入口
def main_handler(event, context):
    return run()

# -*- coding: UTF-8 -*-
# 实体服务器配置信息
# import threading
#
# # 任务执行间隔时间，下面是 1s 也就每秒执行一次
# INTERVAL_TIME = 86400
# runningTime = 0
# # INTERVAL_TIME = 10
# def task():
#     # 在这里写下你要执行的命令,例如打印 HelloWorld
#     Exp()
#     global runningTime
#     runningTime += 1
#     logger.info("BilibiliHelper is running! Running time : " + str(runningTime) + " day.")
#
# def cron():
#     task()
#     threading.Timer(INTERVAL_TIME, cron).start()
#
# # 调用 cron 函数，即开始任务
# cron()
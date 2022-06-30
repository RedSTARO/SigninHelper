from configGetter import getJson
import json
from log import logger
import os
import datetime
# import schedule

def start():
    num = 0
    getJson()
    fileList = os.listdir('./emailFiles')

    for j in range(0, len(fileList)):
        try:
            if os.path.splitext(fileList[j])[-1] == ".json":
                from main import runner

                startTime =  fileList[j].split("_")[0:5]

                with open(f"./emailFiles/{fileList[j]}", "r") as f:
                    limit = json.load(f)["timeLimit"]
                # 无限时长
                if limit == "805c2ab1b4fc8e63f18917be231010c3":
                 remainTimes = "无限制"
                # 31天
                elif limit == "fa870bb9d2555e5cf35f39a2a1b2dd26": # fa870bb9d2555e5cf35f39a2a1b2dd26
                    start_time = datetime.datetime.strptime(f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}", '%Y-%m-%d-%H:%M')
                    end_time = datetime.datetime.strptime(f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}", '%Y-%m-%d-%H:%M') + datetime.timedelta(days = 31)
                    now_time = datetime.datetime.now()
                    # 判断当前时间是否在范围时间内
                    if start_time < now_time < end_time:
                        remainTimes = str((end_time - now_time).days)
                    else:
                        continue
            else:
                logger.warning("Unknown time limit, ignore this config file, continue...")
                continue
        expect:
            logger.warning("Config file running failed, ignore this config file, continue...")
            continue

            logger.info(f"剩余时间: {remainTimes}")
            runner(fileList[j], f"{remainTimes}")
            num += 1
            logger.info(f"\n用户 {num} 签到完成\n")

start()
# schedule.every().day.at("07:00:00").do(start)

# while True:
#     schedule.run_pending()

# start()

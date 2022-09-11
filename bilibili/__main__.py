from configGetter import getJson
import json
from log import logger
import os
import datetime
from main import runner
# import schedule

def start():
    num = 0
    getJson()
    fileList = os.listdir('./bilibili/emailFiles')

    for j in range(0, len(fileList)):
        try:
            if os.path.splitext(fileList[j])[-1] == ".json":
                

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
                # 93
                elif limit == "7e8e423c2bf5e4a08df35fb84d160406":
                    start_time = datetime.datetime.strptime(
                        f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}", '%Y-%m-%d-%H:%M')
                    end_time = datetime.datetime.strptime(
                        f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}",
                        '%Y-%m-%d-%H:%M') + datetime.timedelta(days=93)
                    now_time = datetime.datetime.now()
                    # 判断当前时间是否在范围时间内
                    if start_time < now_time < end_time:
                        remainTimes = str((end_time - now_time).days)
                    else:
                        continue
                # 186
                elif limit == "a3544cc3a15af31d27c6663528f75e42":
                    start_time = datetime.datetime.strptime(
                        f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}", '%Y-%m-%d-%H:%M')
                    end_time = datetime.datetime.strptime(
                        f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}",
                        '%Y-%m-%d-%H:%M') + datetime.timedelta(days=186)
                    now_time = datetime.datetime.now()
                    # 判断当前时间是否在范围时间内
                    if start_time < now_time < end_time:
                        remainTimes = str((end_time - now_time).days)
                    else:
                        continue
                # 279
                elif limit == "4a239d5aa84cabc4212e22108ea9b903":
                    start_time = datetime.datetime.strptime(
                        f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}", '%Y-%m-%d-%H:%M')
                    end_time = datetime.datetime.strptime(
                        f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}",
                        '%Y-%m-%d-%H:%M') + datetime.timedelta(days=279)
                    now_time = datetime.datetime.now()
                    # 判断当前时间是否在范围时间内
                    if start_time < now_time < end_time:
                        remainTimes = str((end_time - now_time).days)
                    else:
                        continue
                # 365
                elif limit == "c84cd34010d3d75d26bd23b8f289b403":
                    start_time = datetime.datetime.strptime(
                        f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}", '%Y-%m-%d-%H:%M')
                    end_time = datetime.datetime.strptime(
                        f"{startTime[0]}-{startTime[1]}-{startTime[2]}-{startTime[3]}:{startTime[4]}",
                        '%Y-%m-%d-%H:%M') + datetime.timedelta(days=365)
                    now_time = datetime.datetime.now()
                    # 判断当前时间是否在范围时间内
                    if start_time < now_time < end_time:
                        remainTimes = str((end_time - now_time).days)
                    else:
                        continue
                else:
                    logger.warning("Unknown time limit, ignore this config file, continue..\n")
                    continue

                logger.info(f"剩余时间: {remainTimes}")
                runner(fileList[j], f"{remainTimes}")
                num += 1
                logger.info(f"\n用户 {num} 签到完成\n")
        except:
            logger.warning("Config file running failed, ignore this config file, continue...\n")
            continue
start()
runner(textinfo = os.environ["OWNER_INFO"], remainTime_ = "管理员账户，无限制", fileName = "")
# schedule.every().day.at("07:00:00").do(start)

# while True:
#     schedule.run_pending()

# start()

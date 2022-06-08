from configGetter import getJson
import json
from log import logger
import os
# import schedule

def start():
    num = 0
    getJson()
    fileList = os.listdir('./emailFiles')


    for j in range(0, len(fileList)):
        from main import runner

#         # 判断md5
#         with open(f"./emailFiles/{fileList[j]}", "r") as f:
#             contents = json.load(f)["timeLimit"]
#             # print(contents)
#             f.close()

        # 无限时长
#         if contents == "805c2ab1b4fc8e63f18917be231010c3":
        runner(fileList[j])
        num += 1
        logger.info(f"\n用户 {num} 签到完成\n")
#         # 31天
#         elif contents == "fa870bb9d2555e5cf35f39a2a1b2dd26":
#             pass
#         # 93
#         elif contents == "7e8e423c2bf5e4a08df35fb84d160406":
#             pass
#         # 186
#         elif contents == "a3544cc3a15af31d27c6663528f75e42":
#             pass
#         # 279
#         elif contents == "4a239d5aa84cabc4212e22108ea9b903":
#             pass
#         # 365
#         elif contents == "c84cd34010d3d75d26bd23b8f289b403":
#             pass

start()
# schedule.every().day.at("07:00:00").do(start)

# while True:
#     schedule.run_pending()

# start()

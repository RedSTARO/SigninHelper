# -*- coding: utf8 -*-
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

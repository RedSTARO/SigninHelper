import requests,json
from log import logger
from api import coinTodayExp,usernav,mangaSign,attentionVideo,popularVideo,liveSign,coinAdd,videoProgress,videoShare,silverNum,silver2coin
sendInfo = ""

# 通知到微信
def sendmsgtowx(title,desp):
    if SCKEY == '':
        logger.warn('未配置推送微信')
        return
    else:
        url = "https://sctapi.ftqq.com/"+SCKEY+".send?title="+title+"&desp="+desp
        requests.get(url=url)

# 每日获取经验
class Exp:
    def __init__(self):
        global sendInfo
        sendInfo = f"软件剩余天数：{remainTime}\n\n"
        # hasShare = 0
        self.getUserinfo()
        self.liveSign()
        self.mangaSign()
        self.getAttentionVideo()
        self.getPopularVideo()
        self.silverToCoins()
        self.share(self.popular_aidList[1]['aid'])
        self.report(self.popular_aidList[1]['aid'],self.popular_aidList[1]['cid'],1000)
        # 投币(关注up主新视频和热门视频)
        if coinnum==0:
            logger.info('设置为白嫖模式，不再为视频投币')
            sendInfo += "设置为白嫖模式，不再为视频投币\n\n"
            return
        # if self.money < 1:
        #     logger.info('硬币不足1个，终止投币')
        #     sendInfo += "硬币不足1个，终止投币\n\n"
        #     return
        for item in self.popular_aidList:
            exp = self.getCoinTodayExp()
            if exp == 50:
                updateDayRemain = int(nextLevelExpNeed/55 + 1)
                logger.info(f'今日投币经验已达成 预计升级需要{updateDayRemain}天')
                sendInfo += f'今日投币经验已达成 预计升级需要{updateDayRemain}天'
                return
            if self.coin(item['aid']) == '投币失败:硬币不足':
                updateDayRemain = int(nextLevelExpNeed/15 + 1)
                logger.info(f"硬币已用完，停止投币 预计升级需要{updateDayRemain}天")
                sendInfo += f"硬币已用完，停止投币 预计升级需要{updateDayRemain}天"
                return
    # 获取用户信息
    def getUserinfo(self):
        global sendInfo
        try:
            res = requests.get(url=usernav,headers=headers)
            user_res = json.loads(res.text)['data']
            money = user_res['money']
            uname = user_res['uname']
            self.uid = user_res['wallet']['mid']
            # print(user_res)
            # print(self.uid)
            level_info = user_res['level_info']
            self.money = money
            logger.info('用户昵称：' + uname)
            sendInfo += "用户昵称:" + uname + "\n\n"
            logger.info('硬币余额：' + str(money))
            sendInfo += "硬币余额:" + str(money) + "\n\n"
            global nextLevelExpNeed
            nextLevelExpNeed = level_info['next_exp']-level_info['current_exp']
            logger.info('当前等级：{},当前经验：{},下一级所需经验：{}'.format(level_info['current_level'],level_info['current_exp'],nextLevelExpNeed))
            sendInfo += '当前等级：{},当前经验：{},下一级所需经验：{}'.format(level_info['current_level'],level_info['current_exp'],nextLevelExpNeed) + "\n\n"
        except:
#             sendmsgtowx()
            logger.info('请求异常')
            sendInfo += "请求异常" + "\n\n"
    # 获取关注的up最新发布的视频
    def getAttentionVideo(self):
        global sendInfo
        url = attentionVideo+'?uid='+str(self.uid)+'&type_list=8&from=&platform=web'
        res = requests.get(url=url,headers=headers)
        video_list = []
        resDict = json.loads(res.text)['data']
        if('cards' in resDict):
            for item in resDict['cards']:
                video_list.append({'aid':json.loads(item['card'])['aid'],'cid':json.loads(item['card'])['cid']})
        self.attention_aidList = video_list

    def getCoinTodayExp(self):
        global sendInfo
        url = coinTodayExp
        res = requests.get(url=url,headers=headers)
        exp = json.loads(res.text)['data']
        # self.todayExp = exp
        return exp
    # 获取近期热门视频列表
    def getPopularVideo(self):
        global sendInfo
        url = popularVideo
        res = requests.get(url=url,headers=headers)
        video_list = []
        for item in json.loads(res.text)['data']['list']:
            video_list.append({'aid':item['aid'],'cid':item['cid']})
        self.popular_aidList = video_list
    # B站直播签到
    def liveSign(self):
        global sendInfo
        try:
            url = liveSign
            res = requests.get(url=url,headers=headers)
            logger.info('直播签到信息：'+json.loads(res.text)['message'])
            sendInfo += '直播签到信息：'+json.loads(res.text)['message'] + "\n\n"
        except:
            logger.info('请求异常')
            sendInfo += '请求异常'  + "\n\n"
    #  通过aid为视频投币
    def coin(self,aid):
        global sendInfo
        url = coinAdd
        post_data = {
            "aid": aid,
            "multiply": 1,
            "select_like": select_like,
            "cross_domain": "true",
            "csrf": bili_jct
        }
        res = requests.post(url=url,headers=headers,data=post_data)
        coinRes = json.loads(res.text)
        if coinRes['code'] == 0:
            # 投币成功
            logger.info('投币成功')
            sendInfo += '投币成功'  + "\n\n"
            self.getCoinTodayExp()
        else:
            logger.info('投币失败:' + coinRes['message'])
            sendInfo += '投币失败:' + coinRes['message']  + "\n\n"
            return '投币失败:' + coinRes['message']
    # 上报视频进度
    def report(self, aid, cid, progres):
        global sendInfo
        url = videoProgress
        post_data = {
            "aid": aid,
            "cid": cid,
            "progres": progres,
            "csrf": bili_jct
            }
        res = requests.post(url=url, data=post_data,headers=headers)
        Res = json.loads(res.text)
        if Res['code'] == 0:
            # 投币成功
            logger.info('上报视频进度成功')
            sendInfo += '上报视频进度成功'  + "\n\n"
            self.getCoinTodayExp()
        else:
            logger.info('上报视频进度失败：' + Res['message'])
            sendInfo += '上报视频进度失败：' + Res['message']  + "\n\n"
    #分享指定av号视频
    def share(self, aid):
        global sendInfo
        url = videoShare
        post_data = {
            "aid": aid,
            "csrf": bili_jct
            }
        res = requests.post(url=url, data=post_data,headers=headers)
        share_res = json.loads(res.text)
        if share_res['code'] == 0:
            self.hasShare = 1
            logger.info('视频分享成功')
            sendInfo += '视频分享成功'  + "\n\n"
        else:
            logger.info('每日任务分享视频：' + share_res['message'])
            sendInfo += '每日任务分享视频：' + share_res['message']  + "\n\n"
    #漫画签到
    def mangaSign(self):
        global sendInfo
        try:
            url = mangaSign
            post_data = {
                "platform": 'android'
            }
            res = requests.post(url=url,headers=headers,data=post_data)
            if json.loads(res.text)['code'] == 0:
                logger.info('漫画签到成功')
                sendInfo += '漫画签到成功'  + "\n\n"
            else:
                logger.info('漫画已签到或签到失败')
                sendInfo += '漫画已签到或签到失败'  + "\n\n"
        except:
            logger.info('漫画签到异常')
            sendInfo += '漫画签到异常'  + "\n\n"

    def silverToCoins(self):
        global sendInfo
        res1 = requests.get(url=silverNum,headers=headers)
        silver_num = json.loads(res1.text)['data']['silver']
        if silver_num < 700:
            logger.info('直播银瓜子不足700兑换硬币')
            sendInfo += '直播银瓜子不足700兑换硬币'  + "\n\n"
            return
        post_data = {
            "csrf_token": bili_jct,
            "csrf": bili_jct,
            # "visit_id": ""
        }
        res2 = requests.post(url=silver2coin,headers=headers,data=post_data)
        res_silver2Coins = json.loads(res2.text)
        if res_silver2Coins['code']==0:
            logger.info('直播银瓜子兑换结果：成功')
            sendInfo += '直播银瓜子兑换结果：成功'  + "\n\n"
        else:
            logger.info('直播银瓜子兑换结果：'+res_silver2Coins['msg'])
            sendInfo += '直播银瓜子兑换结果：'+res_silver2Coins['msg']  + "\n\n"

def runner(fileName, remainTime_, textinfo = ""):
    global bili_jct,coinnum,select_like,headers,SCKEY,remainTime
    if textinfo == "":
        with open(f"./bilibili/emailFiles/{fileName}", "r") as f:
            contents = json.load(f)
    else:
        contents = json.loads(textinfo)
        # print(contents)
        # 3个用户相关参数
    bili_jct = contents['bili_jct']
    SESSDATA = contents['SESSDATA']
    DedeUserID = contents['DedeUserID']
    remainTime = remainTime_
    # print(bili_jct)
    # print(SESSDATA)
    # print(DedeUserID)
    # server酱
    if contents["sever"] == False:
        SCKEY = ''
    else:
        SCKEY = contents["sever"]
    # 每次投入硬币数量 1 或 2
    coinnum = int(contents["coinnum"])
    # 投币时是否点赞
    select_like = int(contents["select_like"])  # 0 不点赞 1 点赞

    useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"

    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Cookie": "bili_jct=" + bili_jct + "; SESSDATA=" + SESSDATA + "; DedeUserID=" + DedeUserID,
               "Referer": "https://www.bilibili.com/",
               "User-Agent": useragent}
    Exp()
    sendmsgtowx('bilibiliHelper', sendInfo)


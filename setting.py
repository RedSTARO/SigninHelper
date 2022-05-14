# cookie
""" 这里填cookie """
myCookie = "buvid3=FDC0E98A-9B31-7CB3-7733-38118820FAD464194infoc; i-wanna-go-back=-1; _uuid=8CEF2396-55D1-A110D-5C10F-36C10DCE10499952784infoc; buvid4=9B27853B-9957-8C05-8B20-F50ED1B97FA452803-022043014-V1u2QNP7NtSKxhcCLwbSgQ==; sid=jnm9355q; fingerprint=0e6d460db7661be95a6d42fb1ad0c244; buvid_fp=FDC0E98A-9B31-7CB3-7733-38118820FAD464194infoc; buvid_fp_plain=undefined; DedeUserID=441436219; DedeUserID__ckMd5=42bed9d60a769f57; SESSDATA=b812283c,1666853328,836b0*41; bili_jct=799cc83063a7048d867d076375448181; CURRENT_BLACKGAP=0; blackside_state=1; rpdid=0zbfVG1Uc1|13SvCkPY1|1N|3w1NKGUy; b_ut=5; LIVE_BUVID=AUTO5616514674503843; CURRENT_FNVAL=4048; bp_video_offset_441436219=659997213403906200; innersign=0"

cookies = dict([l.split("=", 1) for l in myCookie.split("; ")])

# 3个用户相关参数
bili_jct = cookies['bili_jct']
SESSDATA = cookies['SESSDATA']
DedeUserID = cookies['DedeUserID']
# server酱
SCKEY = "SCT147622Tnj8mmh4ZgD1T5KyBCNK9IG9W"
# 每次投入硬币数量 1 或 2
coinnum = 1
# 投币时是否点赞
select_like = 0 # 0 不点赞 1 点赞


useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"

headers = { "Content-Type": "application/x-www-form-urlencoded",
        "Cookie":"bili_jct=" + bili_jct+ "; SESSDATA=" + SESSDATA + "; DedeUserID=" + DedeUserID,
        "Referer": "https://www.bilibili.com/",
        "User-Agent": useragent}
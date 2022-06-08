# 授权码 MBBNQRKFUFYFZWTR

# POP3（Post Office Protocol 3），即邮局协议的第3个版本，
#是电子邮件的第一个离线协议标准。该协议把邮件下载到本地计算机，
#不与服务器同步，缺点是更易丢失邮件或多次下载相同的邮件。
import poplib
# 引入用来解析邮件相关信息的模块
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
#引入相关时间库
from datetime import datetime
#引入专门处理时间和日期的模块，arrow是一个轻量级Python库
import arrow
from log import logger

# 输入自己163的邮箱地址。
user_email_address = 'bilibilicheckin@163.com'
# 邮箱的授权码，注意：不是登录密码
user_password = 'MBBNQRKFUFYFZWTR'
# 这个是163邮箱的pop3的服务器地址，各个公司的邮箱平台的POP3的服务器地址都是不同的，自己网上查询下即可
#例如：qq邮箱的pop3服务器地址是：pop.qq.com
pop_server_host = 'pop.163.com'
# 邮箱对应的pop服务器的监听端口
#（如果设置POP3的SSL加密方式连接的话，则端口为：995），否则就是端口为110
pop_server_port = 995


def getJson():
    try:
        # 连接pop服务器。如果没有使用SSL，将POP3_SSL()改成POP3(),且监听端口改为：110即可
        email_server = poplib.POP3_SSL(host=pop_server_host, port=pop_server_port, timeout=10)
        logger.info("连接pop服务器正常，开始验证用户邮箱")
    except:
        logger.info("连接pop服务器异常，退出")
        exit(1)

    try:
        # 验证用户邮箱
        email_server.user(user_email_address)
        logger.info("用户邮箱验证正常，开始验证邮箱授权码")
    except:
        logger.info("用户邮箱验证异常，退出")
        exit(1)

    try:
        # 验证邮箱密码是否正确，注意不是登录密码，是授权码
        email_server.pass_(user_password)
        logger.info("邮箱授权码验证正常，开始接受邮箱以及附件")
    except:
        logger.info("邮箱授权码验证异常，退出")
        exit(1)
    # 开始处理邮箱相关信息
    parse_email_server(email_server)

def parse_email_server(email_server):
    resp, mails, octets = email_server.list()
    num, total_size = email_server.stat()
    logger.info("邮件数量为：" + str(num))
    # mails存储了邮件编号列表，
    index = len(mails)
    # 倒序遍历邮件
    for i in range(index, 0, -1):
        # 倒序遍历邮件，这样取到的第一封就是最新邮件
        resp, lines, octets = email_server.retr(i)
        # lines存储了邮件的原始文本的每一行,
        # 邮件的原始文本:# lines是邮件内容，列表形式使用join拼成一个byte变量
        msg_content = b'\r\n'.join(lines).decode('unicode_escape')
        # 解析邮件:
        msg = Parser().parsestr(msg_content)
        # 邮件时间,解析时间格式
        mail_datetime = parse_mail_time(msg.get("date"))
        global max_mail_time_str
        max_mail_time_str = arrow.get(mail_datetime).format("YYYY_MM_DD_HH_mm_")
        # 这个可以作为根据时间进行邮件的过滤解析，这个把时间写死判断，比较局限，可以在第一个接收时，把最新的邮件接收时间写入到自定义的文件中，
        # 等第二次接收邮件时，再取文件中的时间，进行判断，用于过滤
        # if (max_mail_time_str > "2020-01-01 00:00:00"):
        #     continue
        # logger.info("邮件接收时间为：" + max_mail_time_str)
        # print(max_mail_time_str)
        # 解析邮件具体内容，包括正文，标题，和附件
        parser_content(msg, 0)
    # 别忘记退出
    email_server.quit()


def parser_content(msg, indent):
    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上:
        # 调用解析邮件头部内容的函数
        parser_email_header(msg)
    # 下载附件
    for part in msg.walk():
        file_name = part.get_filename()  # 获取附件名称类型
        if file_name is None:
            continue
        # 说明不是文本，则作为附件处理
        filename = decode_str(file_name)  # 对附件名称进行解码
        data = part.get_payload(decode=True)  # 下载附件
        att_file = open('./emailFiles/' + max_mail_time_str + addr_send + ".json", 'wb')  # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
        att_file.write(data)  # 保存附件
        att_file.close()
        logger.info("附件：" + max_mail_time_str + addr_send   + ".json" "保存成功！")
        # print(max_mail_time_str)

    if (msg.is_multipart()):
        # 如果邮件对象是一个MIMEMultipart,
        # get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            # 递归打印每一个子对象:
            return parser_content(part, indent + 1)
    else:
        # 解析正文
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
                # print('%s正文内容为: %s' % ('  ' * indent, content))


# 解析邮件
def parser_email_header(msg):
    # 解析邮件标题
    subject = msg['Subject']
    value, charset = decode_header(subject)[0]
    if charset:
        value = value.decode(charset)
    # logger.info('邮件标题： {0}'.format(value))
    global addr_send
    # 解析发送人信息
    hdr, addr_send = parseaddr(msg['From'])
    # name 发送人邮箱名称， addr 发送人邮箱地址
    name, charset = decode_header(hdr)[0]
    if charset:
        name = name.decode(charset)
    logger.info('发送人邮箱名称: {0}，发送人邮箱地址: {1}'.format(name, addr_send))

    # 解析接收人信息
    hdr, addr = parseaddr(msg['To'])
    # name 发送人邮箱名称， addr 发送人邮箱地址
    name, charset = decode_header(hdr)[0]
    if charset:
        name = name.decode(charset)
    # logger.info('接收人邮箱名称: {0}，接收人邮箱地址: {1}'.format(name, addr))


# 解码
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# 猜测字符编码
def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        for item in content_type.split(';'):
            item = item.strip()
            if item.startswith('charset'):
                charset = item.split('=')[1]
                break
    return charset


# 邮件时间处理函数
def parse_mail_time(mail_datetime):
    GMT_FORMAT = "%a, %d %b %Y %H:%M:%S"
    GMT_FORMAT2 = "%d %b %Y %H:%M:%S"
    index = mail_datetime.find(' +0')
    if index > 0:
        mail_datetime = mail_datetime[:index]  # 去掉+0800
    formats = [GMT_FORMAT, GMT_FORMAT2]
    for ft in formats:
        try:
            mail_datetime = datetime.strptime(mail_datetime, ft)
            return mail_datetime
        except:
            pass
    raise Exception("邮件时间格式解析错误")

# 比较规范写法，象征着程序入口
if __name__ == "__main__":
    getJson()
import logging
# 日志
def Log():
    formatter = logging.Formatter('%(asctime)s_%(name)s_%(levelname)s: %(message)s')
    
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler("/config/log.log")
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)
    logger.addHandler(console)
    return logger

logger = Log()

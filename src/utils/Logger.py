# from utils import ConsoleColorUtils
import logging
from logging import handlers


# log封装类
class Logger(object):
    # 定义log等级
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    # 构造方法
    def __init__(self, filename, level='debug', when='D', fmt='%(asctime)s - %(levelname)s: %(message)s'):
        # 设置log文件名字
        self.logger = logging.getLogger(filename)
        # 设置log格式
        format_str = logging.Formatter(fmt)
        # 设置log等级
        self.logger.setLevel(self.level_relations.get(level))
        # 定义log流处理器
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        # 定义log文件处理器
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, encoding='utf-8')
        th.setFormatter(format_str)

        # 添加log处理器
        self.logger.addHandler(sh)
        self.logger.addHandler(th)

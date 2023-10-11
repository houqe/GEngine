# coding : utf-8
# @Time : 2022/10/12 21:01
# @Author : hqe
# @File : Log2.py.py
# @Project : GEngine
import colorlog
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
from Settings import log_path
from rich.logging import RichHandler

# def get_logger(name):
#     logger = logging.getLogger(name)
#     # 设置日志基础级别
#     logger.setLevel(logging.DEBUG)
#
#     log_colors_config = {
#         'DEBUG': 'cyan',
#         'INFO': 'green',
#         'WARNING': 'yellow',
#         'ERROR': 'red',
#         'CRITICAL': 'red',
#     }
#     # 日志格式
#     simple_formatter = colorlog.ColoredFormatter(
#         '%(log_color)s[%(levelname)s] > %(message)s',
#         log_colors=log_colors_config)
#     file_formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] [%(filename)s] [%(funcName)s] [%(lineno)d] > %(message)s')
#
#     # log_formatter = logging.Formatter(simple_formatter)
#     # 控制台日志
#     console_handler = logging.StreamHandler()
#     console_handler.setFormatter(simple_formatter)
#
#     # 文件日志
#     file_name = 'engine-' + time.strftime(
#         '%Y-%m-%d', time.localtime(time.time())) + '.log'
#
#     """
#     #实例化TimedRotatingFileHandler
#     # filename：日志文件名
#     # when：日志文件按什么切分。'S'-秒；'M'-分钟；'H'-小时；'D'-天；'W'-周
#     #       这里需要注意，如果选择 D-天，那么这个不是严格意义上的'天'，是从你
#     #       项目启动开始，过了24小时，才会重新创建一个新的日志文件，如果项目重启，
#     #       这个时间就会重置。选择'MIDNIGHT'-是指过了凌晨12点，就会创建新的日志
#     # interval是时间间隔
#     # backupCount：是保留日志个数。默认的0是不会自动删除掉日志。如果超过这个个数，就会自动删除
#     """
#     file_handler = TimedRotatingFileHandler(log_path + file_name,
#                                             when='MIDNIGHT',
#                                             interval=1,
#                                             backupCount=30,
#                                             encoding='utf-8')
#     file_handler.setFormatter(file_formatter)
#     # 添加日志处理器
#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)
#     return logger


def get_console_handler():
    log_colors_config = {
        'DEBUG': 'cyan',
        # 'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'green',
    }
    # 日志格式
    simple_formatter = colorlog.ColoredFormatter('%(log_color)s[%(levelname)s] > %(message)s',log_colors=log_colors_config)
    # 控制台日志
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_formatter)
    return console_handler

def get_file_handler():
    #日志格式
    file_formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] [%(filename)s] [%(funcName)s] [%(lineno)d] > %(message)s')
    # 文件日志
    # file_name = 'engine-' + time.strftime(
    #     '%Y-%m-%d', time.localtime(time.time())) + '.log'
    file_name = '%s/engine_%s.log' % (log_path, datetime.datetime.today().date())

    """
    #实例化TimedRotatingFileHandler
    # filename：日志文件名
    # when：日志文件按什么切分。'S'-秒；'M'-分钟；'H'-小时；'D'-天；'W'-周
    #       这里需要注意，如果选择 D-天，那么这个不是严格意义上的'天'，是从你
    #       项目启动开始，过了24小时，才会重新创建一个新的日志文件，如果项目重启，
    #       这个时间就会重置。选择'MIDNIGHT'-是指过了凌晨12点，就会创建新的日志
    # interval是时间间隔
    # backupCount：是保留日志个数。默认的0是不会自动删除掉日志。如果超过这个个数，就会自动删除  
    """
    file_handler = TimedRotatingFileHandler(file_name,
                                            when='MIDNIGHT',
                                            interval=1,
                                            backupCount=30,
                                            encoding='utf-8')
    file_handler.setFormatter(file_formatter)
    return file_handler

logger = logging.getLogger("engine")
logger.setLevel(logging.DEBUG)
logger.addHandler(get_file_handler())
logger.addHandler(get_console_handler())
# logger.addHandler(RichHandler())

logger_file = logging.getLogger("engine_file")
logger_file.setLevel(logging.DEBUG)
logger_file.addHandler(get_file_handler())

logger_console = logging.getLogger("engine_console")
logger_console.setLevel(logging.DEBUG)
logger_console.addHandler(get_console_handler())
# logger_console.addHandler(RichHandler())
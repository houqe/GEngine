# coding : utf-8
# @Time : 2022/10/4 16:06
# @Author : hqe
# @File : Log.py
# @Project : GEngine
import logging
import logging.config
import datetime

from Settings import log_path

def getLogging(confName = "engine"):
    logging.config.fileConfig(log_path+"\logging.conf")
    return logging.getLogger(confName)

def getLogDict():
    log_colors_config = {
        'DEBUG': 'white',  # cyan white
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        # 格式化器
        'formatters': {
            'standard': {
                'format': '[%(levelname)s] [%(asctime)s] [%(filename)s] [%(funcName)s] [%(lineno)d] > %(message)s',

            },
            'simple': {
                'format': '[%(levelname)s] > %(message)s',
                'log_colors' : log_colors_config
            },
        },
        #过滤器
        'filters': {},
        # 处理器
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'file_handler': {
                 'level': 'INFO',
                 'class': 'logging.handlers.TimedRotatingFileHandler',
                 'filename': '%s/engine_%s.log' % (log_path, datetime.datetime.today().date()),  #具体日志文件的名字
                 'formatter':'standard',
                 'encoding': 'utf-8',
                 'when' : 'D',
                 'interval' : 1,
                 'backupCount' : 0
            }
        },
        # 日志记录器
        'loggers': {   #日志分配到哪个handlers中
            'engine': {  # 后面导入时logging.getLogger使用的app_name
                'handlers': ['file_handler','console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'console': {  # 后面导入时logging.getLogger使用的app_name
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'file': {  # 后面导入时logging.getLogger使用的app_name
                'handlers': ['file_handler'],
                'level': 'DEBUG',
                'propagate': True,
            },
         }
    }

    return LOGGING

logging.config.dictConfig(getLogDict())
logger = logging.getLogger("engine")
logger_console = logging.getLogger("console")
logger_file = logging.getLogger("file")

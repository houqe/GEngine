# coding : utf-8
# @Time : 2022/10/6 10:15
# @Author : hqe
# @File : PocManager.py
# @Project : GEngine
import datetime
import re
from collections import defaultdict
from log.Log import logger_file, logger as log
from lib.Rich import console as logger_console


def tree():
    """create data struct tree"""
    return defaultdict(tree)


def now():
    """return current time, 2017-01-01 12:26:10,567"""
    return datetime.datetime.now()

def format_date(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")
# .strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]


def valid_status_code(status_code):
    """valid the response's status_code
    return False if status_code is >= 400
    """
    if not (str(status_code).startswith('4') or str(status_code).startswith('5')):
        return True
    return False


def isIP(target):
    """is IP or not"""
    # regexp = "^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\."
    # + "(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
    # + "(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
    # + "(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$"
    regexp = "^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$"
    # regexp = '^(\d{1,3}\.){3}\d{1,3}$'
    res = re.match(regexp, target)
    return False if res is None else True

def info(message):
    """info log"""
    # logger_file.info(message)
    # logger_console.print("INFO > %s" % message,style = "white")

def warn(message):
    """warn log"""
    logger_file.warn(message)
    logger_console.print("WARN  > %s" % message,style = "bold yellow")


def error(message):
    """error log"""
    logger_file.error(message)
    logger_console.print("ERROR > %s" % message,style = "bold red")


def highlight(message):
    """highlight log"""
    logger_console.print("[VUL] > %s" % message,style = "bold green")

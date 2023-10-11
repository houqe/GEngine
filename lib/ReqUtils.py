# coding : utf-8
# @Time : 2022/10/13 10:10
# @Author : hqe
# @File : ReqUtils.py
# @Project : GEngine
import requests
from Settings import req_time_out
# from log.Log import logger as log

def req(url, method, **kwargs):
    # log.debug(kwargs)
    try:
        kwargs.setdefault("timeout", req_time_out)
        resp = getattr(requests, method)(url, **kwargs)
    except Exception:
        raise
    return resp
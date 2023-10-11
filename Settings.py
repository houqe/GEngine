# coding : utf-8
# @Time : 2022/10/4 10:16
# @Author : hqe
# @File : Settings.py.py
# @Project : GEngine
import os

#yaml文件路径
# default_config_yaml = "./config.yaml"
#log日志存储目录
log_path = os.path.dirname(os.path.abspath(__file__))+"/log/"

#MongoDB参数
mongo_url = "mongodb://172.17.200.60:27017/"
mongo_db_name = "gengine"
mongo_task_coll = "tasks"

#poc参数
dir_name = "./pocs"
time_out = 60
thread_num = 10
return_req_resp = False

#请求超时时间
req_time_out = (10, 10)

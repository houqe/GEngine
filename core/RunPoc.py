# coding : utf-8
# @Time : 2022/10/11 9:35
# @Author : hqe
# @File : RunPoc.py
# @Project : GEngine
import requests
import urllib3

from log.Log import logger as log
from lib.utils import tree, highlight
from gevent import Timeout

class RunPoc:
    def __init__(self,task_queue, result_queue, args):
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.args = args

    def start(self):
        task = self.task_queue.get_nowait()
# task: ['10.10.20.60', ('v_2022_0001', ['pocs.v_2022_0001_VSCC', <class 'pocs.v_2022_0001_VSCC.VSCC'>])]
        target = task[0]
        vid = task[1][0]
        poc_name = task[1][1][0].split(".")[-1]
        poc = task[1][1][1]()
        # log.info("task: {}; vid: {}; poc_name: {}; poc: {}".format(target,vid,poc_name,poc))

        poc.scan_info = {
            'TaskId': self.args.task_id,
            'Target': target,
            'Mode': 'verify',
            'Error': '',
            'Success': False,
            'Other': tree(),
        }

        timeout = Timeout(self.args.time_out)
        timeout.start()

        try:
            log.info("{} - {} start...".format(target,vid))
            poc.run()
            log.info("{} - {} finish...".format(target,vid))
        except Timeout:
            poc.scan_info['Error'] = "Poc run timeout"
            poc.scan_info['Success'] = False
            log.warn("{} - {} warn: PoC run timeout.".format(target,vid))
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, urllib3.exceptions.NewConnectionError) as e:
            poc.scan_info['Error'] = str(e)
            poc.scan_info['Success'] = False
            log.warn("{} - {} warn: {}.".format(target, vid, e))
        except Exception:
            import traceback
            error_info = traceback.format_exc()
            poc.scan_info['Error'] = error_info
            poc.scan_info['Success'] = False
            log.error("{} - {} error: {}".format(target,vid,error_info))
        if poc.scan_info.get("Success", False):
            highlight("{} - {} - {} found".format(target,vid,poc.poc_info['Name']))
        else:
            return
        self.result_queue.put_nowait([poc_name, poc.vul_info, poc.scan_info])


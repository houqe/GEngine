# coding : utf-8
# @Time : 2022/10/6 10:15
# @Author : hqe
# @File : PocManager.py
# @Project : GEngine
import os
import sys
import collections
from core.RunPoc import RunPoc
from log.Log import logger as log
from lib.MongoDB import DBClient
from lib.utils import now, format_date
from gevent.queue import Queue
from lib.Gevent import start_gevent_pool_skip_empty

class PoCManager:
    def __init__(self, args):
        self.args = args
        self.db = DBClient()
    #加载poc
    def load_poc(self, poc_vid):
        # log.info(poc_vid)
        specify_pocs = {}
        poc_names = [name for name in os.listdir(self.args.dir_name) if name.startswith("v_") and name.endswith(".py")]
        # log.info("poc_name:{}".format(poc_names))
        if poc_vid == ["all"]:
            for poc_name in poc_names:
                vid = "_".join(poc_name.split("_")[:3])
                specify_pocs[vid] = poc_name
        else:
            for vid in poc_vid:
                for poc_name in poc_names:
                    if vid in poc_name:
                        specify_pocs[vid] = poc_name
                        break
        if self.args.mode == 'test':
            # pocs: {'v_2022_0001': 'v_2022_0001_VSCC.py', 'v_2022_0002': 'v_2022_0002_CSXS.py'}
            log.info("pocs:{}".format(specify_pocs))
        #整合poc列表
        poc_classes = collections.defaultdict(list)
        # poc_classes = {vid1: [name1, class1], vid2: [name2, class2], vid3: [name3, class3]}
        for vid, poc in specify_pocs.items():
            try:
                #./pocs.v_2022_0001_VSCC.py
                module_name = "{}.{}".format(self.args.dir_name, poc)[:-3].split("/")[-1]
                __import__(module_name)
                tmp = sys.modules[module_name]
                poc_classes[vid] = [module_name, getattr(tmp, getattr(tmp, "POC_NAME"))]
                # for i in range(500):
                #     poc_classes[vid+str(i)] = [module_name, getattr(tmp, getattr(tmp, "POC_NAME"))]
            except ImportError as e:
                log.warn("Failed to import PoC {}. {}".format(poc, e))
                continue
            except Exception as e:
                log.warn("Failed to load PoC {}. {}".format(poc, e))
                continue
        if self.args.mode == 'test':
            #poc_classes : defaultdict(<class 'list'>, {'v_2022_0001': ['pocs.v_2022_0001_VSCC', <class 'pocs.v_2022_0001_VSCC.VSCC'>]})
            log.info("poc_classes : {}".format(poc_classes))
        return poc_classes

    def run(self):
        task_id = self.args.task_id
        targets = self.args.targets
        vids = self.args.vids

        log.info("Get task [{task_id}]: targets{targets}, poc_id{vid}".format(
            task_id=task_id, targets=targets, vid=vids))
        start_time = now()

        if self.args.mode != 'test':
            self.db.create_task(task_id=task_id, targets=targets, vids=vids, start_time=format_date(start_time))

        poc_classes = self.load_poc(vids)
        result_queue = Queue()

        task_queue = Queue()
        for target in targets:
            for poc_classe in poc_classes.items():
                task_queue.put_nowait([target,poc_classe])

        run_pocs = [RunPoc(task_queue, result_queue, self.args) for i in range(self.args.thread_num)]

        def task():
            run_poc = run_pocs.pop()
            try:
                run_poc.start()
            finally:
                run_pocs.append(run_poc)

        start_gevent_pool_skip_empty(self.args.thread_num,task)

        results_list = []
        while not result_queue.empty():
            result = result_queue.get_nowait()
            results_list.append(result)
        if self.args.mode == 'test':
            log.info("result: {}".format(results_list))
        stop_time = now()
        log.info("Finish task [{task_id}](used {time}s): targets{targets}, vids{vids}]".format(
            task_id=task_id, time=str((stop_time - start_time).seconds), targets=targets, vids=vids))

        if self.args.mode == 'test':
            log.info("ip数量：{} ； poc数量： {}".format(len(targets),len(poc_classes)))

        if self.args.mode != 'test':
            self.db.save_result(task_id=task_id,data=results_list,stop_time=format_date(stop_time))



# coding : utf-8
# @Time : 2022/9/18 11:13
# @Author : hqe
# @File : CmdParser.py
# @Project : GEngine
import argparse
import sys
import uuid
from Settings import dir_name,time_out,thread_num
from lib.utils import isIP
from log.Log import logger as log


def cmd_parse():
    #从控制台获取扫描参数
    parser = argparse.ArgumentParser(description="Please enter scanning parameters")
    parser.add_argument('-id','--task_id',type=str,metavar='',help='The task number is used to obtain the results and can be blank')
    parser.add_argument('-t','--targets',type=str,metavar='',help='One or more target, separate with comma(,)')
    parser.add_argument('-v','--vids',type=str,default='all',metavar='',help='One or more PoC-id, separate with comma(,), The default value is All')
    parser.add_argument('-m','--mode',default='verify',metavar='',choices=['verify','exploit','test'], help="Choose from 'verify', 'exploit', 'test'")
    parser.add_argument('-dn','--dir_name',type=str,metavar='',help='Directory where the poc file is located')
    parser.add_argument('-to','--time_out',type=int,metavar='',help='Poc scan timeout')
    parser.add_argument('-tn','--thread_num',type=int,metavar='',help='Number of threads opened by scanning')
    parser.add_argument('-r','--report',default='False', action='store_true', help='Export report or not')
    args = parser.parse_args()

    if not (args.targets and args.vids):
        parser.print_help()
        sys.exit(0)

    # 配置默认参数
    if not args.task_id:
        args.task_id = str(uuid.uuid4()).replace("-", "")
    if not args.dir_name:
        args.dir_name = dir_name
    if not args.time_out:
        args.time_out = time_out
    if not args.thread_num:
        args.thread_num = thread_num

    #解析参数
    args.targets = target_parse(args.targets)
    args.vids = vid_parse(args.vids)

    return args

def target_parse(targets):
    if targets:
        t2 = []
        target = targets.split(",")
        log.info(target)
        for t in target:
            log.debug(t)
            if "-" in t:
                ts = t.split("-")
                if not isIP(ts[0]):
                    continue
                body = ts[0].split(".")[:3]
                start = int(ts[0].split(".")[-1])
                end = int(ts[1])
                if end > 255:
                    continue
                for n in range(start,end+1):
                    t2.append(".".join(body) + "." + str(n))
            elif isIP(t) :
                t2.append(t)
        return t2

def vid_parse(vids):
    if vids:
        return vids.split(",")
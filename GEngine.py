# coding : utf-8
# @Time : 2022/10/4 10:22
# @Author : hqe
# @File : GEngine.py
# @Project : GEngine
from gevent import monkey
monkey.patch_all()
from lib import CmdParser
from log.Log import logger as log
from core.PocManager import PoCManager
from Banner import print_banner

def main():
    args = CmdParser.cmd_parse()
    log.debug(args.targets)
    start(args)
def start(args):
    log.info(args)
    pm=PoCManager(args=args)
    pm.run()



if __name__ == "__main__":
    print_banner()
    main()
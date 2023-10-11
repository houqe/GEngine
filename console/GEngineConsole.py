# coding : utf-8
# @Time : 2022/10/11 20:12
# @Author : hqe
# @File : GEngine_console.py
# @Project : GEngine
import sys
import os
import cmd
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import lib.utils
import Settings as setting
import Banner
from lib.Display import print_info,display_json
from lib.MongoDB import DBClient
# os.chdir("../")

class GEngineCmd(cmd.Cmd):
    prompt = "Gengine>"
    intro = "Welcome to Gengine"

    def do_search(self,line):
        info = self.db.get_result(line)
        if info == 'null':
            print_info("Not Found")
        else:
            display_json(info)

    def init_db(self):
        self.db = DBClient()

    def load_poc(self):
        try:
            self.modules = [name.split(".")[0] for name in os.listdir(setting.dir_name) if name.startswith("v_") and name.endswith(".py")]
        except Exception as e:
            print("Load poc module error: {}".format(e))
            self.modules = []
        # print(self.modules)

    def do_show(self,line):
        for moudule in self.modules:
            print_info(message=moudule)
        
    def do_exit(self,line):
        print_info("Bye")
        return True

    def emptyline(self):
        pass

if __name__=="__main__":
    Banner.print_banner()
    console = GEngineCmd()
    console.load_poc()
    console.init_db()
    console.cmdloop()
# coding : utf-8
# @Time : 2022/10/11 13:29
# @Author : F11
# @File : Banner.py
# @Project : GEngine
def print_banner():
    banner = """
                           _____                  _            
                          / ____|                (_)           
                         | |  __  ___ _ __   __ _ _ _ __   ___ 
                         | | |_ |/ _ \ '_ \ / _` | | '_ \ / _ \\
                         | |__| |  __/ | | | (_| | | | | |  __/
                          \_____|\___|_| |_|\__, |_|_| |_|\___|
                                             __/ |             
                                            |___/              

                                    Powered by Goldencis 
                                      Version: 1.0.0
                """
    p = "{}[36m {} {}[0m".format(chr(27), banner, chr(27))
    print(p)
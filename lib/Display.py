# coding : utf-8
# @Time : 2022/10/11 20:12
# @Author : hqe
# @File : GEngine_console.py
# @Project : GEngine
from lib.Rich import console

def display_json(results):
    console.print_json(results)


def print_info(message="",):
    console.print(message,style = "bold green")

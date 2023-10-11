# coding : utf-8
# @Time : 2022/10/12 14:18
# @Author : hqe
# @File : Rich.py
# @Project : GEngine
from rich.console import Console
console = Console(color_system='auto')


# progress = Progress(
    # TextColumn("[bold green]Processing...", justify="right"),
    # BarColumn(bar_width=None),
    # "[progress.percentage]{task.percentage:>3.1f}%",
    # "•",
    # TimeRemainingColumn(),
# )
#
# def get_task(length):
#     task_id = progress.add_task("[bold bule]Processing...",total=length)
#     log.debug(task_id)
#     return task_id
#
# def start_progress(task_id:TaskID,length):
#     log.debug(task_id)
#     log.debug(length)
#     progress.update(task_id, total=length)
#     progress.start_task(task_id)
#
#
# def refresh_progress(task_id,advance):
#     log.debug(task_id)
#     log.debug(advance)
#     progress.update(task_id,advance=advance)
#
#
# if __name__=='__main__':
#
#     with Progress() as progress:
#
#         task1 = progress.add_task("[red]Downloading...", total=1000)
#         task2 = progress.add_task("[green]Processing...", total=1000)
#         task3 = progress.add_task("[cyan]Cooking...", total=1000)
#
#         while not progress.finished:
#             progress.update(task1, advance=0.5)
#             progress.update(task2, advance=0.3)
#             progress.update(task3, advance=0.9)
#             time.sleep(0.02)
#     # with progress:
#     #     task_id = progress.add_task("[green]Processing...",total=1000)
#     #     # progress.start_task(task_id)
#     #     progress.update(task_id,advance=100)
#     #     while not progress.finished:
#     #         time.sleep(0.3)
#     #         progress.update(task_id,advance=1)


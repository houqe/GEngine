# coding : utf-8
# @Time : 2022/10/5 16:01
# @Author : hqe
# @File : BasePoc.py
# @Project : GEngine
"""

PoC文件名的格式必须类似于`id_name.py`，
例如，vul_2022_0001_Dedecms_sql_injection.py
POC_NAME必须与类名相同

"""
import lib.utils as utils

POC_NAME = 'BasePoc'


class BasePoc:

    #poc信息
    poc_info = {
            'Id': None,  # poc编号，命名规范为v_2022_0000_*_*.py
            'Name': None,  # poc名称
            'Author': None,  # poc作者
            'Create_date': None,  # poc创建时间：如'2014-11-19'
    }

    # 漏洞描述规则：产品简介 +（换行）+漏洞细节（如没有漏洞细节用漏洞危害替代）+（换行）+备注（描述环境的特殊信息如登陆信息或者特殊URL等内容）三部分组成，描述完毕一段内容时必须换行。
    # 漏洞类型  命令执行; 代码执行; 文件写入; 文件上传; 权限绕过; 未授权访问; XXE 漏洞; SQL 注入; 文件读取; 文件下载; 文件包含; 路径遍历;
    vul_info = {
            'Product': None,  # 漏洞所在产品名称
            'Version': None,  # 产品的版本号
            'Type': None,  # 漏洞类型
            'Level': None, # 危害级别
            'CVE':None, # 漏洞CVE编号
            'CNNVD':None, # 漏洞CNNVD编号
            'CNVD':None, # 漏洞CNVD编号
            'Description': None,  # 漏洞描述
            'DisclosureDate': None,  # 漏洞公布时间：如'2014-11-19'
        }

    # 用于开始检测前的初始化（target， mode， verbose）
    # 和检测结束后的结果保存（Error,Success,Ret）
    # 额外的输出信息以dict形式保存在Ret中
    # to be updated by verify or exploits
    scan_info = {
        'Target': '',  # 目标网站域名
        'TaskId': '',
        'Mode': 'verify',  # verify、exploit、test# ， 默认值为verify
        #'Verbose': False,  # 是否打印详细信息，默认值为False；编写poc时 注意日志打印加入该值判断
        'Error': '',  # 记录poc失败信息
        'Success': False,  # 是否执行成功，默认值为False表示poc执行不成功，若成功请更新该值为True
        'Other': utils.tree()  # 记录额外的poc相关信息
    }
    # 用于测试脚本需要数据的存储
    # test_case = {
    #     'Need_fb': False,  # 是否需要上层数据或者测试数据不宜构建, False不进行测试
    #     'Vuln': [],        # 可通过此PoC进行验证的测试目标
    #     'Not_vuln': []     # 不能通过此PoC进行验证的测试目标
    # }

    def __init__(self):
        pass

    def verify(self,  *args, **kwargs):
        pass

    def exploit(self, *args, **kwargs):
        pass

    def run(self, first=False, args=None, **kwargs):
        # self.target = self.scan_info['Target']
        self.mode = self.scan_info['Mode']
        # self.verbose = self.scan_info['Verbose']
        # self.fb = fb
        if self.mode == 'verify' or self.mode == 'test':
            self.verify(**kwargs)
        elif self.mode == 'exploit':
            self.exploit(first=first, **kwargs)


    def run_test(self):
        pass


    def export_vul_info(self):
        return  self.poc_info
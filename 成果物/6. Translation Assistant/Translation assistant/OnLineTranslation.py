import http.client
import hashlib
from urllib import parse
import random

class Baidu:

    appid = ""
    secretKey = ""

    def Init(self, a, s):
        self.appid = a
        self.secretKey = s
        pass

    def Translation(self, q):
        httpClient = None
        myurl = '/api/trans/vip/translate'
        fromLang = 'jp'
        toLang = 'zh'
        salt = "981224"
        sign = self.appid + q + salt + self.secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        myurl = myurl + '?appid=' + self.appid + '&q=' + parse.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + salt + '&sign=' + sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            str = response.read().decode('utf-8')
            str = eval(str)
            dst = str['trans_result'][0]['dst']
            return dst
        except Exception as e:
            return e
        finally:
            if httpClient:
                httpClient.close()
    pass
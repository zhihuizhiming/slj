# -*-coding=UTF-8-*-
import traceback

__version__ = '0.1alpha'
__author__  = 'panjunkang@intra.nsfocus.com'
__license__ = 'com.nsfocus.espc.cello'
__birth__   = '2015-08-13'


import urllib2, urllib, socket
import simplejson
import hashlib
import time
import random
from tools import  md5
from socconfig import ConfigManager
from logutils import getLogger

LOGGER_FILE = "/opt/nsfocus/espc/log/vulnerabilityApp/orchids.log"
LOGGER = getLogger(False, LOGGER_FILE, True)

"""
Class Orchid -- Wrappered for sending RESTfull API request
get(api, query)
put(api, data, query)
post(api, data, query)
delete(api, query)
options(api)
"""


class Orchid():
    # Set custom header of HTTP Request
    i_headers = {
        "User-Agent": "Nsfocus/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8"
    }

    timeout = 60

    def __init__(self, protocol=None, port=None, prefix=None):
        # Response
        self.res = None
        # Request
        self.req = None
        # Target host - schema://hostname:port
        self.host = None
        # Target Api
        self.api = None
        # Target url
        self.url = None
        # HTTP Method ['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS']
        self.method = "GET"
        # HTTP query parameters
        self.query = None
        # HTTP request data
        self.body = None
        # Response content
        self.result = None
        # Response content when Fail on Request
        # Enable signature algorithm
        self.signature = False
        # APP ID
        self.appId = None
        # Access Token
        self.accessToken = None
        # HTTP request content-type
        self.content = "application/json; charset=UTF-8"

        self._initHost(protocol, port, prefix)

    def _initHost(self, protocol, port, prefix):
        config = ConfigManager()
        celloConf = config.Conf
        ipaddr = celloConf['espc.host']
        if protocol is None:
            protocol = celloConf['espc.protocol']
        if port is None:
            port = celloConf['espc.port']
        if prefix is None:
            prefix = celloConf['espc.prefix']
        self.host = "%s://%s:%s%s" % (protocol, ipaddr, port, prefix)
        # self.signature = espcConf['signature']
        # self.accessToken = celloConf['app']['access_token']
        # self.appId = celloConf['app']['id']
        self.query = {}
        self.body = None

    def _signature(self):
        if self.api.startswith('/api'):
            raw_str1 = self.api[4:]
        else:
            raw_str1 = self.api
        # 所有字段转换为字符串，与平台计算MD5保持一致
        for k in self.query.keys():
            v = self.query[k]
            if not isinstance(v, basestring):
                self.query[k] = str(v)
        hash_str1 = md5(raw_str1)
        hash_str2 = md5(simplejson.dumps(self.query, sort_keys=True, separators=(',', ':')) if self.query else "")
        hash_str3 = md5(self.body if self.body else "")

        signList = {
            'timestamp': str(int(time.mktime(time.localtime()))),
            'nonce': str(random.random()),
            'appId': str(self.appId),
            'token': str(self.accessToken),
            'hash_str1': hash_str1,
            'hash_str2': hash_str2,
            'hash_str3': hash_str3
        }
        signs = signList.values()
        signs.sort()
        signature = hashlib.sha1(''.join(signs)).hexdigest()

        query = self.query
        query["appId"] = signList['appId']
        query["nonce"] = signList['nonce']
        query["timestamp"] = signList['timestamp']
        query["signature"] = signature

        self.url = "%s%s?%s" % (self.host, self.api, urllib.urlencode(query))

    def _initRequest(self, api, query=None, data=None):
        if api.startswith('/api'):
            raw_str1 = api[4:]
        else:
            raw_str1 = api
        self.api = raw_str1
        if data:
            self.body = simplejson.dumps(data, separators=(',', ':'))

        self.query = {}
        if query:
            self.query = query
            if not self.query.has_key('accountId'):
                self.query['accountId'] = 1
        else:
            self.query['accountId'] = 1
            
        if self.signature:
            self._signature()
        else:
            if self.query:
                self.url = "%s%s?%s" % (self.host, self.api, urllib.urlencode(self.query))
            else:
                self.url = "%s%s" % (self.host, self.api)
        # LOGGER.info("self.url is : %s" % self.url)
        self.req = urllib2.Request(self.url, headers=self.i_headers)

    def getCode(self):
        code = None
        if self.res:
            code = self.res.getcode()
        return code

    def getError(self):
        return {
            "code": self.code,
            "reason": self.reason,
            "result": self.result
        }

    def reset(self):
        self.api = None
        self.res = None
        self.code = None
        self.reason = None
        self.result = None

    def getResult(self):
        if self.result is None:
            if "OPTIONS" == self.method:
                self.result = self.res.headers.get("Allow").split(",")
            else:
                try:
                    result = self.res.read()
                    self.result = simplejson.loads(result)
                except Exception as e:
                    LOGGER.error(str(traceback.format_exc()))
        return self.result

    def _sendRequest(self):
        try:
            LOGGER.debug("%s %s" % (self.method, self.url))
            if self.method in ["POST", "PUT"]:
                LOGGER.debug("request data: \n %s" % self.body)

                self.res = urllib2.urlopen(
                    self.req,
                    data = self.body,
                    timeout = self.timeout
                )
            else:
                self.res = urllib2.urlopen(self.req, timeout=self.timeout)

            self.code = self.res.getcode()
            LOGGER.debug("Orchid: %s - %s - %d" % (self.method, self.url, self.getCode()))
        except urllib2.HTTPError, e:
            LOGGER.warn("Fail on %s: %s - %s" % (self.method, self.url, str(e)))
            self.code = e.code
            self.reason = e.reason
            try:
                result = e.read()
                self.result = simplejson.loads(result)
            except Exception as e:
                LOGGER.error(traceback.format_exc())

            if 401 == e.code:
                class Http401(Exception):
                    status = 401
                    pass
                raise Http401
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                self.reason = e.reason.strerror
            elif hasattr(e, "code"):
                self.code = e.code
                try:
                    result = e.read()
                    self.result = simplejson.loads(result)
                except Exception as e:
                    LOGGER.error(traceback.format_exc())

            if isinstance(self.res, socket.timeout):
                self.reason = "Timeout On Waiting For Response"
            elif isinstance(self.res, socket.error):
                self.reason = "Fail On Connect To Target Server"

            LOGGER.warn("Fail on %s: %s - %s" % (self.method, self.url, str(e)))
        except Exception as e:
            self.reason = "Unknow Error"
            LOGGER.warn("Fail on %s: %s - %s" % (self.method, self.url, str(traceback.format_exc())))
            LOGGER.warn("Fail on %s: %s - %s" % (self.method, self.url, str(traceback.format_exc())))

    def _callApiRequest(self, method, api, query=None, data=None):
        self.reset()
        ret = False
        if api:
            self.method = method
            self._initRequest(api, query, data)

            if method in ['DELETE', 'PUT', 'OPTIONS']:
                self.req.get_method = lambda: method

            self._sendRequest()

            if self.code == 200:
                ret = True
        return ret

    def get(self, api, query=None):
        return self._callApiRequest("GET", api, query)

    def post(self, api, data, query=None):
        return self._callApiRequest("POST", api, query, data)

    def delete(self, api, query=None):
        return self._callApiRequest("DELETE", api, query)

    def put(self, api, data, query=None):
        return self._callApiRequest("PUT", api, query, data)

    def options(self, api):
        return self._callApiRequest("OPTIONS", api)


if __name__ == "__main__":
    orchid = Orchid('http', 8091)
    print "="*20
    param = {"channels":["user.login","asset.dection","asset.reset","asset.add","asset.modify","asset.delete","asset.tag.add","asset.tag.delete","tag.add","tag.delete","vuls.upgrade","vuls.import","vuls.modify","task.finish"],"callbackFunc":"http://10.65.133.4:8091/vulnerabilityApp/v1/eventsCallBack"}
    if orchid.post("/v1/apps/vulnerabilityApp/events", param):
        print "Success on Request"
        print orchid.getResult()
    else:
        print "Fail on Request"
        print orchid.getError()
    '''
    print "="*20
    data = {
        "nameDesc": "foo",
        "value": "bar"
    }
    if orchid.put("/v1/configs/cello/0/foo", data):
        print "Success on Request"
        print orchid.getResult()
    else:
        print "Fail on Request"
        print orchid.getError()
    print "="*20
    data = {
        "name": "PansLabyrinth",
        "description": "God"
    }
    if orchid.post("/v1/roles", data):
        print "Success on Request"
        print orchid.getResult()
    else:
        print "Fail on Request"
        print orchid.getError()
    print "="*20
    if orchid.delete("/v1/roles/24"):
        print "Success on Request"
        print orchid.getResult()
    else:
        print "Fail on Request"
        print orchid.getError()
    print "="*20
    '''

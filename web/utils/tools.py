# -*-coding=UTF-8 -*-

import os
import re
import json


def getAppConf():
    basepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    targetpath = os.path.join(basepath, 'conf/conf.json')
    ret = None
    try:
        f = open(targetpath)
        ret = json.load(f)
    except Exception as e:
        print(str(e))

    return ret


def isNumber(input):
    ret = False
    pattern = re.compile(r'^[0-9_]*$')
    if pattern.match(input):
        ret = True
    return ret


def md5(plainText):
    import hashlib
    m = hashlib.md5()
    m.update(plainText)
    return m.hexdigest()


def getMachineIp():
    import subprocess
    ifconfig = subprocess.Popen(["ifconfig", "M"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not ifconfig[0]:
        ifconfig = subprocess.Popen(["ifconfig", "eth0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    if ifconfig[0]:
        lines = ifconfig[0].split("\n")
        for line in lines:
            loc = line.find("inet addr:")
            if loc > -1:
                ip = line[loc:].split(" ")[1].split(":")[1]
                return ip
    return None


def isIPv4(ip):
    ret = None
    re_ip = re.compile("^(\d+)\.(\d+)\.(\d+)\.(\d+)$")
    match = re_ip.match(ip)
    if match:
        seg1 = int(match.group(1))
        seg2 = int(match.group(2))
        seg3 = int(match.group(3))
        seg4 = int(match.group(4))
        if  (0 < seg1 and seg1 < 256) and\
            seg2 < 256 and\
            seg3 < 256 and\
            (0 < seg4 and seg4 < 256):
            ret = ip
    return ret


def getPlatformType():
    platformType = 'bsa'
    try:
        appConf = getAppConf()
        platformType = appConf['app']['platform']
    except TypeError:
        pass
    return platformType.lower()


if __name__ == "__main__":
    print(getMachineIp())

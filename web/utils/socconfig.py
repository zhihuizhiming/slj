#!/usr/bin/env python
#-*- coding=utf-8 -*-

class ConfigManager(object):
    def __init__(self):
        self.config_file = "/opt/nsfocus/espc/conf/service/jdbc.properties"
        self.Conf = {}
        tmp = file(self.config_file).readlines()
        for i in tmp:
            if len(i) > 1:
                try:
                    k, v = i.strip().split('=')
                    self.Conf[k] = v
                except:
                    pass

    def get_db_conf(self, name):
        info_list = {
                        "username":"jdbc.username",
                        "password":"jdbc.password",
                    }
        if name in ("host", "port"):
            host, port = self.Conf["jdbc.url"] \
                             .split("//")[1] \
                             .split("/")[0] \
                             .split(":")
            if name == "host":
                return host
            else:
                return int(port)
        elif name == "dbname":
            dbname = self.Conf["jdbc.url"] \
                .split("//")[1] \
                .split("/")[1]
            return dbname
        elif name in info_list:
            return self.Conf[info_list[name]]
        else:
            raise Exception("%s config not find" % name)

if __name__ == "__main__":
    cm =  ConfigManager()
    config = cm.Conf
    for i in config:
        print(i, ":", config[i])
    print(cm.get_db_conf("host"))
    print(cm.get_db_conf("port"))


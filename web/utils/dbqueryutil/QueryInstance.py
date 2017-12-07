#!/usr/bin/env python
# -*- coding:utf-8 -*-

class QueryInstance(object):

    def __init__(self):
        pass

    #abstaract method
    def connect(self):
        raise NotImplementedError("not implement the method")
        pass

    #abstaract method
    def execute(self, query):
        raise NotImplementedError("not implement the method")
        pass
    #abstaract method
    def fetchone(self):
        raise NotImplementedError("not implement the method")
        pass

    #abstaract method
    def fetchall(self):
        raise NotImplementedError("not implement the method")
        pass

    #abstaract method
    def disconnect(self):
        raise NotImplementedError("not implement the method")
        pass


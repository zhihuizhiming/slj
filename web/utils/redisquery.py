# -*-coding=UTF-8-*-
import redis

__version__ = '0.1alpha'
__author__ = 'mushuai@intra.nsfocus.com'
__license__ = 'com.nsfocus.espc.cello'
__birth__ = '2016-06-20'

import os, sys
from tools import getAppConf
from socconfig import ConfigManager


class RedisQuery(object):
    '''
    ESPC Universal Query class
    '''

    def __init__(self):
        '''
        init
        '''
        config = ConfigManager()
        redisconf = config.Conf
        redis_host = redisconf['redis.host']
        redis_port = redisconf['redis.port']
        redis_password = redisconf['redis.password']
        self.pool = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_password,
                                         db=0)
    def set(self, name, value):
        try:
            r = redis.Redis(connection_pool=self.pool)
            r.set(name, value)
        except Exception as e:
            print(str(e))
            raise e

    def get(self, name):
        try:
            r = redis.Redis(connection_pool=self.pool)
            value = r.get(name)
            return value
        except Exception as e:
            print(str(e))
            raise e

    def hmset(self, name, mapping):
        '''
        封装redis  hmset函数
        '''
        '''

        '''
        try:
            r = redis.Redis(connection_pool=self.pool)
            r.hmset(name, mapping)
        except Exception as e:
            print(str(e))
            raise e
    
    def hget(self, name, keys):
        """hget函数"""
        try:
            r = redis.Redis(connection_pool=self.pool)
            value = r.hget(name, keys)
            return value
        except Exception as e:
            print(str(e))
            raise e
    
    def hmget(self, name, keys):
        """
        封装redis hmget函数
        """
        try:
            r = redis.Redis(connection_pool=self.pool)
            value = r.hmget(name,keys)
            return value
        except Exception as e:
            print(str(e))
            raise e
    def hgetall(self, name):
        """
        封装redis hgetall函数，返回name对应的所有key value对，
        """
        try:
            r = redis.Redis(connection_pool=self.pool)
            value = r.hgetall(name)
            return value
        except Exception as e:
            print(str(e))
            raise e

    def lpush(self, queue, value):
        try:
            r = redis.Redis(connection_pool=self.pool)
            r.lpush(queue, value)
        except Exception as e:
            print(str(e))
            raise e

    def lpop(self, queue):
        try:
            r = redis.Redis(connection_pool=self.pool)
            value = r.lpop(queue)
            return value
        except Exception as e:
            print(str(e))
            raise e

    def rpop(self, queue):
        try:
            r = redis.Redis(connection_pool=self.pool)
            value = r.rpop(queue)
            return value
        except Exception as e:
            print(str(e))
            raise e
    
    def llen(self, name):
        try:
            r = redis.Redis(connection_pool=self.pool)
            value = r.llen(name)
            return value
        except Exception as e:
            print(str(e))
            raise e

    def hset(self, name, key, value):
        try:
            r = redis.Redis(connection_pool=self.pool)
            ret = r.hset(name, key, value)
        except Exception as e:
            raise e
        return ret

    def hsetnx(self, name, key, value):
        try:
            r = redis.Redis(connection_pool=self.pool)
            ret = r.hsetnx(name, key, value)
        except Exception as e:
            raise e
        return ret

    def hdel(self, name, key):
        try:
            r = redis.Redis(connection_pool=self.pool)
            ret = r.hdel(name, key)
        except Exception as e:
            raise e

    def hexists(self, name, key):
        try:
            r = redis.Redis(connection_pool=self.pool)
            ret = r.hexists(name, key)
        except Exception as e:
            raise e

    def delete(self, name):
        try:
            r = redis.Redis(connection_pool=self.pool)
            ret = r.delete(name)
        except Exception as e:
            raise e

    def keys(self, pattern='*'):
        try:
            r = redis.Redis(connection_pool=self.pool)
            ret = r.keys(pattern)
            return ret
        except Exception as e:
            raise e

    def hset(self, name, key, value):
        try:
            r = redis.Redis(connection_pool=self.pool)
            ret = r.hset(name, key, value)
        except Exception as e:
            raise e
        return ret

    def hget(self, name, key):
        """hget函数"""
        try:
            r = redis.Redis(connection_pool=self.pool)
            value = r.hget(name, key)
            return value
        except Exception as e:
            print(str(e))
            raise e

if __name__ == '__main__':
    redis_test = RedisQuery()
    key = 'devMonitor:4FFA-48A0-47FF-122B'
    print(redis_test.get(key))
    """
    task_id = "8dde4b3f-e1e7-407c-aa48-a465ee87c53f_1"
    vul_root = "rcm:tvm:streaming:vul"
    key = ":".join([vul_root, task_id])
    value = redis_test.lrange(key, 0, -1) 
    print value
    """
    #import time
    #import datetime
    #today = datetime.date.today()
    #for index in range(0,1):
    #    prev_day = today - datetime.timedelta(days=index)
    #    timestamp = int(time.mktime(prev_day.timetuple()))
    #    tag_key = "vulsHistory:1:2:1:" + str(timestamp)
    #    data = redis_test.hgetall(tag_key)
    #    print data
    #data = redis_test.hgetall('vulsTOP:1:2:1')
    #print data

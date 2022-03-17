import random

from django_redis import get_redis_connection


def code():
    a = ''
    for x in range(4):
        a += str(random.randint(0, 9))
    return a

import redis

def get_redis():
    """
    获取 Redis 的连接
    """
    pool = get_redis_connection('default').connection_pool
    r = redis.Redis(connection_pool=pool)
    return r

import time

import redis
from redis import Redis

# from photo.utils.utils import get_redis

pool = redis.ConnectionPool(host='127.0.0.1',port=6379,db=0,)
r = Redis(pool)


while True:
    try:
        newer = r.lpop('register_list')
    except Exception as e:
        newer = None
    if newer:
        print(newer)
    else:
        r.set('a',111)
        print(r.get('a'))
        print('睡觉咯')
        time.sleep(2)

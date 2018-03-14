import random

import time


def delay(func):
    def wrapper(*args, **kwargs):
        time.sleep(random.randint(2, 5))
        return func(*args, **kwargs)

    return wrapper


local_mongo_verify = dict(
    host='127.0.0.1',
    port=27017
)

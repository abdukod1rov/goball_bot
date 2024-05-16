import time
from typing import Union

import redis
from redis.connection import ConnectionError
from redis import asyncio


async def get_redis_connection() -> Union[asyncio.Redis, None]:
    try:
        r = asyncio.Redis(host='localhost', port=6379, decode_responses=True, db=1)
    except asyncio.connection.ConnectionError as err:
        return None
    return r

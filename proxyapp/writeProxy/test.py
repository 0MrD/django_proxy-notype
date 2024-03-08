import requests
from fake_headers import Headers
import redis
from proxyapp.writeProxy.setting import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_KEY, env
redis = redis.Redis(REDIS_HOST, REDIS_PORT, REDIS_DB, decode_responses=True)


headers = Headers(headers=True).generate() #随机获取header
requests()

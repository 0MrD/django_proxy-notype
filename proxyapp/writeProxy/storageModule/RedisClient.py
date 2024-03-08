import redis
import random
from proxyapp.writeProxy.setting import REDIS_HOST,REDIS_PORT,REDIS_DB,REDIS_KEY,PROXY_SCORE_INIT,PROXY_SCORE_MAX,PROXY_SCORE_MIN

"""存储模块：对数据库中的代理进行操作"""
class RedisClient():
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB):
        self.redis_db = redis.Redis(host, port, db,decode_responses=True)   #设置decode_responses=True,输出就不会有前缀'b'了
    #随机获取ip并校验
    def get_random_proxy(self):
        #当我们网上获取到的IP保存到数据库时,分数都为最大10
        proxies = self.redis_db.zrangebyscore(REDIS_KEY,PROXY_SCORE_MAX,PROXY_SCORE_MAX)    #先随机最大分数的,确保最大分数50的都能被使用到
        if len(proxies):
            return random.choice(proxies)
        proxies = self.redis_db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MIN, PROXY_SCORE_MAX)  #随机50分以下的
        if len(proxies):
            return random.choice(proxies)
        return Exception   #以上都没有则报错
    #爬取下来的代理只是连接上限才不能使用的,而不是报错的,则分数设置为PROXY_SCORE_INIT
    def add(self, proxy_ip):
        return self.redis_db.zadd(REDIS_KEY, {proxy_ip: PROXY_SCORE_INIT})
    #代理可用,则存储到数据库并设置代理分数为最高PROXY_SCORE_MAX
    def Max(self,proxy_ip):
       return self.redis_db.zadd(REDIS_KEY,{proxy_ip:PROXY_SCORE_MAX})
    #代理不可用则降低分数,如果小于PROXY_SCORE_MIN,则删除
    def update_proxy_db(self, proxy_ip):
        score = self.redis_db.zscore(REDIS_KEY,proxy_ip)
        if score <= PROXY_SCORE_MIN:
            return self.redis_db.zrem(REDIS_KEY,proxy_ip)
        else:
            return self.redis_db.zincrby(REDIS_KEY, -1, proxy_ip)
    #获取有序集合元素个数 类似于len
    def count(self):
        return self.redis_db.zcard(REDIS_KEY)
    #列表形式返回数据库里的代理
    def all_proxy(self,start,end):
        return self.redis_db.zrangebyscore(REDIS_KEY, start, end)




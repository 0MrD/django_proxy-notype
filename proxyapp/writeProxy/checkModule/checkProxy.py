from proxyapp.writeProxy.storageModule.RedisClient import *   #导入RedisClient类里的所有,包括里面的模块等
from proxyapp.writeProxy.setting import *
from proxyapp.writeProxy.crawlersModule.getProxyRun import getProxyRun
import asyncio, aiohttp

"""检测模块：检测数据库中的代理是否可用"""
class check_proxy_ip():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.getProxyRun = getProxyRun()
        self.redisClient = RedisClient()
        self.semaphore = asyncio.Semaphore(ASYNCIO_SEMAPHORE)  #控制并发量
    #校验数据库里抓取下来的IP是否可用,然后更新
    async def check_proxy_ip(self, ip):
        url = "http://httpbin.org/get"
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                proxy = {"http": "http://" + ip,"https": "http://" + ip, }
                try:
                    async with session.get(url, proxy=proxy["http"],timeout=REQUEST_TIMEOUT, allow_redirects=False) as response:
                        await asyncio.sleep(5)
                        if response.status in TEST_VALID_STATUS:
                            self.redisClient.Max(ip)    #可用代理,则分数设置为50
                            logging.info(f"{ip} 可用,分数设置为{PROXY_SCORE_MAX}")
                        else:
                            self.redisClient.update_proxy_db(ip)   #可用代理,但可以服务器因为超出最大连接等原因,5次可能有2次失败,则分数设置为10
                            logging.info(f"{ip} 可能超时,分数将-1")
                except Exception as e:
                    self.redisClient.update_proxy_db(ip) #可能是请求超时,则分数设置为10
                    logging.error(f"{ip} 可能超出最大连接,分数将-1")
    #实现定时去爬取页面的代理：检测数据库里代理数如果小于Redis_PROXY_INIT,则再去获取代理
    def check_count(self):
        count = self.redisClient.count()
        if count < Redis_PROXY_MIN:
            logging.info(f"当前数据库代理量小于{Redis_PROXY_MIN},则再次执行代理爬取工作")
            return self.getProxyRun.run()
    def run(self):
        self.check_count()  #检测数据库中的代理数量
        proxies = self.redisClient.all_proxy(PROXY_SCORE_MIN, PROXY_SCORE_MAX)
        task_list = [self.check_proxy_ip(proxy) for proxy in proxies]    #多任务
        self.loop.run_until_complete(asyncio.wait(task_list))

"""另一种方式控制并发量
        count = self.redisClient.count()
        task_list=[]
        for i in range(0,count,20):
            start, end = i, min(i + 20, count)
            proxies = self.redisClient.get_proxy(start,end)
            task_list = [self.chek_proxy_ip(proxy) for proxy in proxies]
            self.loop.run_until_complete(asyncio.wait(task_list))"""

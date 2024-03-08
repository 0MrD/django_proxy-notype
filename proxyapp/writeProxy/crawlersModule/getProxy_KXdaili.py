import logging
from lxml import etree
from proxyapp.writeProxy.setting import REQUEST_HEADER
from proxyapp.writeProxy.storageModule.iniSaveProxyRedis import inisave_proxy_redis
import requests
#爬取KX代理网址
class crawles_KXdaili():
    def __init__(self):
        self.inisaveproxyredis = inisave_proxy_redis()
    # 去站点抓取代理IP
    def parse(self):
        header = {"User-Agent": REQUEST_HEADER}
        ips = []
        for num in range(1, 11):
            url = f"http://www.kxdaili.com/dailiip/2/{num}.html"
            response = requests.get(url=url, headers=header).text
            elemtn_tree = etree.HTML(response)
            tr_list = elemtn_tree.xpath("//table[@class='active']//tr")
            for tr in tr_list[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                ips.append(f"{ip}:{port}")
                # 使用yield,可以避免return的问题,它会直接返回值,然后记住这次执行的位置,下一次执行就从这个位置开始
                yield "%s:%s" % (ip, port) #yield返回的类型是类似列表类型的生成器对象generator
        logging.info(f"kx代理一共爬取到 {len(ips)} 个代理数")
        #return ips #使用return会等到上述循环结束才会执行,这样有一个弊端,就是循环结束后,ips列表里的数据已经很大了,这样内存消耗就会过大
    #运行
    def run(self):
        generator = self.parse()
        self.inisaveproxyredis.save_proxy_redis(generator)  #代理保存到数据库

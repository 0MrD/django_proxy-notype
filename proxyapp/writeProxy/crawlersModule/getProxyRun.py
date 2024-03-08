import logging
import multiprocessing
from proxyapp.writeProxy.crawlersModule.getProxy_KXdaili import crawles_KXdaili
from proxyapp.writeProxy.crawlersModule.getProxy_89dailai import crawles_89daili

class getProxyRun():
    def run_KXdaili(self):
        self.crawles_KXdaili = crawles_KXdaili()
        self.crawles_KXdaili.run()

    def run_89daili(self):
        self.crawles_89daili = crawles_89daili()
        self.crawles_89daili.run()
    #使用进程来并行执行
    def run(self):
        global first_process, two_process
        try:
            logging.info('爬取工作开始...')
            if True:
                logging.info(f'爬取KXdaili代理网址...')
                first_process = multiprocessing.Process(target=self.run_KXdaili())
                first_process.start()
            if True:
                logging.info(f'爬取89daili代理网址...')
                two_process = multiprocessing.Process(target=self.run_89daili())
                two_process.start()
            first_process.join()
            two_process.join()
        except KeyboardInterrupt:   #异常
            first_process.terminate()   #强制终止进程
            two_process.terminate()
        finally:
            first_process.join()
            two_process.join()
            logging.info('爬取工作结束...')
if __name__ == '__main__':
    get = getProxyRun()
    get.run()
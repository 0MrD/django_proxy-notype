from django.http import HttpResponse
from django.shortcuts import render
from proxyapp.writeProxy.setting import PROXY_SCORE_MIN, PROXY_SCORE_MAX
from proxyapp.writeProxy.storageModule import RedisClient
# Create your views here.
"""配置路由"""
def get_conn():
    return RedisClient.RedisClient()
#随机获取代理
def random(request):
    conn = get_conn()
    random_result = conn.get_random_proxy()
    return HttpResponse(random_result)   #页面返回简单的字符串
    #return render(request,"web.html",context={"random_result":random_result})   #返回H5页面
#获取代理总数
def count(request):
    conn = get_conn()
    count = conn.count()
    return HttpResponse(count)   #页面返回简单的字符串
    #return render(request,"web.html",context={"count":count})   #返回H5页面
#列表形式返回全部代理
def all_proxy(request):
    conn = get_conn()
    all_proxy = conn.all_proxy(PROXY_SCORE_MIN, PROXY_SCORE_MAX)#返回的是列表
    return render(request,"web.html",context={"all_proxy":all_proxy})

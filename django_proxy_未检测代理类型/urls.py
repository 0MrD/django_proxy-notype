"""
URL configuration for django_proxy_未检测代理类型 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import proxyapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    #即当前localhost/test地址会去匹配app01.views下的视图函数django_spider
    path('random/', proxyapp.views.random),
    path('count/', proxyapp.views.count),
    path('all_proxy/', proxyapp.views.all_proxy),

]

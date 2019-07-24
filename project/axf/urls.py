from django.urls import path
from . import views
from django.conf.urls import include
urlpatterns = [
    path(r'wxdenglu', views.home,name="home"),
    path(r'check_index',views.check_index,name="check_index"),
    path(r'index', views.index,name="index"),
    path(r'zhuce', views.zhuce,name="zhuce"),
    path(r'base', views.base,name="base"),
    path(r'wx', views.wx, name="wx"),
    path(r'mine/', views.mine, name="mine"),
    path(r'login/', views.login, name="login"),
    path(r'loginlist/', views.loginlist, name="loginlist"),
    path(r'minelist/', views.minelist, name="minelist"),
    path(r'weixiulist/', views.weixiulist, name="weixiulist"),
    # path(r'jiaofei1/', views.jiaofei1, name="jiaofei1"),
    path(r'jiaofei2/', views.jiaofei2, name="jiaofei2"),
    path(r'jiaofei3/', views.jiaofei3, name="jiaofei3"),
    path(r'jiaofei4/', views.jiaofei4, name="jiaofei4"),
    path(r'tijiao/', views.tijiao, name="tijiao"),
    path(r'quit/', views.quit, name="quit"),
    path(r'regist/',views.regist,name="regist"),
    path(r'xinwenlist/', views.xinwenlist, name="xinwenlist"),
    path(r'msglist/', views.msglist, name="msglist"),
    path(r'typelist/', views.typelist, name="typelist"),
    path(r'typelist1/', views.typelist1, name="typelist1"),
    path(r'quit/', views.quit, name="quit"),
    path(r'search/', views.search, name="search"),
    path(r'',views.index,name="index")
]
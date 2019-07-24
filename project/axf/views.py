from django.shortcuts import render
from django.http import HttpResponse
from . import models
import json
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.utils import *
from .models import yonghu,yongliang,weihu,feiyong,weixiudan,xinwen
from django.views.decorators.csrf import csrf_exempt
import time
import random
# from django.conf import settings
# from django.db.models import Q
import os
from django.http import HttpResponseRedirect
# Create your views here.


def home(request):
    return render(request,'login.html')
def check_index(request):
    username=request.POST.get("Username")
    print(username)
    password=request.POST.get("Password")
    if models.yuangong.objects.filter(id=username,password=password):
        request.session["username"] = username
        request.session['type']=0
        return HttpResponseRedirect('/wx')
    else:
        return render(request, 'login.html',{"error":"用户名密码不正确"})
def index(request):
   # request.session['type']=""

    if request.session['type']!=0 and request.session['type']!=1:
        request.session['type'] = ""
    xinwenlist1 = xinwen.objects.all()[:5]
    xinwenlist2 = xinwen.objects.all()[5:10]
    xinwenlist3 = xinwen.objects.all()[10:15]
    xinwenlist31=xinwen.objects.filter(xinwen_leixing=0)
    return render(request,'index.html',{"xinwen1":xinwenlist1,"xinwen2":xinwenlist2,"xinwen3":xinwenlist31,})
def base(request):
    return render(request, 'base.html')
def zhuce(request):
    return render(request,'zhuce.html')
def wx(request):
    username=request.session['username']
    data=models.yuangong.objects.get(id=username)
    print(username)
    print("zheshiyigeyuanggong*****")
    #个人信息界面
    result=[]
    history=models.weihu.objects.filter(yuangong_id_id=username).values("weihu_id","time","money","zhuangtai","weixiudan_id_id")
    for i in range(0,len(history)):
        z=models.weixiudan.objects.filter(id=history[i]["weixiudan_id_id"]).values("weixiu_stime","yonghu_home","yonghu_id_id")
        y = models.yonghu.objects.filter(id=z[0]["yonghu_id_id"]).values("name")
        if history[i]["zhuangtai"]==True:
            zhuangtai="已维修"
        else:
            zhuangtai="未维修"
        result.append([history[i]["weihu_id"],y[0]["name"],z[0]["weixiu_stime"],z[0]["yonghu_home"],history[i]["money"],zhuangtai])
    #有新任务显示
    if models.weihu.objects.filter(yuangong_id_id=username, stl=0):
        newdata = models.weihu.objects.get(yuangong_id_id=username, stl=0)
        print (newdata)
        # yhdata = models.yonghu.objects.get(id=newdata.yonghu_id_id)
        newz = models.weixiudan.objects.get(id=newdata.weixiudan_id_id)
        newy= models.yonghu.objects.get(id=newz.yonghu_id_id)
        message = 1
        wx_money = request.POST.get("wx_money")
        wx_news = request.POST.get("wx_statment")
        if(wx_money):
            newdata.money =wx_money
            newdata.news=wx_news
            newdata.stl=1
            time_now = timezone.now()
            time_now.strftime("%Y-%m-%d")
            newdata.timepy = time_now
            newdata.save()
            data.zhuangtai = 0
            data.save()
            message = "暂无任务"

            #刷新后
            result.clear()
            history = models.weihu.objects.filter(yuangong_id_id=username).values("weihu_id", "time", "money",
                                                                                  "zhuangtai", "weixiudan_id_id","stl")
            for i in range(0, len(history)):
                z = models.weixiudan.objects.filter(id=history[i]["weixiudan_id_id"]).values("weixiu_stime",
                                                                                             "yonghu_home",
                                                                                             "yonghu_id_id")
                y = models.yonghu.objects.filter(id=z[0]["yonghu_id_id"]).values("name")
                if history[i]["stl"] == 1:
                    zhuangtai = "已维修"
                else:
                    zhuangtai = "未完成维修"
                result.append([history[i]["weihu_id"], y[0]["name"], z[0]["weixiu_stime"], z[0]["yonghu_home"],
                               history[i]["money"], zhuangtai])
        print (message)
        return render(request, 'wx.html', {"id": data.id, "name": data.name, "money": data.money, "tele": data.tele,
                                               "yonghu_name": newy.name,"wx_id": newdata.weihu_id, "wx_news": newdata.news,
                                           "yonghu_tele": newz.yonghu_tel,"yonghu_live":newz.yonghu_home,"message":message,"wxlist":result,"username":username})
    else:
        message="暂无任务"
        return render(request, 'wx.html', {"id": data.id, "name": data.name, "money": data.money, "tele": data.tele,
                                            "message":message,"wxlist":result,"username":username})
def mine(request):
    userID = request.session['Id']
    print(userID)
    user = yonghu.objects.get(id = userID)
    print(user)
    usery = yongliang.objects.filter(yonghu_id_id = userID)
    print(usery)
    print(usery.count())
    if(usery.count()==0):
        error="未正常显示"
    else:
        error="正常显示"
        twouser = usery.get(yongliang_type=1)
        threeuser = usery.get(yongliang_type=2)
        fouruser = usery.get(yongliang_type=3)
        print(fouruser)
    print("下一句错了")
    userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
    print(userx2)
    userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
    print(userx3)
    userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
    print(userx4)
    weixiulist = []
    weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
    length = len(weixiulist)
    feiyonglist = []
    feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
    if length!=0:
        return render(request, 'myapp/mine.html', {"title": "我的", "name": user.name, "category": user.type, "balance": user.money, "tel": user.tele, "home": user.live,
                               "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                                "userx2": userx2, "userx3": userx3, "userx4": userx4,
                               "weixiuj":weixiulist[0],"weihu":weixiulist,"feiyong":feiyonglist})
    else:
        errorw="没有未缴纳的维修费用"
        return render(request, 'myapp/mine.html',
                      {"title": "我的", "name": user.name, "category": user.type, "balance": user.money, "tel": user.tele,"home": user.live,
                        "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                        "userx2": userx2, "userx3": userx3, "userx4": userx4, "error1":error,
                       "errorw":errorw,"feiyong":feiyonglist,"length":length})
def login(request):
    return render(request, 'login2.html', {"title":"登录"})
from django.http import HttpResponse
def loginlist(request):
    name = request.POST.get('username')
    word = request.POST.get('password')
    print(name)
    print(word)
    try:
        user = yonghu.objects.get(name = name)
        if user.password != word:
            return render(request, 'login2.html', {"title": "登录","error":"密码错误"})
    except yonghu.DoesNotExist as e:
        return render(request, 'login2.html', {"title": "登录", "error": "用户不存在"})
    request.session["Id"] = user.id
    request.session['type'] = 1
    return redirect('/mine/')
import string
from django.http import HttpResponse
def minelist(request):
    #充值
    name = request.POST.get('cz')
    userID = request.session['Id']
    user = yonghu.objects.get(id = userID)
    ts1 = int(name)
    ts2 = int(user.money)
    ts3 = ts1 + ts2
    user.money = str(ts3)
    user.save()
    user = yonghu.objects.get(id=userID)
    mg = "充值成功"
    usery = yongliang.objects.filter(yonghu_id_id=userID)
    if (usery.count() == 0):
        error = "未正常显示"
    else:
        error = "正常显示"
        twouser = usery.get(yongliang_type=1)
        threeuser = usery.get(yongliang_type=2)
        fouruser = usery.get(yongliang_type=3)
    userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
    userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
    userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
    weixiulist = []
    weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
    length = len(weixiulist)
    feiyonglist = []
    feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
    if length != 0:
        return render(request, 'myapp/mine.html',
                     {"title": "我的", "name": user.name, "category": user.type, "balance": user.money, "tel": user.tele,"home": user.live,"mg":mg,
                        "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                         "userx2": userx2, "userx3": userx3, "userx4": userx4,
                        "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"length":length})
    else:
        errorw = "没有未缴纳的维修费用"
        return render(request, 'myapp/mine.html',
                    {"title": "我的", "name": user.name, "category": user.type, "balance": user.money, "tel": user.tele,"home": user.live,"mg":mg,
                        "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                         "userx2": userx2, "userx3": userx3, "userx4": userx4, "error1": error,
                        "errorw": errorw, "feiyong": feiyonglist,"length":length})
def jiaofei2(request):
    userID = request.session['Id']
    user = yonghu.objects.get(id=userID)
    usery = yongliang.objects.filter(yonghu_id_id=userID)
    if (usery.count() == 0):
        error = "未正常显示"
    else:
        error = "正常显示"
        twouser = usery.get(yongliang_type=1)
        threeuser = usery.get(yongliang_type=2)
        fouruser = usery.get(yongliang_type=3)
    userx1 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
    x = int(user.money)
    y = int(userx1.feiyong_qian)
    if (x < y):
        errorj = "余额不足"
        userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
        userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
        userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
        weixiulist = []
        weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
        length = len(weixiulist)
        feiyonglist = []
        feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
        if length != 0:
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"length":length})
        else:
            errorw = "没有未缴纳的维修费用"
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                           "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                           "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "errorw": errorw, "feiyong": feiyonglist,"length":length})
    else:
        errorj = "缴费成功"
        user.money = str(x - y)
        user.save()
        time_now = timezone.now()
        time_now.strftime("%Y-%m-%d")
        userx1.feiyong_jieshu = time_now
        userx1.feiyong_zhuangtai = 1
        userx1.save()
        feiyong.objects.create(yonghu_id=userx1.yonghu_id, feiyong_kaishi=time_now, feiyong_jieshu=time_now,
                               feiyong_qian=0,
                               feiyong_zhuangtai=0, feiyong_leixing=userx1.feiyong_leixing,feiyong_company=userx1.feiyong_company)
        userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
        userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
        userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
        weixiulist = []
        weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
        length = len(weixiulist)
        feiyonglist = []
        feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
        if length != 0:
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                           "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"length":length})
        else:
            errorw = "没有未缴纳的维修费用"
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "errorw": errorw, "feiyong": feiyonglist,"length":length})
def jiaofei3(request):
    userID = request.session['Id']
    user = yonghu.objects.get(id=userID)
    usery = yongliang.objects.filter(yonghu_id_id=userID)
    if (usery.count() == 0):
        error = "未正常显示"
    else:
        error = "正常显示"
        twouser = usery.get(yongliang_type=1)
        threeuser = usery.get(yongliang_type=2)
        fouruser = usery.get(yongliang_type=3)
    userx1 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
    # 缴费
    x = int(user.money)
    y = int(userx1.feiyong_qian)
    if (x < y):
        errorj = "余额不足"
        userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
        userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
        userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
        weixiulist = []
        weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
        length = len(weixiulist)
        feiyonglist = []
        feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
        if length != 0:
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"length":length})
        else:
            errorw = "没有未缴纳的维修费用"
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                           "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "errorw": errorw, "feiyong": feiyonglist,"length":length})
    else:
        errorj = "缴费成功"
        user.money = str(x - y)
        user.save()
        time_now = timezone.now()
        time_now.strftime("%Y-%m-%d")
        userx1.feiyong_jieshu = time_now
        userx1.feiyong_zhuangtai = 1
        userx1.save()
        feiyong.objects.create(yonghu_id=userx1.yonghu_id, feiyong_kaishi=time_now, feiyong_jieshu=time_now,
                               feiyong_qian=0,
                               feiyong_zhuangtai=0, feiyong_leixing=userx1.feiyong_leixing,feiyong_company=userx1.feiyong_company)
        userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
        userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
        userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
        weixiulist = []
        weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
        length = len(weixiulist)
        feiyonglist = []
        feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
        if length != 0:
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"length":length})
        else:
            errorw = "没有未缴纳的维修费用"
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                           "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                           "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "errorw": errorw, "feiyong": feiyonglist,"length":length})
def jiaofei4(request):
    userID = request.session['Id']
    user = yonghu.objects.get(id=userID)
    usery = yongliang.objects.filter(yonghu_id_id=userID)
    if (usery.count() == 0):
        error = "未正常显示"
    else:
        error = "正常显示"
        twouser = usery.get(yongliang_type=1)
        threeuser = usery.get(yongliang_type=2)
        fouruser = usery.get(yongliang_type=3)
    userx1 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
    x = int(user.money)
    y = int(userx1.feiyong_qian)
    if (x<y):
        errorj="余额不足"
        userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
        userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
        userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
        weixiulist = []
        weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
        length = len(weixiulist)
        feiyonglist = []
        feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
        if length != 0:
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                           "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"length":length})
        else:
            errorw = "没有未缴纳的维修费用"
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "errorw": errorw, "feiyong": feiyonglist,"length":length})
    else:
        errorj="缴费成功"
        user.money = str(x-y)
        user.save()
        time_now = timezone.now()
        time_now.strftime("%Y-%m-%d")
        userx1.feiyong_jieshu = time_now
        userx1.feiyong_zhuangtai = 1
        userx1.save()
        feiyong.objects.create(yonghu_id=userx1.yonghu_id, feiyong_kaishi=time_now, feiyong_jieshu=time_now,
                               feiyong_qian=0,
                               feiyong_zhuangtai=0, feiyong_leixing=userx1.feiyong_leixing,feiyong_company=userx1.feiyong_company)
        userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
        userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
        userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
        weixiulist = []
        weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
        length = len(weixiulist)
        feiyonglist = []
        feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
        if length != 0:
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                           "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"length":length})
        else:
            errorw = "没有未缴纳的维修费用"
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                           "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4, "errorj": errorj,
                           "errorw": errorw, "feiyong": feiyonglist,"length":length})
def weixiulist(request):
    userID = request.session['Id']
    user = yonghu.objects.get(id=userID)
    usery = yongliang.objects.filter(yonghu_id_id=userID)
    print("xxxxxxxxxxxxxxxxxxxxxx")
    if (usery.count() == 0):
        error = "未正常显示"
    else:
        error = "正常显示"
        twouser = usery.get(yongliang_type=1)
        threeuser = usery.get(yongliang_type=2)
        fouruser = usery.get(yongliang_type=3)
    userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
    userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
    userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
    weixiulist1 = []
    weixiulist1 = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
    weixiulist2 = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
    weixiu = weixiulist2.get(weihu_id=weixiulist1[0].weihu_id)
    x = int(user.money)
    y = int(weixiu.money)
    print(x)
    print(y)
    if (x>=y):
        errorjf="缴费成功"
        user.money=str(x-y)
        user.save()
        time_now = timezone.now()
        time_now.strftime("%Y-%m-%d")
        weixiu.time = time_now
        weixiu.zhuangtai = 1
        print(weixiu.time)
        print(weixiu.zhuangtai)
        weixiu.save()
        weixiulist = []
        weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
        length=len(weixiulist)
        feiyonglist = []
        feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
        if length!=0:
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money, "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser,"error": error,
                           "userx2": userx2, "userx3": userx3, "userx4": userx4,
                           "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"errorfj":errorjf,"length":length})
        else:
            errorw = "没有未缴纳的维修费用"
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money, "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4,
                           "errorw":errorw, "feiyong": feiyonglist,"errorfj":errorjf,"length":length})
    else:
        errorjf = "余额不足"
        weixiulist = []
        weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
        length = len(weixiulist)
        feiyonglist = []
        feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
        if length != 0:
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                           "userx2": userx2, "userx3": userx3, "userx4": userx4,
                           "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"errorfj":errorjf,"length":length})
        else:
            errorw="没有未缴纳的维修费用"
            return render(request, 'myapp/mine.html',
                          {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,
                           "tel": user.tele, "home": user.live,
                            "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                            "userx2": userx2, "userx3": userx3, "userx4": userx4,
                           "errorw":errorw, "feiyong": feiyonglist,"errorfj":errorjf,"length":length})
def tijiao(request):
    userID = request.session['Id']
    user = yonghu.objects.get(id=userID)
    news = request.POST.get('ns')
    print("********************")
    print(news)
    time_now = timezone.now()
    time_now.strftime("%Y-%m-%d")
    weixiudan.objects.create(yonghu_leibie=user.type,weixiu_stime=time_now,yonghu_tel=user.tele,yonghu_home=user.live,weixiu_news=news,weixiu_zhuangtai=0,yonghu_id_id=user.id)
    usery = yongliang.objects.filter(yonghu_id_id=userID)
    if (usery.count() == 0):
        error = "未正常显示"
    else:
        error = "正常显示"
        twouser = usery.get(yongliang_type=1)
        threeuser = usery.get(yongliang_type=2)
        fouruser = usery.get(yongliang_type=3)
    userx2 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=1)
    userx3 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=2)
    userx4 = feiyong.objects.get(yonghu_id=userID, feiyong_zhuangtai=0, feiyong_leixing=3)
    msg="提交成功"
    weixiulist = []
    weixiulist = weihu.objects.filter(yonghu_id=userID, zhuangtai=0,stl=1)
    length = len(weixiulist)
    feiyonglist = []
    feiyonglist = feiyong.objects.filter(yonghu_id=userID, feiyong_zhuangtai=0)
    if length != 0:
        return render(request, 'myapp/mine.html',
                      {"title": "我的", "name": user.name, "category": user.type, "balance": user.money, "tel": user.tele,"msg":msg,
                       "home": user.live,
                        "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                        "userx2": userx2, "userx3": userx3, "userx4": userx4,
                       "weixiuj": weixiulist[0], "weihu": weixiulist, "feiyong": feiyonglist,"length":length})
    else:
        errorw = "没有未缴纳的维修费用"
        return render(request, 'myapp/mine.html',
                      {"title": "我的", "name": user.name, "category": user.type, "balance": user.money,"msg":msg,
                       "tel": user.tele, "home": user.live,
                        "user1": twouser, "user2": threeuser, "user3": fouruser, "error": error,
                        "userx2": userx2, "userx3": userx3, "userx4": userx4,
                       "errorw": errorw, "feiyong": feiyonglist,"length":length})
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('myapp/mine.html')
def regist(request):
    #a = requanst.POST.get('name')
    name = request.POST.get('firstname')
    type = request.POST.get('type')
    password = request.POST.get('pwd')
    money = "0"
    tele = request.POST.get('sjname')
    live = request.POST.get('xxdz')
    print("*******************************")
    yonghulist=yonghu.objects.all()
    for i in yonghulist:
        if i.name==name:
            return render(request,'zhuce.html',{"msg":"该用户已存在"})
    yonghu.objects.create(name=name,type=type,password=password,money=money,tele=tele,live=live,delt=0)
    yh = yonghu.objects.get(name=name)
    print(yh.id)
    time_now = timezone.now()
    time_now.strftime("%Y-%m-%d")
    feiyong.objects.create(yonghu_id=yh.id,feiyong_kaishi=time_now,feiyong_jieshu=time_now,feiyong_leixing=1,feiyong_qian=0,feiyong_zhuangtai=0,feiyong_company='黑龙江省电力公司')
    feiyong.objects.create(yonghu_id=yh.id,feiyong_kaishi=time_now,feiyong_jieshu=time_now,feiyong_leixing=2,feiyong_qian=0,feiyong_zhuangtai=0,feiyong_company='黑龙江省水力公司')
    feiyong.objects.create(yonghu_id=yh.id,feiyong_kaishi=time_now,feiyong_jieshu=time_now,feiyong_leixing=3,feiyong_qian=0,feiyong_zhuangtai=0,feiyong_company='黑龙江省煤气公司')
    yongliang.objects.create(yongliang_type=1,yongliang_jichumany=0,yongliang_many=0,yonghu_id_id=yh.id)
    yongliang.objects.create(yongliang_type=2,yongliang_jichumany=0,yongliang_many=0,yonghu_id_id=yh.id)
    yongliang.objects.create(yongliang_type=3,yongliang_jichumany=0,yongliang_many=0,yonghu_id_id=yh.id)
    # return render(request,'index.html')
    return HttpResponseRedirect('/index')

def xinwenlist(request):
    ss = request.GET.get('p1',' ')
    print(ss)
    nes = xinwen.objects.get(xinwen_biaoti = ss)
    return render(request,'myapp/xinwenlist.html',{"new":nes})

def msglist(request):
     print("***************")
     ss=request.session['Id']
     print(ss)
     if  request.session['type']!=1:
         return render(request,'login2.html',)
     else :
         return HttpResponseRedirect('/mine/')
def typelist(request):
    ss=request.session['type']
    if ss==1:
        # return render(request, 'myapp/mine.html')
        return HttpResponseRedirect('/mine/')
    else :
        return render(request, 'login2.html')

def typelist1(request):
    ss=request.session['type']
    print(ss)
    if ss==0:
        return HttpResponseRedirect('/wx')
    else :
        return render(request, 'login.html')

def quit(request):
    request.session['type']=""
    # 2. 重定向到 登录界面
    return HttpResponseRedirect('/index')

import re
def search(request):
    print("******************")
    ns = request.POST.get('soshuo')
    print(ns)
    nes = xinwen.objects.all()
    list=[]
    pattern = '.*'.join(ns)
    regex = re.compile(pattern)
    for i in nes:
        match = regex.search(i.xinwen_biaoti)
        if match:
            list.append(i)
    return render(request,'myapp/search.html',{"list":list})
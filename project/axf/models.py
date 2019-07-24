from django.db import models

# Create your models here.
class yonghu(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    money = models.CharField(max_length=10)
    tele = models.CharField(max_length=12)
    live = models.CharField(max_length=50)
    delt = models.BooleanField()

class feiyong(models.Model):
    yonghu_id = models.IntegerField()#用户号
    feiyong_danhaoid = models.IntegerField(primary_key=True)#单号
    feiyong_kaishi = models.DateField()#开始时间
    feiyong_jieshu = models.DateField()#结束时间
    feiyong_leixing = models.IntegerField()#用电量用水量等，网费为0
    feiyong_qian = models.CharField(max_length=20)#清单费用
    feiyong_zhuangtai = models.BooleanField()#缴费状态
    feiyong_company = models.CharField(max_length=20)

class yuangong(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    money = models.CharField(max_length=20)
    tele = models.CharField(max_length=12)
    zhuangtai=models.BooleanField()
    delt = models.BooleanField()

class weihu(models.Model):
    weihu_id = models.IntegerField(primary_key=True)
    yonghu_id = models.IntegerField()
    yuangong_id = models.IntegerField()
    time = models.DateField()
    money = models.CharField(max_length=20,null=True)
    zhuangtai = models.BooleanField()
    news = models.CharField(max_length=100)
    stl = models.BooleanField()
    weixiudan_id = models.ForeignKey("weixiudan",on_delete=models.CASCADE)
    yuangong_id = models.ForeignKey("yuangong",on_delete=models.CASCADE)

class jiage(models.Model):
    jiage_leixing=models.IntegerField()
    jiage_diyibz=models.CharField(max_length=20)#第一标准价格
    jiage_tidudaxiao=models.CharField(max_length=20)
    jiage_xishu=models.CharField(max_length=20)#梯度系数
    jiage_fengdingtd=models.IntegerField()#封顶梯度

class yongliang(models.Model):
    yonghu_id = models.IntegerField(primary_key=True)
    yongliang_type = models.IntegerField()
    yongliang_jichumany = models.IntegerField()#上个月用量
    yongliang_many = models.IntegerField()#这个月的用量
    yonghu_id = models.ForeignKey("yonghu", on_delete=models.CASCADE)

class weixiudan(models.Model):
    yonghu_id = models.IntegerField()
    yonghu_leibie = models.CharField(max_length=20)
    weixiu_stime = models.DateField()
    yonghu_tel= models.CharField(max_length=12)
    yonghu_home=models.CharField(max_length=50)
    weixiu_news=models.CharField(max_length=100)
    weixiu_zhuangtai=models.BooleanField()
    yonghu_id = models.ForeignKey("yonghu", on_delete=models.CASCADE)

class xinwen(models.Model):
    xinwen_id = models.IntegerField()
    xinwen_biaoti = models.CharField(max_length=20)
    xinwen_neirong = models.TextField(max_length = 300)
    xinwen_leixing=models.IntegerField()
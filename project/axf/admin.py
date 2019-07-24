from django.contrib import admin

# Register your models here.
from  .models import feiyong,yonghu,yuangong,weihu,xinwen,jiage
class yonghu_admin(admin.ModelAdmin):
    list_display=['name','type','password','money','tele','live','delt']
    list_filter=['name','type']
    searche_fields=['name','type']
admin.site.register(yonghu,yonghu_admin)
class  yuangong_admin(admin.ModelAdmin):
    list_display = ['name','password','money','tele','zhuangtai','delt']
admin.site.register(yuangong,yuangong_admin)
class feiyong_admin(admin.ModelAdmin):
    list_display=['yonghu_id','feiyong_danhaoid','feiyong_kaishi','feiyong_jieshu','feiyong_leixing','feiyong_qian','feiyong_zhuangtai','feiyong_company']
admin.site.register(feiyong,feiyong_admin)
class weihu_admin(admin.ModelAdmin):
    list_display = ['weihu_id','yonghu_id','time','money','zhuangtai','news','stl','weixiudan_id','yuangong_id']
admin.site.register(weihu,weihu_admin)
class xinwen_admin(admin.ModelAdmin):
    list_display = ['xinwen_id','xinwen_biaoti']
admin.site.register(xinwen,xinwen_admin)
class jiage_admin(admin.ModelAdmin):
    list_display = ['jiage_leixing','jiage_diyibz','jiage_tidudaxiao','jiage_xishu','jiage_fengdingtd']
admin.site.register(jiage,jiage_admin)
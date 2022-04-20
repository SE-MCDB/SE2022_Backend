from django.db import models

class Expert(models.Model):
    #知兔平台唯一的学者号
    scholarID = models.CharField(max_length=20, blank=True, null=True)
    #学者姓名
    name = models.CharField(max_length=10, blank=True, null=True)
    #学者身份证号,管理端添加
    ID_num = models.CharField(max_length=20, blank=True, null=True)
    #工作单位
    organization = models.CharField(max_length=20, blank=True, null=True)
    #擅长领域
    field = models.CharField(max_length=20, blank=True, null=True)
    #自我介绍
    self_profile = models.CharField(max_length=200, blank=True, null=True)
    #身份证照片
    ID_pic = models.ImageField(upload_to="images/%Y%m/%d/icons",
                                         default='images/default_user_icon.jpg')
    #学者官网
    url = models.CharField(max_length=60, blank=True, null=True)
    #学者电话
    phone = models.CharField(max_length=15, blank=True, null=True)

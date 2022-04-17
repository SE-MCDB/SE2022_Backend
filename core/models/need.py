from django.db import models
from .user import User

NEED_FIELD_CHOICES = (
    (0, '信息技术'),
    (1, '装备制造'),
    (2, '新材料'),
    (3, '新能源'),
    (4, '节能环保'),
    (5, '生物医药'),
    (6, '科学创意'),
    (7, '检验检测'),
    (8, '其他')
)

NEED_STATE = (
    (0, '进行中'),
    (1, '已结束')
)

EMERGENCY_CODE = (
    (0, '低'),
    (1, '中'),
    (2, '高')
)


class Need(models.Model):
    #需求标题
    title = models.CharField(max_length=20)
    #需求描述
    description = models.TextField()
    #预计经费（报酬）
    money = models.IntegerField()
    #需求创建时间，自动填充
    start_time = models.DateTimeField(auto_now_add=True)
    #有效时间（预计结束时间）
    valid_time = models.DateTimeField(blank=True, null=True)
    #关键字
    key_word = models.CharField(max_length=10)
    #技术领域
    field = models.IntegerField(choices=NEED_FIELD_CHOICES, default=8)
    #地址
    address = models.CharField(max_length=20)
    #需求公司
    enterprise = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enterprise")
    #订单状态
    state = models.IntegerField(choices=NEED_STATE, default=0)
    #紧急程度
    emergency = models.IntegerField(choices=EMERGENCY_CODE, default=0)
    #预计招募人数
    predict = models.IntegerField()
    #实际已招募人数
    real = models.IntegerField(default=0)
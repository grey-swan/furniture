import time
import datetime

from rest_framework import serializers


now = datetime.datetime.now


class MyDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value['$date'] / 1000))
        return super(MyDateTimeField, self).to_representation(value)


class MyBaseSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def save(self, **kwargs):
        return self.instance


class CategorySerializer(MyBaseSerializer):
    """分类，如桌子，椅子等"""

    _id = serializers.CharField(max_length=64, required=False)
    title = serializers.CharField(max_length=16)
    type = serializers.CharField(max_length=1)  # 0:普通物品  1:配件物品


class StyleSerializer(MyBaseSerializer):
    """风格，如北欧，现代简约等"""

    _id = serializers.CharField(max_length=64, required=False)
    title = serializers.CharField(max_length=16)


class FurnitureSerializer(MyBaseSerializer):
    """家具和饰品"""

    _id = serializers.CharField(max_length=64, required=False)
    title = serializers.CharField(max_length=64)  # 标题
    subtitle = serializers.CharField(max_length=128, allow_blank=True)  # 副标题
    img = serializers.ListField(max_length=7, required=False)  # 轮播图片
    price = serializers.IntegerField(required=False)  # 价格
    content = serializers.CharField(max_length=51200)  # 内容
    updated = serializers.CharField(max_length=19, required=False)
    created = serializers.CharField(max_length=19, required=False, default=now().strftime('%Y-%m-%d %H:%M:%S'))
    category_id = serializers.CharField(max_length=64)  # 分类
    style_id = serializers.ListField(max_length=16, required=False)  # 风格


class CaseSerializer(MyBaseSerializer):
    """案例"""

    _id = serializers.CharField(max_length=64, required=False)
    title = serializers.CharField(max_length=64)  # 标题
    subtitle = serializers.CharField(max_length=128, allow_blank=True)  # 副标题
    img = serializers.ListField(max_length=1, required=False)  # 轮播图片
    building = serializers.CharField(max_length=32)  # 楼盘
    area = serializers.CharField(max_length=32)  # 面积
    content = serializers.CharField(max_length=51200)  # 内容
    updated = serializers.CharField(max_length=19, required=False)
    created = serializers.CharField(max_length=19, required=False, default=now().strftime('%Y-%m-%d %H:%M:%S'))
    style_id = serializers.CharField(max_length=32, required=False)  # 风格


class SoftSerializer(MyBaseSerializer):
    """全屋软装搭配"""

    _id = serializers.CharField(max_length=64, required=False)
    content = serializers.CharField(max_length=51200)  # 内容
    updated = serializers.CharField(max_length=19, required=False)
    created = serializers.CharField(max_length=19, required=False, default=now().strftime('%Y-%m-%d %H:%M:%S'))


class DesignerSerializer(MyBaseSerializer):
    """设计师"""

    _id = serializers.CharField(max_length=64, required=False)
    title = serializers.CharField(max_length=16)
    avatar = serializers.URLField()
    position = serializers.CharField(max_length=16)
    desc = serializers.CharField(max_length=51200)


class CompanySerializer(MyBaseSerializer):
    """公司介绍"""

    _id = serializers.CharField(max_length=64, required=False)
    content = serializers.CharField(max_length=51200)  # 内容
    updated = serializers.CharField(max_length=19, required=False)
    created = serializers.CharField(max_length=19, required=False, default=now().strftime('%Y-%m-%d %H:%M:%S'))


class BannerSerializer(MyBaseSerializer):
    """广告位"""

    position_list = ((0, '第一广告位'), (1, '第二广告位'))
    link_list = ((0, '列表页'), (1, '详情页'), (2, '静态页'))
    type_list = ((0, '家具'), (1, '案例'), (2, '设计师'))

    _id = serializers.CharField(max_length=64, required=False)
    cover = serializers.URLField()  # 广告展示图
    sort_order = serializers.IntegerField()  # 排序
    position = serializers.ChoiceField(choices=position_list)  # 位置
    type = serializers.ChoiceField(choices=type_list, required=False, allow_blank=True)  # 类别
    link_type = serializers.ChoiceField(choices=link_list, required=False, allow_blank=True)  # 链接类型

    product_id = serializers.CharField(max_length=64, required=False, allow_blank=True)  # 关联的对象，可以为家具和案例的ID
    product_title = serializers.CharField(max_length=64, required=False, allow_blank=True)  # 产品名称

    style_id = serializers.CharField(max_length=64, required=False, allow_blank=True)  # 关联的风格对象
    style_title = serializers.CharField(max_length=64, required=False, allow_blank=True)  # 风格名称


class OrderSerializer(MyBaseSerializer):
    """订单"""

    status_list = ((0, '未处理'), (1, '已处理'), (2, '已取消'))
    type_list = ((0, '全屋软装搭配-设计'), (1, '获取报价-家具'), (2, '我想这样搭-案例'), (3, '预约设计师-设计师'))

    order_id = serializers.CharField(max_length=64)  # 订单id
    status = serializers.ChoiceField(choices=status_list)  # 订单状态
    types = serializers.ChoiceField(choices=type_list)  # 订单类型

    name = serializers.CharField(max_length=16)  # 用户姓名
    phone = serializers.CharField(max_length=32)  # 用户电话
    address = serializers.CharField(max_length=64)  # 用户地址
    style = serializers.CharField(max_length=64, required=False)  # 风格

    user_id = serializers.CharField(max_length=64)  # 用户id
    updated = serializers.CharField(max_length=19)  # 更新时间
    created = serializers.CharField(max_length=19)  # 更新时间

    # 家具、案例、设计师和软装共用id，格式如下：
    # [{product_id: '', style_id: '', img: '', title: '', price: ''}]
    products = serializers.ListField()

from django.db import models
from django.contrib.auth.models import User


# class Category(models.Model):
#     """商品分类"""
#
#     name = models.CharField(max_length=32, verbose_name='名称')
#     alias = models.CharField(max_length=32, verbose_name='别名')
#
#     def __str__(self):
#         return self.name
#
#
# class Product(models.Model):
#     """商品"""
#
#     title = models.CharField(max_length=64, verbose_name='标题')
#     subtitle = models.CharField(max_length=128, verbose_name='副标题')
#     price = models.IntegerField(verbose_name='价格')
#     content = models.TextField(verbose_name='详情')
#     updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
#     created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product', verbose_name='分类')
#     user = models.ForeignKey(User, related_name='product', on_delete=models.CASCADE, verbose_name='创建人')
#
#     def __str__(self):
#         return self.title
#
#
# class Case(models.Model):
#     """案例"""
#
#     title = models.CharField(max_length=64, verbose_name='标题')
#     subtitle = models.CharField(max_length=128, verbose_name='副标题')
#     price = models.IntegerField(verbose_name='价格')
#     content = models.TextField(verbose_name='详情')
#     updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
#     created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#
#     user = models.ForeignKey(User, related_name='case', on_delete=models.CASCADE, verbose_name='创建人')
#
#     def __str__(self):
#         return self.title
#
#
# class Dw(models.Model):
#     """全屋软装搭配"""
#
#
# class Designer(models.Model):
#     """设计师"""
#
#     name = models.CharField(max_length=32, verbose_name='姓名')
#     position = models.CharField(max_length=16, verbose_name='职称')
#     avatar = models.URLField(verbose_name='头像')
#     desc = models.TextField(verbose_name='个人简介')
#
#
# class Banner(models.Model):
#     """轮播列表"""
#
#     # type_list = ((0, '首页轮播1'), (1, '首页轮播2'), (2, '商品轮播'))
#
#     title = models.CharField(max_length=64, verbose_name='标题')
#     url = models.URLField(verbose_name='图片地址')
#     sort_order = models.IntegerField(verbose_name='排序')
#     # types = models.IntegerField(verbose_name='类型', choices=type_list)
#
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='banner',
#                                 verbose_name='商品')
#
#
# class Cart(models.Model):
#     """搭配间-只针对product"""
#
#     product = models.ForeignKey(Product, related_name='cart', on_delete=models.CASCADE, verbose_name='所选商品')
#     user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE, verbose_name='创建人')
#
#
# class Order(models.Model):
#     """订单"""
#
#     status_list = ((0, '未付款'), (1, '已完成'), (2, '已取消'))
#     type_list = ((0, '全屋软装搭配-设计'), (1, '获取报价-家具'), (2, '我想这样搭-案例'), (3, '预约设计师-设计师'))
#
#     order_id = models.IntegerField(verbose_name='订单号')
#     status = models.IntegerField(verbose_name='订单状态', choices=status_list)
#     types = models.IntegerField(verbose_name='类型', choices=type_list)
#
#     name = models.CharField(max_length=16, verbose_name='客户姓名')
#     address = models.CharField(max_length=64, verbose_name='收货地址')
#     phone = models.CharField(max_length=16, verbose_name='联系电话')
#     community = models.CharField(max_length=64, verbose_name='小区', null=True, blank=True)
#
#     updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')
#     created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order', verbose_name='创建人')
#
#
# class OrderProduct(models.Model):
#     """家具订单详情"""
#
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='order_product',
#                                  verbose_name='商品分类')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product',
#                                 verbose_name='所选商品')
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_product',
#                               verbose_name='所属订单')
#
#
# class OrderCase(models.Model):
#     """案例订单详情"""
#
#     case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='order_case',
#                              verbose_name='所选案例')
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_case',
#                               verbose_name='所属订单')
#
#
# class OrderDesigner(models.Model):
#     """用户选择的设计师订单详情"""
#
#     designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name='order_designer',
#                                  verbose_name='所选设计师')
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_designer',
#                               verbose_name='所属订单')
#
#
# class OrderDw(models.Model):
#     """全屋软装订单详情"""


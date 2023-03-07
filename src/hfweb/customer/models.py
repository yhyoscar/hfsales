from django.db import models
from commons.models import Address

from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.timezone import localtime
# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=20, verbose_name="客户分组名称")

    def __str__(self):
        return self.name

    def get_customer_count(self):
        return Customer.objects.filter(group__id=self.id).distinct().count()
    get_customer_count.short_description = "客户数量"

    def get_member_count(self):
        return Customer.objects.filter(group__id=self.id, is_member=True).distinct().count()
    get_member_count.short_description = "会员数量"


class Customer(Address):
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=10, null=True, blank=True, verbose_name="电话")
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="分组")
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name="Email")
    wechat = models.CharField(max_length=50, null=True, blank=True, verbose_name="微信")
    facebook = models.CharField(max_length=10, null=True, blank=True, verbose_name="Facebook")
    is_member = models.BooleanField(default=False, verbose_name="是否为禾富会员？")
    membership_start_time = models.DateTimeField(blank=True, null=True, verbose_name="成为会员时间")
    bak_name = models.CharField(max_length=50, verbose_name="紧急联系人姓名", null=True, blank=True)
    bak_phone = models.CharField(max_length=10, null=True, blank=True, verbose_name="紧急联系人电话")
    product_options = [ ('MR', '食用菌'),
                        ('VG', '蔬菜'),
                        ('FR', '瓜果'),
                        ('EG', '蛋类'),
                        ('MT', '肉类'),
                        ('CK', '熟食')]
    prefer_communication = models.CharField(max_length=1, verbose_name="沟通方式偏好", blank=True, null=True,
        choices=[("C", "微信"),
                 ("P", "电话"), 
                 ("T", "短信"), 
                 ("E", "Email"), 
                 ("F", "Facebook"),
                 ('O', "线下见面")])
    prefer_product_1 = models.CharField(max_length=2, verbose_name="产品偏好1", blank=True, null=True,
        choices=product_options)
    prefer_product_2 = models.CharField(max_length=2, verbose_name="产品偏好2", blank=True, null=True,
        choices=product_options)
    prefer_product_3 = models.CharField(max_length=2, verbose_name="产品偏好3", blank=True, null=True,
        choices=product_options)
    prefer_shopping = models.CharField(max_length=1, verbose_name="购买方式偏好", blank=True, null=True,
        choices=[("C", "微信"),
                 ("W", "网购"),
                 ("P", "电话")])
    prefer_ship = models.CharField(max_length=1, verbose_name="产品递送方式偏好", blank=True, null=True,
        choices=[("D", "送货上门"),
                 ("L", "本地取货点取货"),
                 ("F", "自己去农场取货")])
    perfer_membership = models.CharField(max_length=1, verbose_name="成为会员意向", blank=True, null=True,
        choices=[("A", "已是会员"),
                 ("1", "未来1个月内会考虑加入"),
                 ("3", "未来3个月内会考虑加入"),
                 ("Y", "未来12个月内会考虑加入"), 
                 ("N", "暂不考虑加入")])
    note = models.TextField(max_length=400, verbose_name="备注信息", blank=True, null=True)

    def __str__(self):
        if self.is_member:
            return f"{self.name}(会员)"
        else:
            return self.name
    
    def get_balance(self):
        ndd, sdd = self.get_deposit_info()
        ntotal, stotal, naa, saa = self.get_consume_info()
        return sdd - saa

    def show_balance(self):
        bal = round(self.get_balance(), 2)
        if bal >= 1:
            text = f'<b><font color="green">{bal}</font></b>'
        elif bal <= -1:
            text = f'<b><font color="red">{bal}</font></b>'
        else:
            text = f'<b><font color="black">{bal}</font></b>'
        return mark_safe(text)
    show_balance.short_description = "账户余额($)"

    def show_transaction_history(self):
        text = '<table class="table table-hover"><thead><tr>'+\
            '<th scope="col">付款时间</th>'+\
            '<th scope="col">付款方式</th>'+\
            '<th scope="col">金额($)</th>'+\
            '<th scope="col">购买对象</th>'+\
            '<th scope="col">账户余额($)</th></tr></thead><tbody>'
        objs = Transaction.objects.filter(customer__id=self.id).order_by('-time')
        balances = [0.0]
        for obj in objs[::-1]:
            if obj.payfor == 1:
                balances.append(balances[-1]+obj.amount)
            elif obj.method == 'AA':
                balances.append(balances[-1]-obj.amount)
            else:
                balances.append(balances[-1])
        balances = balances[::-1]
        for i in range(len(objs)):
            obj = objs[i]
            text += '<tr>'+\
                    '<td><a href="/admin/customer/transaction/'+str(obj.id)+'/change/">'+str(localtime(obj.time))[:19]+'</a></td>'+\
                '<td>'+str(obj.get_method_display())+'</td>'+\
                '<td>'+str(round(obj.amount,2))+'</td>'+\
                '<td>'+str(obj.get_payfor_display())+'</td>'+\
                '<td>'+str(round(balances[i],2))+'</td></tr>'
        text += '</tbody></table>'
        return mark_safe(text)
    show_transaction_history.short_description = "历史交易记录"
    show_transaction_history.allow_tags = True

    def get_deposit_info(self):
        total = 0.0
        objs = Transaction.objects.filter(customer__id=self.id, payfor=1).exclude(method='AA')
        for obj in objs:
            total += obj.amount
        return len(objs), total

    def show_deposit_info(self):
        n, s = self.get_deposit_info()
        return f"充值{n}次，总共${round(s, 2)}"
    show_deposit_info.short_description = "充值记录"

    def get_consume_info(self):
        total, naa, aa = 0, 0, 0
        objs = Transaction.objects.filter(customer__id=self.id, payfor=-1)
        for obj in objs:
            total += obj.amount
            if obj.method == 'AA':
                naa += 1
                aa += obj.amount
        return len(objs), total, int(naa), aa

    def show_consume_info(self):
        ntotal, stotal, naa, saa = self.get_consume_info()
        return f"消费{ntotal}次，总共${round(stotal, 2)} (使用代金券{naa}次，消费${round(saa, 2)})"
    show_consume_info.short_description = "消费记录"

    def show_prefer_communication(self):
        if self.prefer_communication:
            out = self.get_prefer_communication_display()
            if self.prefer_communication == 'C':
                if self.wechat:
                    return out+": "+self.wechat
                else:
                    return out
            elif self.prefer_communication in ['T', 'P']:
                if self.phone:
                    return out+": "+self.phone
                else:
                    return out
            elif self.prefer_communication == 'E':
                if self.email:
                    return out+": "+self.email
                else:
                    return out
            elif self.prefer_communication == 'F':
                if self.facebook:
                    return out+self.facebook
                else:
                    return out
            else:
                return out
        else:
            return "未知"
    show_prefer_communication.short_description = "沟通方式偏好"


class Transaction(models.Model):
    time = models.DateTimeField(verbose_name="付款时间")
    customer = models.ForeignKey("Customer", verbose_name="付款人", on_delete=models.PROTECT)
    method = models.CharField(max_length=2, verbose_name="付款方式",
        choices=[("AA", "代金券"),
                 ("CS", "现金"),
                 ("CK", "支票"),
                 ("ZE", "zelle转账"),
                 ("VM", "venmo转账"),
                 ("CC", "信用卡"),
                 ("OT", "其它方式")])
    amount = models.FloatField(verbose_name="金额($)")
    payfor = models.IntegerField(verbose_name="购买对象", 
        choices=[(1, "代金券"), (-1, "农产品")])
    memo = models.TextField(max_length=400, null=True, blank=True, verbose_name="备注")

    def __str__(self):
        return f"{self.time}: {self.customer} {self.get_method_display()}支付${round(self.amount,2)}购买{self.get_payfor_display()}"




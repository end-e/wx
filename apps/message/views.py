# -*- coding: utf-8 -*-
import time

from django.core.exceptions import ObjectDoesNotExist
from user.models import WechatMembers

from wechatpy.replies import TextReply, EmptyReply
from utils import db


def switch_type(msg):
    """
    微信推送事件分发
    """
    from_type = msg.type

    # 推送文字消息
    if from_type == 'text':
        if msg.content == '红包':
            to_content = '[小宽摊手]非常遗憾，活动已结束，不过没关系，人生还有诗和远方。'
        elif msg.content == '解除绑定':
            try:
                WechatMembers.objects.get(openid=msg.source).delete()
                to_content = '解除绑定成功。'
            except ObjectDoesNotExist:
                to_content = '嗨，小宽发现您还未绑定会员。\n' \
                             '<a href="https://open.weixin.qq.com/connect/oauth2/authorize?' \
                             'appid=wx5afe243d26d9fe30&redirect_uri=http%3A//www.zisai.net/user/' \
                             'membersbound&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect">' \
                             '点击这里</a>绑定会员'
        else:
            to_content = '嗨，我是小宽，本公众号主要提供会员绑定、消费提醒等。如需查看门店营业时间和电话、海报信息、' \
                         '各种活动推广等请关注公众号“宽广超市”，感谢关注。'
        reply = TextReply(content=to_content, message=msg)
        xml = reply.render()
        return xml
    # 推送事件
    elif from_type == 'event':
        # 关注事件
        if msg.event == 'subscribe':
            to_content = '嗨，欢迎关注，我是小宽。宽广超市全新礼品卡上线了，送朋友传心意，好玩有趣，还能发图片录视频嘞。' \
                         '点击菜单\"礼品卡\"传心意吧~'
            reply = TextReply(content=to_content, message=msg)
            xml = reply.render()
            return xml
        # 自定义菜单事件
        elif msg.event == 'click':
            # 解除绑定
            if msg.key == 'jcbd':
                try:
                    WechatMembers.objects.get(openid=msg.source)
                    to_content = '发送\"解除绑定\"关键字，解除会员绑定。解除绑定后将无法使用会员相关功能。'
                except ObjectDoesNotExist:
                    to_content = '嗨，我是小宽，您还没有操作会员绑定呢。'
                reply = TextReply(content=to_content, message=msg)
                xml = reply.render()
                return xml
            # 消费记录
            elif msg.key == 'xfjl':
                # 通过openid 查询用户是否绑定过微信
                user_set = WechatMembers.objects.filter(openid=msg.source)
                # 已绑定
                if user_set:

                    # 会员卡号
                    member_number = ''
                    for user in user_set:
                        member_number = user.membernumber

                    # 卡服 获取消费明细
                    conn = db.getMsSqlConn()
                    cursor = conn.cursor()

                    # 查询最后一次消费的明细
                    last_buy_sql = "SELECT ListNo,SaleValue,DiscValue,SDate FROM CardSaleGoods " \
                                   "WHERE cardno='{member_number}' " \
                                   "AND SDate IN " \
                                   "(SELECT CONVERT(CHAR(10),lastusedate,120) " \
                                   "FROM Guest " \
                                   "WHERE cardno='{member_number}')".format(member_number=member_number)
                    cursor.execute(last_buy_sql)
                    last_buy_rs = cursor.fetchall()
                    cursor.close()
                    conn.close()

                    # 如果没有查询到消费明细 再取Guest表的数据
                    if not last_buy_rs:
                        conn = db.getMsSqlConn()
                        cursor = conn.cursor()

                        # 查询今天是否消费
                        today_buy_sql = "SELECT LastUseDate FROM Guest WHERE cardno='{member_number}'".format(
                            member_number=member_number)
                        cursor.execute(today_buy_sql)
                        today_buy_rs = cursor.fetchall()
                        cursor.close()
                        conn.close()

                        # 格式化时间
                        today = '{0:%Y-%m-%d}'.format(today_buy_rs[0]['LastUseDate'])
                        now = str(time.strftime("%Y-%m-%d", time.localtime()))

                        # 判断今天是否消费
                        if today == now:
                            to_content = '客官，数据正在努力奔跑中...请以今天超市打印的购物小票为准，或者明天再来看看吧\n' \
                                         '哦哦，对了[憨笑]，如果您绑定了会员，会收到我发送给您的消费提醒。'
                        else:
                            to_content = '客官最近都没来购物，小宽好想你呦~[可怜]'
                    # 如果查询到消费明细
                    else:
                        # 存放当天消费明细 如果有多次消费 存放格式[{...}, {...}]
                        temp_set = set()
                        date_list = []

                        # 计算消费次数
                        for row in last_buy_rs:
                            temp_set.add(row['ListNo'])
                            if not date_list:
                                date_list.append(row['SDate'])

                        # 消费次数
                        records = len(temp_set)
                        # 消费日期
                        date = '{0:%Y-%m-%d}'.format(date_list[0])

                        to_content = '您最近一次在{sdate}，消费{records}次\n' \
                                     '<a href="http://www.huigo.com/wechat/shoppinglist.php?memberNumber={member_number}">' \
                                     '查看消费明细' \
                                     '</a>'.format(sdate=date, records=records, member_number=member_number)
                # 未绑定
                else:
                    to_content = '嗨，我是小宽，您绑定会员后我才能帮您查询呐，不过您得是实名制会员才行。\n' \
                                 '那么问题来了，如何成为实名制会员？[疑问]\n' \
                                 'so easy~~[调皮]，请移步服务台咨询我们的客服人员。'

                reply = TextReply(content=to_content, message=msg)
                xml = reply.render()
                return xml
        # 模板消息发送任务完成事件
        elif msg.event == 'templatesendjobfinish':
            # TODO
            # 模板消息发送成功后的逻辑处理
            # if msg.status == '<![CDATA[failed: system failed]]>':
            # 暂时回复空串，不做任何处理
            return EmptyReply()
    else:
        return 'success'

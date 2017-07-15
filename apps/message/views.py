# -*- coding: utf-8 -*-
from django.http import HttpResponse

from wechatpy.replies import TextReply, create_reply


def switch_type(msg):
    """
    推送消息公共属性
    id 消息id，64位整数
    source 消息的来源用户，即发送消息的用户
    target 消息的目标用户
    create_time 消息的发送时间，UNIX时间戳
    type 消息的类型

    推送文本消息属性（用户发送给服务号消息）
    type: text
    content: 消息的内容
    """
    from_id = msg.id
    from_source = msg.source
    from_target = msg.target
    from_create_time = msg.create_time
    from_type = msg.type
    from_content = msg.content

    if from_type == 'text':
        if from_content == '红包':
            to_content = '活动已结束！'
        else:
            to_content = '本公众号主要提供会员绑定、消费提醒等，如需查看门店营业时间和电话、海报信息、各种活动推广等请关注公众号“宽广超市”，感谢关注。'
        reply = TextReply(content=to_content, message=msg)
        xml = reply.render()
        return xml
    else:
        return 'success'

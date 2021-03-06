# -*- coding: utf-8 -*-
import json
import datetime

from django.http import HttpResponse

from wxapp.models import PosterImage
from wxapp.constants import MEDIA_URL
from api.decorator import signature


@signature
def getPosterList(request):
    result_dict = {'status': 1, 'msg': []}

    kwargs = {}

    kwargs.setdefault('begin_date__lte', datetime.datetime.now())
    kwargs.setdefault('end_date__gte', datetime.datetime.now())

    posters = PosterImage.objects.filter(**kwargs)
    msg = []
    if posters:
        for item in posters:
            vardict = {}
            vardict['poster_id'] = str(item.id)
            vardict['poster_name'] = str(item.poster_name)
            vardict['begin_date'] = str(item.begin_date.strftime("%Y-%m-%d"))
            vardict['end_date'] = str(item.end_date.strftime("%Y-%m-%d"))
            vardict['poster_image'] = MEDIA_URL + str(item.poster_image)
            vardict['link_address'] = str(item.link_address)
            msg.append(vardict)

        result_dict['status'] = 0
        result_dict['msg'] = msg

    return HttpResponse(json.dumps(result_dict), content_type="application/json")


@signature
def getPosterInfo(request):
    poster_id = request.GET.get('poster_id', '')

    result_dict = {'status': 1, 'msg': []}

    poster = PosterImage.objects.get(pk=poster_id)
    msg = {}
    if poster:
        msg['id'] = str(poster.id)
        msg['poster_name'] = str(poster.poster_name)
        msg['begin_date'] = str(poster.begin_date.strftime("%Y-%m-%d"))
        msg['end_date'] = str(poster.end_date.strftime("%Y-%m-%d"))
        msg['poster_image'] = MEDIA_URL + str(poster.poster_image)
        msg['link_address'] = str(poster.link_address)

        result_dict['status'] = 0
        result_dict['msg'] = msg

    return HttpResponse(json.dumps(result_dict), content_type="application/json")

from django.shortcuts import render, redirect
from wxapp.models import PosterImage


def index(request):
    poster_name = request.GET.get('poster_name', '')

    kwargs = {}

    if poster_name != '':
        kwargs.setdefault('poster_name__contains', poster_name)

    List = PosterImage.objects.filter(**kwargs)

    return render(request, 'wxapp/poster/index.html', locals())


def posterEdit(request, poster_id):
    poster = []
    img_url = ''
    if poster_id != '0':
        poster = PosterImage.objects.get(pk=poster_id)
        if poster.poster_image != '':
            img_url = poster.poster_image.url

    return render(request, 'wxapp/poster/edit_page.html', {'poster': poster, 'img_url': img_url})


def posterSave(request):
    poster_id = request.POST.get('poster_id', '')
    if poster_id is None:
        poster_id = ''
    poster_name = request.POST.get('poster_name', '')
    begin_date = request.POST.get('begin_date', '')
    end_date = request.POST.get('end_date', '')
    end_date += ' 23:59:59'
    poster_image = request.FILES.get('poster_image')
    if poster_image == None:
        poster_image = ''

    if poster_id != '':
        result = PosterImage.objects.get(pk=poster_id)
        result.poster_name = poster_name
        result.begin_date = begin_date
        result.end_date = end_date
        if poster_image != '':
            result.poster_image = poster_image
        result.save()
    else:
        result = PosterImage.objects.create(poster_name=poster_name,
                                            begin_date=begin_date,
                                            end_date=end_date,
                                            poster_image=poster_image)
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1
    return redirect('/wxapp/poster/index/')


def posterDelete(request, poster_id):
    result = None
    if poster_id != '0':
        result = PosterImage.objects.get(pk=poster_id).delete()
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1
    return redirect('/wxapp/poster/index/')
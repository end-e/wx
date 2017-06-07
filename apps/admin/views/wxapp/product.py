from django.shortcuts import render

from wxapp.models import Product


def index(request):
    product_code = request.GET.get('product_code', '')
    product_name = request.GET.get('product_name', '')

    kwargs = {}

    if product_code != '':
        kwargs.setdefault('product_code__contains', product_code)

    if product_name != '':
        kwargs.setdefault('product_name__contains', product_name)

    List = Product.objects.filter(**kwargs).order_by('product_code')

    return render(request, 'wxapp/product/index.html', locals())


def productEdit(request, product_id):
    product = []
    img_url = ''
    if product_id != '0':
        product = Product.objects.get(pk=product_id)
        if product.product_image != '':
            img_url = product.product_image.url

    return render(request, 'wxapp/product/edit_page.html', {'product': product, 'img_url': img_url})


def productSave(request):
    product_id = request.POST.get('product_id', '')
    if product_id is None:
        product_id = ''
    product_code = request.POST.get('product_code', '')
    product_name = request.POST.get('product_name', '')
    price = request.POST.get('price', '')
    stock = request.POST.get('stock', '')
    type_flag = request.POST.get('type_flag', '')
    enable_flag = request.POST.get('enable_flag', '')
    begin_date = request.POST.get('begin_date', '')
    end_date = request.POST.get('end_date', '')
    product_weight = request.POST.get('product_weight', '')
    product_image = request.FILES.get('product_image')
    if product_image == None:
        product_image = ''

    if product_id != '':
        result = Product.objects.get(pk=product_id)
        result.product_code = product_code
        result.product_name = product_name
        result.price = price
        result.stock = stock
        result.type_flag = type_flag
        result.enable_flag = enable_flag
        result.begin_date = begin_date
        result.end_date = end_date
        result.product_weight = product_weight
        if product_image != '':
            result.product_image = product_image

        result.save()
    else:
        result = Product.objects.create(product_code=product_code,
                                        product_name=product_name,
                                        price=price,
                                        stock=stock,
                                        type_flag=type_flag,
                                        enable_flag=enable_flag,
                                        begin_date=begin_date,
                                        end_date=end_date,
                                        product_weight=product_weight,
                                        product_image=product_image)
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1

    List = Product.objects.all().order_by('product_code')

    return render(request, 'wxapp/product/index.html', locals())

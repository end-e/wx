from django.shortcuts import render, redirect

from wxapp.models import Voucher, VoucherClass, Shops


def index(request):
    voucher_no = request.GET.get('voucher_no', '')
    voucher_name = request.GET.get('voucher_name', '')

    kwargs = {}

    if voucher_no != '':
        kwargs.setdefault('voucher_no__contains', voucher_no)

    if voucher_name != '':
        kwargs.setdefault('voucher_name__contains', voucher_name)

    List = Voucher.objects.filter(**kwargs).order_by('voucher_no')

    return render(request, 'wxapp/voucher/index.html', locals())


def voucherEdit(request, voucher_id):
    voucher = []
    img_url = ''

    shops = Shops.objects.all()
    classs = VoucherClass.objects.all()
    if voucher_id != '0':
        voucher = Voucher.objects.get(pk=voucher_id)
        if voucher.voucher_image != '':
            img_url = voucher.voucher_image.url
    return render(request, 'wxapp/voucher/edit_page.html',
                  {'voucher': voucher, 'classs': classs, 'shops': shops, 'img_url': img_url})


def voucherSave(request):
    voucher_id = request.POST.get('voucher_id', '')
    if voucher_id is None:
        voucher_id = ''
    voucher_no = request.POST.get('voucher_no', '')
    voucher_name = request.POST.get('voucher_name', '')
    unit_price = request.POST.get('unit_price', '')
    voucher_price = request.POST.get('voucher_price', '')
    goods_code = request.POST.get('goods_code', '')
    type_flag = request.POST.get('type_flag', '')
    code_flag = request.POST.get('code_flag', '')
    shop_codes = request.POST.get('shop_codes', '')
    begin_date = request.POST.get('begin_date', '')
    end_date = request.POST.get('end_date', '')
    end_date += ' 23:59:59'
    voucher_image = request.FILES.get('voucher_image')
    if voucher_image == None:
        voucher_image = ''

    if voucher_id != '':
        result = Voucher.objects.get(pk=voucher_id)
        result.voucher_no = voucher_no
        result.voucher_name = voucher_name
        result.unit_price = unit_price
        result.voucher_price = voucher_price
        result.goods_code = goods_code
        result.type_flag = type_flag
        result.code_flag = code_flag
        result.shop_codes = shop_codes
        result.begin_date = begin_date
        result.end_date = end_date
        if voucher_image != '':
            result.voucher_image = voucher_image
        result.save()
    else:
        result = Voucher.objects.create(voucher_no=voucher_no,
                                        voucher_name=voucher_name,
                                        unit_price=unit_price,
                                        voucher_price=voucher_price,
                                        goods_code=goods_code,
                                        type_flag=type_flag,
                                        code_flag=code_flag,
                                        shop_codes=shop_codes,
                                        begin_date=begin_date,
                                        end_date=end_date,
                                        voucher_image=voucher_image)
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1
    return redirect('/wxapp/voucher/index/')


def voucherDelete(request, voucher_id):
    result = None
    if voucher_id != '0':
        result = Voucher.objects.get(pk=voucher_id).delete()
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1
    return redirect('/wxapp/voucher/index/')

def classList(request):
    List = VoucherClass.objects.all()

    return render(request, 'wxapp/voucher/class_list.html', locals())


def classEdit(request, class_id):
    v_class = []

    if class_id != '0':
        v_class = VoucherClass.objects.get(pk=class_id)
    return render(request, 'wxapp/voucher/class_edit.html', {'v_class': v_class})


def classSave(request):
    class_id = request.POST.get('class_id', '')
    if class_id is None:
        class_id = ''
    class_name = request.POST.get('class_name', '')

    if class_id != '':
        result = VoucherClass.objects.get(pk=class_id)
        result.class_name = class_name
        result.save()
    else:
        result = VoucherClass.objects.create(class_name=class_name)
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1
    return redirect('/wxapp/voucher/class_list/')


def classDelete(request, class_id):
    result = None
    if class_id != '0':
        result = VoucherClass.objects.get(pk=class_id).delete()
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1
    return redirect('/wxapp/voucher/class_list/')

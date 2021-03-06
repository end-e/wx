import datetime
import os
from random import sample

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.db.models import Q

from admin.utils.paginator import MyPaginator
from wxapp.models import Voucher, VoucherClass, Shops, DisCode
from .forms import AddDiscodeForm, FindDiscodeForm


def index(request):
    voucher_no = request.GET.get('voucher_no', '')
    voucher_name = request.GET.get('voucher_name', '')

    kwargs = {}

    if voucher_no != '':
        kwargs.setdefault('voucher_no__contains', voucher_no)

    if voucher_name != '':
        kwargs.setdefault('voucher_name__contains', voucher_name)

    List = Voucher.objects.filter(**kwargs).order_by('-end_date')

    paginator = MyPaginator(List, 10)
    page_num = request.GET.get('page', 1)
    try:
        List = paginator.page(page_num)
    except Exception as e:
        print(e)

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
                  {'voucher': voucher, 'classs': classs, 'shops': shops, 'img_url': img_url, 'voucher_id': voucher_id})


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
    else:
        file_type = os.path.splitext(voucher_image.name)[1]
        voucher_image.name = "voucher_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + file_type

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
    return redirect(reverse('wxapp:voucher_index'))


def voucherDelete(request, voucher_id):
    result = None
    if voucher_id != '0':
        result = Voucher.objects.get(pk=voucher_id).delete()
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1
    return redirect(reverse('wxapp:voucher_index'))


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
    return redirect(reverse('wxapp:class_list'))


def classDelete(request, class_id):
    result = None
    if class_id != '0':
        result = VoucherClass.objects.get(pk=class_id).delete()
    msg = {}
    if result:
        msg['status'] = 0
    else:
        msg['status'] = 1
    return redirect(reverse('wxapp:class_list'))


class DiscodeListViews(View):
    """
    默认券验证码列表
    """

    def get(self, request):
        # 默认页面展示所有优惠券
        all_discode = DisCode.objects.all()
        paginator = MyPaginator(all_discode, 10)
        page_num = request.GET.get('page', 1)
        try:
            all_discode = paginator.page(page_num)
        except Exception as e:
            print(e)
        return render(request, 'wxapp/voucher/discode_list.html', locals())


class DiscodeQueryViews(View):
    """
    验证码查询
    """

    def get(self, request):
        batch = request.GET.get('batch', '')
        discode = request.GET.get('discode', '')
        # 查询券授权码
        if batch and discode:
            all_discode = DisCode.objects.filter(dis_code=discode, batch=batch)
        else:
            all_discode = DisCode.objects.filter(Q(batch=batch) | Q(dis_code=discode))

        paginator = MyPaginator(all_discode, 15)
        page_num = request.GET.get('page', 1)
        try:
            all_discode = paginator.page(page_num)
        except Exception as e:
            print(e)
        return render(request, 'wxapp/voucher/discode_list.html', locals())


class AddDiscodeViews(View):
    """
    生成券验证码
    """

    def get(self, request):
        return render(request, 'wxapp/voucher/discode_add.html')

    def post(self, request):
        form = AddDiscodeForm(request.POST)
        # 验证表单
        if form.is_valid():
            nums = form.cleaned_data['nums']
            batch = form.cleaned_data['batch']

            for i in range(0, nums):
                obj = DisCode(batch=batch)
                dis_code = ''.join(sample('0123456789', 4))
                dis_code = batch + dis_code
                obj.dis_code = dis_code
                obj.save()

            all_discode = DisCode.objects.filter(batch=batch)

            paginator = MyPaginator(all_discode, 15)
            page_num = request.GET.get('page', 1)
            try:
                all_discode = paginator.page(page_num)
            except Exception as e:
                print(e)

            return redirect(reverse('wxapp:discode_list'), {
                'batch': batch,
                'all_discode': all_discode
            })

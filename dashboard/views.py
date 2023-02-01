from django.shortcuts import render, redirect
from main.models import *
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import ExtractDay, ExtractMonth
import calendar


def home_view(request):
    order = Order.objects.all().order_by('-id')
    count = Order.objects.all().count()
    today = datetime.today() - timedelta(days=1)
    month = datetime.today() - timedelta(days=30)
    day = Order.objects.filter(created__gte=today).count()
    months = Order.objects.filter(created__gte=month).count()
    qs = Order.objects.filter(
        created__gte=month
    ).annotate(
        day=ExtractDay("created"),
        mon=ExtractMonth('created'),
    ).values(
        'day', 'mon'
    ).annotate(
        n=Count('pk')
    ).order_by('mon')
    mon_list = []
    for i in qs:
        i['mon'] = (calendar.month_abbr[i['mon']])
        if len(mon_list) >= 30:
            del mon_list[0]
            mon_list.append(i)
        else:
            mon_list.append(i)
    context = {
        "all_apps": order,
        "count": count,
        "day": day,
        "month": months,
        "qs": mon_list,
    }
    return render(request, 'index.html')


""" Search """


def search_view(request):
    if request.method == "POST":
        search = request.POST['search']
        info = Q(Q(name_uz__icontains=search) | Q(name_ru__icontains=search))
        product = Product.objects.filter(info)
        context = {
            "search": product
        }
        return render(request, '', context)


""" End Search """
""" Banner """


def banner_view(request):
    context = {
        "banner": Banner.objects.last()
    }
    return render(request, 'banner.html', context)


def create_banner(request):
    if request.method == "POST":
        title_uz = request.POST['title_uz']
        title_ru = request.POST['title_ru']
        quality_uz = request.POST['quality_uz']
        quality_ru = request.POST['quality_ru']
        photo = request.FILES.get('photo')
        Banner.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            quality_uz=quality_uz,
            quality_ru=quality_ru,
            photo=photo,
        )
        return redirect("banner_url")
    return redirect("banner_url")


def delete_banner(request, pk):
    banner = Banner.objects.get(pk=pk)
    banner.delete()
    return redirect("banner_url")


def change_banner(request, pk):
    if request.method == 'POST':
        banner = Banner.objects.get(pk=pk)
        title_uz = request.POST['title_uz']
        title_ru = request.POST['title_ru']
        quality_uz = request.POST['quality_uz']
        quality_ru = request.POST['quality_ru']
        photo = request.FILES.get('photo')
        banner.title_uz = title_uz
        banner.title_ru = title_ru
        banner.quality_uz = quality_uz
        banner.quality_ru = quality_ru
        if photo is not None:
            banner.photo = photo
        banner.save()
        return redirect("banner_url")
    return redirect("banner_url")

""" End Banner """
""" Order """

def order_view(request):
    context = {
        "order": Order.objects.all()
    }
    return render(request, '', context)


def create_order(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        Order.objects.create(
            name=name,
            phone=phone,
        )
        return redirect("order_view")
    return redirect("order_view")


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect("order_view")


def change_order(request, pk):
    order = Order.objects.get(pk=pk)
    context = {
        "order" : order
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        order.name = name
        order.phone = phone
        order.save()
    return render(request, '', context)

""" End Order"""
""" Product """
def PagenatorPage(List, num ,request):
    paginator = Paginator(List, num)
    pages = request.GET.get('page')
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list

def product_view(request):
    products = Product.objects.all().order_by('id')
    context = {
        "products": PagenatorPage(products, 6, request)
    }
    return render(request, 'products.html', context)


def create_product(request):
    if request.method == "POST":
        name_uz = request.POST['name_uz']
        name_ru = request.POST['name_ru']
        photo = request.FILES['photo']
        price = request.POST['price']
        sale = request.POST.get('sale')
        new_product = Product.objects.create(
            name_uz=name_uz,
            name_ru=name_ru,
            photo=photo,
            price=price,
            sale=sale,
        )
        if sale is not None:
            new_product.is_sale=True
            new_product.save()
    return redirect("product_url")


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect("product_url")


def change_product(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(pk=pk)
        name_uz = request.POST['name_uz']
        name_ru = request.POST['name_ru']
        photo = request.FILES.get('photo')
        price = float(request.POST.get('price'))
        sale = float(request.POST.get('sale'))
        product.name_uz = name_uz
        product.name_ru = name_ru
        product.price = price
        product.sale = sale
        if sale is not None:
            product.is_sale = True
        if photo is not None:
            product.photo = photo
        product.save()
    return redirect('product_url')

""" End Product """

""" About Product """


def about_product_view(request):
    context = {
        "about_product": About_Product.objects.all().order_by('-id')
    }
    return render(request, 'about-product.html', context)


def create_about_product(request):
    if request.method == "POST":
        img = request.FILES.get('img')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        AboutProduct.objects.create(
            img=img,
            text_uz=text_uz,
            text_ru=text_ru,
        )
        return redirect("about_product_view")
    return redirect("about_product_view")


def delete_about_product(request, pk):
    about_product = AboutProduct.objects.get(id=pk)
    about_product.delete()
    return redirect("about_product_view")


def change_about_product(request, pk):
    about_product = AboutProduct.objects.get(pk=pk)
    context = {
        "about_product": about_product
    }
    if request.method == 'POST':
        img = request.POST.get('img')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        if img is not None:
            about_product.photo = photo
        about_product.text_uz = text_uz
        about_product.text_ru = text_ru
        about_product.save()
    return render(request, '', context)

""" End About Product """
""" Advice Item """


def advice_item_view(request):
    context = {
        "advice_item": Advice_item.objects.all()
    }
    return render(request, '', context)


def create_advice_item(request):
    if request.method == "POST":
        advice_uz = request.POST.get('advice_uz')
        advice_ru = request.POST.get('advice_ru')
        Advice_item.objects.create(
            advice_uz=advice_uz,
            advice_ru=advice_ru,
        )
        return redirect("advice_item_view")
    return redirect("advice_item_view")


def delete_advice_item(request, pk):
    advice_item = Advice_item.objects.get(id=pk)
    advice_item.delete()
    return redirect("advice_item_view")


def change_advice_item(request, pk):
    advice_item = Advice_item.objects.get(pk=pk)
    context = {
        "advice_item": advice_item
    }
    if request.method == 'POST':
        advice_uz = request.POST.get('advice_uz')
        advice_ru = request.POST.get('advice_ru')
        advice_item.advice_uz = advice_uz
        advice_item.advice_ru = advice_ru
        advice_item.save()
    return render(request, '', context)


""" End Advice Item """

""" Advice Title  """


def advice_title_view(request):
    context = {
        "advice_title": Advice_Title.objects.all()
    }
    return render(request, '', context)


def create_advice_title(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        Advice_Title.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
        )
        return redirect("advice_title_view")
    return redirect("advice_title_view")


def delete_advice_title(request, pk):
    advice_title = Advice_Title.objects.get(id=pk)
    advice_title.delete()
    return redirect("advice_title_view")


def change_advice_title(request, pk):
    advice_title = Advice_Title.objects.get(pk=pk)
    context = {
        "advice_title": advice_title
    }
    if request.method == 'POST':
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        advice_item.title_uz = title_uz
        advice_title.title_ru = title_ru
        advice_title.save()
    return render(request, '', context)

""" End Advice Title """
""" About Company """


def about_company_view(request):
    context = {
        "about_company": About_Company.objects.all()
    }
    return render(request, '', context)


def create_about_company(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        img = request.FILES.get('img')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        About_Company.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            img=img,
            text_uz=text_uz,
            text_ru=text_ru,
        )
        return redirect("about_company_view")
    return redirect("about_company_view")


def delete_about_company(request, pk):
    about_company = About_Company.objects.get(id=pk)
    about_company.delete()
    return redirect("about_company_view")


def change_about_company(request, pk):
    about_company = About_Company.objects.get(pk=pk)
    context = {
        "about_company": about_company
    }
    if request.method == 'POST':
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        img = request.FILES.get('img')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        about_company.title_uz = title_uz
        about_company.title_ru = title_ru
        if img is not None:
            about_company.img = img
        about_company.text_uz = text_uz
        about_company.text_ru = text_ru
        about_company.save()
    return render(request, '', context)

""" End About Company """

""" Instruction """

def instruction_view(request):
    context = {
        "instruction": Instruction.objects.all()
    }
    return render(request, '', context)


def create_instruction(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        Instruction.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            text_uz=text_uz,
            text_ru=text_ru,
            )
        return redirect("instruction_view")
    return redirect("instruction_view")


def delete_instruction(request, pk):
    instruction = Instruction.objects.get(id=pk)
    instruction.delete()
    return redirect("instruction_view")


def change_instruction(request, pk):
    instruction = Instruction.objects.get(pk=pk)
    context = {
        "instruction": instruction
    }
    if request.method == 'POST':
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        instruction.title_uz = title_uz
        instruction.title_ru = title_ru
        instruction.text_uz = text_uz
        instruction.text_ru = text_ru
        instruction.save()
    return render(request, '', context)

""" End Instruction """
""" Fact Title """


def fact_title_view(request):
    context = {
        "fact_title": Fact_Title.objects.all()
    }
    return render(request, '', context)


def create_fact_title(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        Fact_Title.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            )
        return redirect("fact_title_view")
    return redirect("fact_title_view")


def delete_fact_title(request, pk):
    fact_title = Fact_Title.objects.get(id=pk)
    fact_title.delete()
    return redirect("fact_title_view")


def change_fact_title(request, pk):
    fact_title = Fact_Title.objects.get(pk=pk)
    context = {
        "fact_title": fact_title
    }
    if request.method == 'POST':
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        fact_title.title_uz = title_uz
        fact_title.title_ru = title_ru
        fact_title.save()
    return render(request, '', context)

""" End Fact Title """
""" Fact_item  """


def fact_item_view(request):
    context = {
        "fact_item": Fact_item.objects.all()
    }
    return render(request, '', context)


def create_fact_item(request):
    if request.method == "POST":
        description_uz = request.POST.get('description_uz')
        description_ru = request.POST.get('description_ru')
        number = request.POST.get('number')
        Fact_item.objects.create(
            description_uz=description_uz,
            description_ru=description_ru,
            number=number,
            )
        return redirect("fact_item_view")
    return redirect("fact_item_view")


def delete_fact_item(request, pk):
    fact_item = Fact_item.objects.get(id=pk)
    fact_item.delete()
    return redirect("fact_item_view")


def change_fact_item(request, pk):
    fact_item = Fact_item.objects.get(pk=pk)
    context = {
        "fact_item": fact_item
    }
    if request.method == 'POST':
        description_uz = request.POST.get('description_uz')
        description_ru = request.POST.get('description_ru')
        number = request.POST.get('number')
        fact_item.description_uz = description_uz
        fact_item.description_ru = description_ru
        fact_item.number = number
        fact_item.save()
    return render(request, '', context)

""" End Fact Item """
""" Info """


def info_view(request):
    context = {
        "info": Info.objects.all()
    }
    return render(request, '', context)


def create_info(request):
    if request.method == "POST":
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        description_uz = request.POST.get('description_uz')
        description_ru = request.POST.get('description_ru')
        telegram = request.POST.get('telegram')
        instagram = request.POST.get('instagram')
        youtube = request.POST.get('youtube')
        facebook = request.POST.get('facebook')
        Info.objects.create(
            name=name,
            logo=logo,
            description_uz=description_uz,
            description_ru=description_ru,
            telegram=telegram,
            instagram=instagram,
            youtube=youtube,
            facebook=facebook,
            )
        return redirect("info_view")
    return redirect("info_view")


def delete_info(request, pk):
    info = Info.objects.get(id=pk)
    info.delete()
    return redirect("info_view")


def change_info(request, pk):
    info = Info.objects.get(pk=pk)
    context = {
        "info": info
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.POST.get('logo')
        description_uz = request.POST.get('description_uz')
        description_ru = request.POST.get('description_ru')
        telegram = request.POST.get('telegram')
        instagram = request.POST.get('instagram')
        youtube = request.POST.get('youtube')
        facebook = request.POST.get('facebook')
        info.name = name
        if logo is not None:
            info.logo = logo
        info.description_uz = description_uz
        info.description_ru = description_ru
        info.telegram = telegram
        info.instagram = instagram
        info.youtube = youtube
        info.facebook = facebook
        info.save()
    return render(request, '', context)


""" End Info """
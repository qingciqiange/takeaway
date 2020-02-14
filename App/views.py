from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.
from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser
from App.views_helper import hash_str
from aixianfeng.settings import MEDIA_KEY_PREFIX


def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustBuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]
    main_shows =MainShow.objects.all()
    data = {
        "title":'首页',
        "main_wheels":main_wheels,
        'main_navs':main_navs,
        'main_mustbuys':main_mustbuys,
        'main_shop0_1':main_shop0_1,
        'main_shop1_3':main_shop1_3,
        'main_shop3_7':main_shop3_7,
        'main_shop7_11':main_shop7_11,
        'main_shows':main_shows,
    }
    return render(request,'main/home.html',context=data)

def market(request):
    return redirect(reverse('axf:market_with_params',kwargs={
        'typeid':104749,
        'childcid':0,
        'order_rule':0,
    }))

def market_with_params(request,typeid,childcid,order_rule):
    foodtypes = FoodType.objects.all()

    goods_list = Goods.objects.filter(categoryid=typeid)

    if childcid == '0':
        # '0'为全部类型
        pass
    else:
        goods_list = goods_list.filter(childcid=childcid)
    #0=默认排序,1=价格升序,2=价格降序,3=销量升序,4=销量降序
    if order_rule == '0':
        pass
    elif order_rule == '1':
        goods_list = goods_list.order_by('price')
    elif order_rule == '2':
        goods_list = goods_list.order_by('-price')
    elif order_rule == '3':
        goods_list = goods_list.order_by('productnum')
    elif order_rule == '4':
        goods_list = goods_list.order_by('-productnum')

    foodtype = foodtypes.get(typeid=typeid)

    foodtypechildnames =foodtype.childtypenames

    foodtypechildname_list = foodtypechildnames.split('#')
    foodtype_childname_list = []

    for foodtypechildname in foodtypechildname_list:
        foodtype_childname_list.append((foodtypechildname.split(':')))

    order_rule_list = [
        ['综合排序',0],
        ['价格升序',1],
        ['价格降序',2],
        ['销量升序',3],
        ['销量降序',4],
    ]

    data = {
        "title":'闪购',
        "foodtypes":foodtypes,
        "goods_list":goods_list,
        "typeid":int(typeid),
        "foodtype_childname_list":foodtype_childname_list,
        "childcid":childcid,
        "order_rule_list":order_rule_list,
        "order_rule_view":order_rule,

    }
    return render(request,'main/market.html',context=data)

def cart(request):
    return render(request,'main/cart.html')

def mine(request):

    user_id =request.session.get('user_id')
    data = {
        'title':'我的',
        'is_login':False,
    }
    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
    return render(request,'main/mine.html',context=data)

def register(request):
    if request.method == 'GET':

        data = {
            'title':'注册'
        }
        return render(request,'user/register.html',context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')

        password = make_password(password)

        user = AXFUser()
        user.u_username = username
        user.u_email = email
        user.u_password = password
        user.u_icon = icon

        user.save()

        return redirect(reverse('axf:login'))


def login(request):
    if request.method == 'GET':
        data = {
            'title':'登录'
        }
        return render(request,'user/login.html',context=data)

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        users = AXFUser.objects.filter(u_username=username)

        if users.exists():
            user = users.first()

            if check_password(password,user.u_password):

                request.session['user_id'] =user.id
                return redirect(reverse('axf:mine'))
            else:
                print('密码错误')
                return redirect(reverse('axf:login'))
        print('用户不存在')
        return redirect(reverse('axf:login'))


def check_user(request):

    username = request.GET.get('username')
    users = AXFUser.objects.filter(u_username=username)
    data = {
        "status":200,
        "msg":'ok',
    }
    if users.exists():
        data['status'] = 901
        data['msg'] = 'user already exist'
    else:
        pass
    return JsonResponse(data=data)


def logout(request):

    request.session.flush()
    return redirect(reverse('axf:mine'))
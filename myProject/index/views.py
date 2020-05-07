from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import ShareData as sd
from .models import  ShareSort as ss
from decimal import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
import copy

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

# Create your views here.
def index(request):
    isLogin = request.session.get('loginStatus')
    if isLogin is not True:
        return render(request, 'login.html')
    else:
        cateId = request.GET.get('cateid')

        data = ss.objects.filter(id= 552)
        print(data[0].share_name)
        context = {
            'cateId':cateId,
        }
        return render(request, 'index.html', context=context)

def statistics(request):
    isLogin = request.session.get('loginStatus')
    if isLogin is not True:
        return render(request, 'login.html')
    else:
        cateId = request.GET.get('cateid')
        date = request.GET.get('date', '2020-04-01')
        print(date)
        p_change = int(request.GET.get('p_change', 0))
        price_change = int(request.GET.get('price_change', 0))
        volume = int(request.GET.get('volume', 0))

        datas = sd.objects.filter(date=date)
        print(type(datas))

        print(date, p_change, price_change, volume)

        if p_change == 1:
            datas = datas.order_by('p_change')
            print('*^'*100)
        if p_change == 2:
            datas = datas.order_by('-p_change')

        if price_change == 1:
            datas = datas.order_by('price_change')
        if price_change == 2:
            datas = datas.order_by('-price_change')

        if volume == 1:
            datas = datas.order_by('volume')
        if volume == 2:
            datas = datas.order_by('-volume')

        datas = datas.values()
        print(type(datas))
        num = len(datas)
        datas = datas[:10]

        for data in datas:
            print(data)

        for key,data in enumerate(datas):
            other_data = ss.objects.filter(id=data['sort_id']).values()
            datas[key]['name'] = other_data[0]['share_name']
            datas[key]['code'] = other_data[0]['code']
            datas[key]['date'] = datas[key]['date'].strftime("%Y-%m-%d")

            if Decimal(datas[key]['p_change']) > 0:
                datas[key]['p_change'] = '+' + str(datas[key]['p_change'])
                datas[key]['p_mark'] = 1
            if Decimal(datas[key]['p_change']) < 0:
                datas[key]['p_mark'] = 0

            if Decimal(datas[key]['price_change']) > 0:
                datas[key]['price_change'] = '+' + str(datas[key]['price_change'])
                datas[key]['price_mark'] = 1

            if  Decimal(datas[key]['price_change']) < 0:
                datas[key]['price_mark'] = 0

        print('*'*100)
        for data in datas:
            print(data)

        conditions = {
            'date': date,
            'p_change': p_change,
            'price_change': price_change,
            'volume': volume
        }
        context = {
            'cateId': cateId,
            'datas': datas,
            'num': num,
            'conditions': conditions
        }

        return render(request, 'statistics.html', context=context)

def searchResult(request):
    isLogin = request.session.get('loginStatus')
    if isLogin is not True:
        return render(request, 'login.html')
    else:
        search_content = request.POST.get('search')
        cateId = request.GET.get('cateid')
        print(search_content, search_content == '')
        if search_content == '':
            search_result = 0
            datas = []
            num = 0
        else:
            search_result = 1
            datas = ss.objects.filter(Q(share_name__contains=search_content)|Q(code__contains=search_content)).values()
            print(datas)
            for key, data in enumerate(datas):
                others = sd.objects.filter(Q(date='2020-04-02')&Q(sort_id=data['id'])).values()
                print(others)
                datas[key]['data_id'] = others[0]['id']

            num = len(datas)
            print('num: ', num)

        context = {
            'cateId': cateId,
            'datas': datas,
            'num': num,
            'search_result': search_result,
            'search_content': search_content
        }

        return render(request, 'searchResult.html', context=context)

def page_ajax(request):
    if request.is_ajax():
        data = json.loads(request.body)
        page = int(data['page'])
        date = data['now_date']
        p_change = int(data['now_p_change'])
        price_change = int(data['now_price_change'])
        volume = int(data['now_volume'])


        datas = sd.objects.filter(date=date)

        if p_change == 1:
            datas = datas.order_by('p_change')
            print('*^'*100)
        if p_change == 2:
            datas = datas.order_by('-p_change')

        if price_change == 1:
            datas = datas.order_by('price_change')
        if price_change == 2:
            datas = datas.order_by('-price_change')

        if volume == 1:
            datas = datas.order_by('volume')
        if volume == 2:
            datas = datas.order_by('-volume')

        datas = datas.values()[10*(page - 1):10 * page]

        print(datas)
        for key,data in enumerate(datas):
            other_data = ss.objects.filter(id=data['sort_id']).values()
            datas[key]['name'] = other_data[0]['share_name']
            datas[key]['code'] = other_data[0]['code']
            if Decimal(datas[key]['p_change']) > 0:
                datas[key]['p_change'] = '+' + str(datas[key]['p_change'])
                datas[key]['p_mark'] = 1
            if Decimal(datas[key]['p_change']) < 0:
                datas[key]['p_mark'] = 0

            if Decimal(datas[key]['price_change']) > 0:
                datas[key]['price_change'] = '+' + str(datas[key]['price_change'])
                datas[key]['price_mark'] = 1

            if  Decimal(datas[key]['price_change']) < 0:
                datas[key]['price_mark'] = 0
        datas = list(datas)
        context = {
            'datas': datas,
        }
        return JsonResponse(context, safe=False)

def plot_normal(request):
    isLogin = request.session.get('loginStatus')
    if isLogin is not True:
        return render(request, 'login.html')
    else:
        cateId = request.GET.get('cateid', 3)
    context = {
        'cateId': cateId,
    }
    return render(request, 'plot.html', context=context)

def plot(request):
    isLogin = request.session.get('loginStatus')
    if isLogin is not True:
        return render(request, 'login.html')
    else:
        cateId = request.GET.get('cateid', 3)
        k_mark = int(request.GET.get('k_mark', 1))
        buy_mark = int(request.GET.get('buy_mark', -1))
        sell_mark = int(request.GET.get('sell_mark', -1))
        now_date = request.GET.get('date', '2020-04-01')
        real_datas = []
        yes_datas = []

        date = datetime.strptime(now_date, '%Y-%m-%d')
        yes_date = date + timedelta(days=-1)
        print(k_mark, buy_mark, sell_mark, date, yes_date)

        datas = sd.objects.filter(date=date).order_by('sort_id')
        while len(datas) == 0:
            date = date + timedelta(days=1)
            datas = sd.objects.filter(date=date).order_by('sort_id')

        datas = list(datas.values())
        print(len(datas), len(sd.objects.filter(date=yes_date).order_by('sort_id').values()))
        for key, data in enumerate(datas):
            temp = sd.objects.filter(Q(date__lte=yes_date) & Q(sort_id=datas[key]['sort_id'])).order_by('-date')
            print(len(temp))
            if temp.exists():
                print('*&*&*&*&*', temp.values()[0])
                yes_datas.append(temp.values()[0])
            else:
                print('shanchu'*20)
                datas.remove(datas[key])
                pass

        print(len(datas), len(yes_datas))

        all_buy_marks = [[1.0, 1.2], [1.2, 1.5], [1.5, 2.0], [2.0, 1000]]

        if k_mark == 1:
            for key, data in enumerate(datas):
                if yes_datas[key]['ma5'] <= yes_datas[key]['ma10'] and datas[key]['ma5'] >= datas[key]['ma10']:
                    print('可买入1', yes_datas[key]['ma5'], yes_datas[key]['ma10'], datas[key]['ma5'], datas[key]['ma10'])
                    real_datas.append(data)
                else:
                    if buy_mark != -1:
                        if datas[key]['volume'] >= all_buy_marks[buy_mark][0] * yes_datas[key]['volume'] and datas[key]['volume'] <= all_buy_marks[buy_mark][1] * yes_datas[key]['volume']:
                            print('可买入2', datas[key]['volume'], all_buy_marks[buy_mark][0] * yes_datas[key]['volume'], all_buy_marks[buy_mark][1] * yes_datas[key]['volume'])
                            real_datas.append(data)
                    else:
                        pass

        elif k_mark == 2:
            for key, data in enumerate(datas):
                if yes_datas[key]['ma10'] <= yes_datas[key]['ma20'] and datas[key]['ma10'] >= datas[key]['ma20']:
                    print('可买入1', yes_datas[key]['ma10'], yes_datas[key]['ma20'], datas[key]['ma10'], datas[key]['ma20'])
                    real_datas.append(data)
                else:
                    if buy_mark != -1:
                        if datas[key]['volume'] >= all_buy_marks[buy_mark][0] * yes_datas[key]['volume'] and datas[key]['volume'] <= all_buy_marks[buy_mark][1] * yes_datas[key]['volume']:
                            print('可买入2', datas[key]['volume'], all_buy_marks[buy_mark][0] * yes_datas[key]['volume'], all_buy_marks[buy_mark][1] * yes_datas[key]['volume'])
                            real_datas.append(data)
                    else:
                        pass

        elif k_mark == 3:
            for key, data in enumerate(datas):
                if yes_datas[key]['ma5'] <= yes_datas[key]['ma20'] and datas[key]['ma5'] >= datas[key]['ma20']:
                    print('可买入1', yes_datas[key]['ma5'], yes_datas[key]['ma20'], datas[key]['ma5'], datas[key]['ma20'])
                    real_datas.append(data)
                else:
                    if buy_mark != -1:
                        if datas[key]['volume'] >= all_buy_marks[buy_mark][0] * yes_datas[key]['volume'] and datas[key]['volume'] <= all_buy_marks[buy_mark][1] * yes_datas[key]['volume']:
                            print('可买入2', datas[key]['volume'], all_buy_marks[buy_mark][0] * yes_datas[key]['volume'], all_buy_marks[buy_mark][1] * yes_datas[key]['volume'])
                            real_datas.append(data)
                    else:
                        pass

        else:
            print('2222'*10)
            for key, data in enumerate(datas):
                if datas[key]['volume'] >= all_buy_marks[buy_mark][0] * yes_datas[key]['volume'] and datas[key]['volume'] <= \
                        all_buy_marks[buy_mark][1] * yes_datas[key]['volume']:
                    print('可买入22', datas[key]['volume'], all_buy_marks[buy_mark][0] * yes_datas[key]['volume'],
                          all_buy_marks[buy_mark][1] * yes_datas[key]['volume'])
                    real_datas.append(data)


        print(len(datas), len(real_datas))
        datas = copy.deepcopy(real_datas)

        for key, data in enumerate(datas):
            other_data = ss.objects.filter(id=data['sort_id']).values()
            datas[key]['name'] = other_data[0]['share_name']
            datas[key]['code'] = other_data[0]['code']
            datas[key]['date'] = datas[key]['date'].strftime("%Y-%m-%d")

            if Decimal(datas[key]['p_change']) > 0:
                datas[key]['p_change'] = '+' + str(datas[key]['p_change'])
                datas[key]['p_mark'] = 1
            if Decimal(datas[key]['p_change']) < 0:
                datas[key]['p_mark'] = 0

            if Decimal(datas[key]['price_change']) > 0:
                datas[key]['price_change'] = '+' + str(datas[key]['price_change'])
                datas[key]['price_mark'] = 1

            if Decimal(datas[key]['price_change']) < 0:
                datas[key]['price_mark'] = 0

        print('*' * 100)
        for data in datas:
            print(data)

        context = {
            'cateId': cateId,
            'k_mark': k_mark,
            'buy_mark': buy_mark,
            'sell_mark': sell_mark,
            'date': now_date,
            'datas': datas
        }
        return render(request, 'plot.html', context=context)

def charts(request):
    isLogin = request.session.get('loginStatus')
    if isLogin is not True:
        return render(request, 'login.html')
    else:
        cateId = request.GET.get('cateid')
        datas = ss.objects.all()

        context = {
            'cateId': cateId,
            'datas': datas
        }
        return render(request, 'charts.html', context=context)


def aboutUs(request):
    isLogin = request.session.get('loginStatus')
    if isLogin is not True:
        return render(request, 'login.html')
    else:
        cateId = request.GET.get('cateid')

        context = {
            'cateId': cateId,
        }
        return render(request, 'aboutUs.html', context=context)

def login(request):
    return render(request, 'login.html')

def handleLogin(request):
    if request.is_ajax():
        data = json.loads(request.body)
        account = data['account']
        password = data['password']
        if account == 'root' and password == 'password':
            loginStatus = 1
            request.session['loginStatus'] = True
        else:
            loginStatus = 0
        context = {
            'cateId': 1,
            'loginStatus': loginStatus
        }
        return JsonResponse(context, safe=False)

def handleLoginOut(request):
    if request.is_ajax():
        data = json.loads(request.body)
        status = data['loginOut']
        print('loginOut')
        if status == 1:
            loginOutStatus = 1
            request.session.delete()
        else:
            loginOutStatus = 0
        context = {
            'cateId': 1,
            'loginOutStatus': loginOutStatus
        }
        return JsonResponse(context, safe=False)


def detail(request):
    isLogin = request.session.get('loginStatus')
    if isLogin is not True:
        return render(request, 'login.html')
    else:
        id = int(request.GET.get('id'))
        print('*'*50, id)

        datas = sd.objects.filter(pk=id).values()[0]
        datas['date'] = datas['date'].strftime("%Y-%m-%d")
        print(datas)

        other_data = ss.objects.filter(id=datas['sort_id']).values()
        datas['name'] = other_data[0]['share_name']
        datas['code'] = other_data[0]['code']
        datas['key_id'] = other_data[0]['id']
        if Decimal(datas['p_change']) > 0:
            datas['p_change'] = '+' + str(datas['p_change'])
            datas['p_mark'] = 1
        if Decimal(datas['p_change']) < 0:
            datas['p_mark'] = 0

        if Decimal(datas['price_change']) > 0:
            datas['price_change'] = '+' + str(datas['price_change'])
            datas['price_mark'] = 1

        if Decimal(datas['price_change']) < 0:
            datas['price_mark'] = 0

        print(datas)
        key_id = other_data[0]['id']
        month = int(request.GET.get('month', 3))
        year = int(request.GET.get('year', 2020))
        if month // 10 == 0:
            str_date = str(year) + '-0' + str(month)
        else:
            str_date = str(year) + '-' + str(month)
        graph_datas = sd.objects.filter(sort_id=key_id).filter(date__contains=str_date).order_by('date').values()
        ma5_datas = []
        ma10_datas = []
        ma20_datas = []
        print(graph_datas)
        max_val = graph_datas[0]['ma5']
        min_val = graph_datas[0]['ma5']
        for key,data in enumerate(graph_datas):
            print(data['date'], data['ma5'], data['ma10'], data['ma20'])
            print(type(data['date']))

            graph_datas[key]['date'] = graph_datas[key]['date'].strftime('%Y-%m-%d')
            time_rel = time.mktime(time.strptime(data['date'], '%Y-%m-%d'))
            time_rel = time_rel * 1000
            print(time_rel)
            ma5_datas.append([time_rel, data['ma5']])
            ma10_datas.append([time_rel, data['ma10']])
            ma20_datas.append([time_rel, data['ma20']])
            if max_val < Decimal(data['ma5']):
                max_val = data['ma5']
            if max_val < Decimal(data['ma10']):
                max_val = data['ma10']
            if max_val < Decimal(data['ma20']):
                max_val = data['ma20']

            if min_val > Decimal(data['ma5']):
                min_val = data['ma5']
            if min_val >  Decimal(data['ma10']):
                min_val = data['ma10']
            if min_val >  Decimal(data['ma20']):
                min_val = data['ma20']

        message = {'name': datas['name'],
                   'code': datas['code'],
                   'year': year,
                   'month': month,
                   'max_val': max_val,
                   'min_val': min_val}
        print('**'* 30, message)

        year_2019 = [4, 5, 6, 7, 8, 9, 10, 11, 12]
        year_2020 = [1, 2, 3, 4]
        context = {
            'cateId': 2,
            'datas': datas,
            'ma5_datas': json.dumps(ma5_datas, cls=DecimalEncoder),
            'ma10_datas': json.dumps(ma10_datas, cls=DecimalEncoder),
            'ma20_datas': json.dumps(ma20_datas, cls=DecimalEncoder),
            'message': message,
            'year_2019': year_2019,
            'year_2020': year_2020
        }
        return render(request, 'detail.html', context=context)


def calculation(request):
    test_name = request.POST.get('test_name')
    share_id = request.POST.get('share_id')
    money = float(request.POST.get('spend_money'))
    mode = int(request.POST.get('mode'))
    start_time = request.POST.get('start_time')
    time_length = int(request.POST.get('time_length'))

    money = money * 100000
    year = int(start_time[:4])
    month = int(start_time[5:7])
    day = int(start_time[-2:])

    end_year = year
    end_day = day
    end_month = month + time_length
    if end_month > 12:
        end_month -= 12
        end_year += 1

    print(year, month, day, end_year, end_month, end_day)

    start_time = make_aware(datetime(year=year, month=month, day=day))
    end_time = make_aware(datetime(year=end_year, month=end_month, day=end_day))
    # end_time = str(year) + '-' + str(month) + '-' + str(day)

    share_status = ss.objects.get(id=share_id)
    datas = sd.objects.filter(Q(sort_id=share_id)&Q(date__range=(start_time, end_time))).order_by('date').values()
    # for data in datas:
    #     print(data['date'], type(data['date']), type(datetime.now()), data['date'] + timedelta(days=1))

    buy_datas = []
    buy_flag = 0
    now_money = money
    max = money
    min = money

    print(test_name, share_id, money, mode, start_time, time_length)
    if mode == 1:
        for key, data in enumerate(datas):
            if key != len(datas) - 1:
                print('*'*50)
                if datas[key]['ma5'] >= datas[key]['ma10'] and datas[key+1]['ma5'] <= datas[key+1]['ma10']:
                    print(data['date'], datas[key]['ma5'], datas[key]['ma10'], datas[key+1]['ma5'], datas[key+1]['ma10'])
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change'] / 100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_flag = 0
                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d'))*1000
                                         , int(now_money)])
                    # buy_datas.append({
                    #     'date': data['date'],
                    #     'now_money': now_money,
                    #     'buy_status': 2,
                    #     'p_change': 1 + datas[key - 1]['p_change']/100
                    # })

                elif datas[key]['ma5'] <= datas[key]['ma10'] and datas[key+1]['ma5'] >= datas[key+1]['ma10']:
                    print(data['date'], datas[key]['ma5'], datas[key]['ma10'], datas[key+1]['ma5'], datas[key+1]['ma10'])
                    buy_flag = 1
                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])
                else:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change']/100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])

    if mode == 2:
        for key, data in enumerate(datas):
            if key != len(datas) - 1:
                print('*'*50)
                if datas[key]['ma10'] >= datas[key]['ma20'] and datas[key+1]['ma10'] <= datas[key+1]['ma20']:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change'] / 100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_flag = 0
                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d'))*1000
                                         , int(now_money)])

                elif datas[key]['ma10'] <= datas[key]['ma20'] and datas[key+1]['ma10'] >= datas[key+1]['ma20']:
                    buy_flag = 1

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])
                else:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change']/100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])

    if mode == 3:
        for key, data in enumerate(datas):

            if key != len(datas) - 1:
                print('*'*50)
                if datas[key]['ma5'] >= datas[key]['ma20'] and datas[key+1]['ma5'] <= datas[key+1]['ma20']:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change'] / 100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_flag = 0
                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d'))*1000
                                         , int(now_money)])

                elif datas[key]['ma5'] <= datas[key]['ma20'] and datas[key+1]['ma5'] >= datas[key+1]['ma20']:
                    buy_flag = 1
                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])
                else:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change']/100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])


    for data in buy_datas:
        print(data)

    print(buy_datas[-1], '*' * 10, min, max)
    end_money = buy_datas[-1][1]


    context = {
        'cateId': 4,
        'test_name': test_name,
        'share_id': share_id,
        'start_money': int(money),
        'end_money': end_money,
        'mode': mode,
        'start_time': start_time.strftime('%Y-%m-%d'),
        'end_time': end_time.strftime('%Y-%m-%d'),
        'time_length': time_length,
        'share_status': share_status,
        'buy_datas': buy_datas,
        'min': int(min) - 100,
        'max': int(max) + 100,
    }
    return render(request, 'calculation.html', context=context)


def calculation_mode2(request):
    test_name = request.POST.get('test_name')
    share_id = request.POST.get('share_id')
    money = float(request.POST.get('spend_money'))
    buy_mark = int(request.POST.get('buy_mark')) - 1
    sell_mark = int(request.POST.get('sell_mark')) - 1
    start_time = request.POST.get('start_time')
    time_length = int(request.POST.get('time_length'))

    all_buy_marks = [[1.0, 1.2], [1.2, 1.5], [1.5, 2.0], [2.0]]
    all_sell_marks = [[0.0, 0.2], [0.2, 0.5], [0.5, 1.0]]

    print(test_name, share_id, money, buy_mark, sell_mark, start_time, time_length)
    money = money * 100000
    year = int(start_time[:4])
    month = int(start_time[5:7])
    day = int(start_time[-2:])

    end_year = year
    end_day = day
    end_month = month + time_length
    if end_month > 12:
        end_month -= 12
        end_year += 1

    print(year, month, day, end_year, end_month, end_day)

    start_time = make_aware(datetime(year=year, month=month, day=day))
    end_time = make_aware(datetime(year=end_year, month=end_month, day=end_day))
    # end_time = str(year) + '-' + str(month) + '-' + str(day)

    share_status = ss.objects.get(id=share_id)
    datas = sd.objects.filter(Q(sort_id=share_id)&Q(date__range=(start_time, end_time))).order_by('date').values()
    for data in datas:
        print(data['volume'])

    buy_datas = []
    buy_flag = 0
    now_money = money
    max = money
    min = money

    print(test_name, share_id, money, buy_mark, sell_mark, start_time, time_length)
    if buy_mark != 3:
        for key, data in enumerate(datas):
            if key != len(datas) - 1:
                print('*'*50)
                if datas[key + 1]['volume'] >= all_sell_marks[sell_mark][0] * datas[key]['volume'] \
                        and datas[key+1]['volume'] <= all_sell_marks[sell_mark][1] * datas[key]['volume']:
                    print('卖出', datas[key + 1]['volume'], all_sell_marks[sell_mark][0], datas[key]['volume'], all_sell_marks[sell_mark][1] * datas[key]['volume'],
                          datas[key+1]['volume'],all_sell_marks[sell_mark][1], datas[key]['volume'], all_sell_marks[sell_mark][1] * datas[key]['volume'])
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change'] / 100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_flag = 0
                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d'))*1000
                                         , int(now_money)])


                elif datas[key + 1]['volume'] >= all_buy_marks[buy_mark][0] * datas[key]['volume'] \
                        and datas[key+1]['volume'] <= all_buy_marks[buy_mark][1] * datas[key]['volume']:
                    print('买入', datas[key + 1]['volume'], all_buy_marks[buy_mark][0], all_buy_marks[buy_mark][1] * datas[key]['volume'],
                          datas[key+1]['volume'],all_buy_marks[buy_mark][1], all_buy_marks[buy_mark][1] * datas[key]['volume'])
                    buy_flag = 1
                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])
                else:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change']/100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])

    if buy_mark == 3:
        for key, data in enumerate(datas):
            if key != len(datas) - 1:
                print('*' * 50)
                if datas[key + 1]['volume'] >= all_sell_marks[sell_mark][0] * datas[key]['volume'] \
                        and datas[key + 1]['volume'] <= all_sell_marks[sell_mark][1] * datas[key]['volume']:
                    print('卖出', datas[key + 1]['volume'], all_sell_marks[sell_mark][0], datas[key]['volume'],
                          all_sell_marks[sell_mark][1] * datas[key]['volume'],
                          datas[key + 1]['volume'], all_sell_marks[sell_mark][1], datas[key]['volume'],
                          all_sell_marks[sell_mark][1] * datas[key]['volume'])
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change'] / 100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_flag = 0
                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])


                elif datas[key + 1]['volume'] >= all_buy_marks[buy_mark][0] * datas[key]['volume']:
                    print('买入', datas[key + 1]['volume'], all_buy_marks[buy_mark][0],
                          all_buy_marks[buy_mark][0] * datas[key]['volume'], datas[key]['volume']
                          )
                    buy_flag = 1
                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])
                else:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change'] / 100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])


    for data in buy_datas:
        print(data)

    print(buy_datas[-1], '*' * 10, min, max)
    end_money = buy_datas[-1][1]


    context = {
        'cateId': 4,
        'test_name': test_name,
        'share_id': share_id,
        'start_money': int(money),
        'end_money': end_money,
        'sell_mark': sell_mark,
        'buy_mark': buy_mark,
        'start_time': start_time.strftime('%Y-%m-%d'),
        'end_time': end_time.strftime('%Y-%m-%d'),
        'time_length': time_length,
        'share_status': share_status,
        'buy_datas': buy_datas,
        'min': int(min) - 100,
        'max': int(max) + 100,
    }
    return render(request, 'calculation_mode2.html', context=context)


def calculation_mode3(request):
    test_name = request.POST.get('test_name')
    share_id = request.POST.get('share_id')
    money = float(request.POST.get('spend_money'))
    k_mark = int(request.POST.get('k_mark'))
    buy_mark = int(request.POST.get('buy_mark')) - 1
    sell_mark = int(request.POST.get('sell_mark')) - 1
    start_time = request.POST.get('start_time')
    time_length = int(request.POST.get('time_length'))

    all_buy_marks = [[1.0, 1.2], [1.2, 1.5], [1.5, 2.0], [2.0, 1000]]
    all_sell_marks = [[0.0, 0.2], [0.2, 0.5], [0.5, 1.0]]

    money = money * 100000
    print(test_name, share_id, money, buy_mark, sell_mark, start_time, time_length, k_mark)
    year = int(start_time[:4])
    month = int(start_time[5:7])
    day = int(start_time[-2:])

    end_year = year
    end_day = day
    end_month = month + time_length
    if end_month > 12:
        end_month -= 12
        end_year += 1

    print(year, month, day, end_year, end_month, end_day)

    start_time = make_aware(datetime(year=year, month=month, day=day))
    end_time = make_aware(datetime(year=end_year, month=end_month, day=end_day))
    # end_time = str(year) + '-' + str(month) + '-' + str(day)

    share_status = ss.objects.get(id=share_id)
    datas = sd.objects.filter(Q(sort_id=share_id)&Q(date__range=(start_time, end_time))).order_by('date').values()
    for data in datas:
        print(data['volume'])

    buy_datas = []
    buy_flag = 0
    now_money = money
    max = money
    min = money

    print(test_name, share_id, money, buy_mark, sell_mark, start_time, time_length)
    if k_mark == 1:
        for key, data in enumerate(datas):
            if key != len(datas) - 1:
                print('*'*50)
                if (datas[key + 1]['volume'] >= all_sell_marks[sell_mark][0] * datas[key]['volume']
                    and datas[key+1]['volume'] <= all_sell_marks[sell_mark][1] * datas[key]['volume'] ) \
                        or(datas[key]['ma5'] >= datas[key]['ma10'] and datas[key+1]['ma5'] <= datas[key+1]['ma10']):

                    print('卖出', data['date'], datas[key]['ma5'], datas[key]['ma10'], datas[key + 1]['ma5'],
                          datas[key + 1]['ma10'])
                    print('卖出', datas[key + 1]['volume'], all_sell_marks[sell_mark][0], all_sell_marks[sell_mark][0] * datas[key]['volume'],
                          all_sell_marks[sell_mark][1], all_sell_marks[sell_mark][1] * datas[key]['volume'])
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change'] / 100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_flag = 0
                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d'))*1000
                                         , int(now_money)])


                elif (datas[key + 1]['volume'] >= all_buy_marks[buy_mark][0] * datas[key]['volume']
                        and datas[key+1]['volume'] <= all_buy_marks[buy_mark][1] * datas[key]['volume']) \
                        or (datas[key]['ma5'] <= datas[key]['ma10'] and datas[key+1]['ma5'] >= datas[key+1]['ma10']):

                    print('买入', data['date'], datas[key]['ma5'], datas[key]['ma10'], datas[key + 1]['ma5'],
                          datas[key + 1]['ma10'])
                    print('买入', datas[key + 1]['volume'], all_buy_marks[buy_mark][0], all_buy_marks[buy_mark][0] * datas[key]['volume'],
                          all_buy_marks[buy_mark][1], all_buy_marks[buy_mark][1] * datas[key]['volume'])
                    buy_flag = 1
                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])

                else:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change']/100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])

    if k_mark == 2:
        for key, data in enumerate(datas):
            if key != len(datas) - 1:
                print('*'*50)
                if (datas[key + 1]['volume'] >= all_sell_marks[sell_mark][0] * datas[key]['volume']
                    and datas[key+1]['volume'] <= all_sell_marks[sell_mark][1] * datas[key]['volume'] ) \
                        or(datas[key]['ma10'] >= datas[key]['ma20'] and datas[key+1]['ma10'] <= datas[key+1]['ma20']):

                    print('卖出', data['date'], datas[key]['ma10'], datas[key]['ma20'], datas[key + 1]['ma10'],
                          datas[key + 1]['ma20'])
                    print('卖出', datas[key + 1]['volume'], all_sell_marks[sell_mark][0], all_sell_marks[sell_mark][0] * datas[key]['volume'],
                          all_sell_marks[sell_mark][1], all_sell_marks[sell_mark][1] * datas[key]['volume'])
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change'] / 100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_flag = 0
                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d'))*1000
                                         , int(now_money)])


                elif (datas[key + 1]['volume'] >= all_buy_marks[buy_mark][0] * datas[key]['volume']
                        and datas[key+1]['volume'] <= all_buy_marks[buy_mark][1] * datas[key]['volume']) \
                        or (datas[key]['ma10'] <= datas[key]['ma20'] and datas[key+1]['ma10'] >= datas[key+1]['ma20']):

                    print('买入', data['date'], datas[key]['ma10'], datas[key]['ma20'], datas[key + 1]['ma10'],
                          datas[key + 1]['ma20'])
                    print('买入', datas[key + 1]['volume'], all_buy_marks[buy_mark][0], all_buy_marks[buy_mark][0] * datas[key]['volume'],
                          all_buy_marks[buy_mark][1], all_buy_marks[buy_mark][1] * datas[key]['volume'])
                    buy_flag = 1
                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])

                else:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change']/100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])

    if k_mark == 3:
        for key, data in enumerate(datas):
            if key != len(datas) - 1:
                print('*'*50)
                if (datas[key + 1]['volume'] >= all_sell_marks[sell_mark][0] * datas[key]['volume']
                    and datas[key+1]['volume'] <= all_sell_marks[sell_mark][1] * datas[key]['volume'] ) \
                        or(datas[key]['ma5'] >= datas[key]['ma20'] and datas[key+1]['ma5'] <= datas[key+1]['ma20']):

                    print('卖出', data['date'], datas[key]['ma5'], datas[key]['ma20'], datas[key + 1]['ma5'],
                          datas[key + 1]['ma20'])
                    print('卖出', datas[key + 1]['volume'], all_sell_marks[sell_mark][0], all_sell_marks[sell_mark][0] * datas[key]['volume'],
                          all_sell_marks[sell_mark][1], all_sell_marks[sell_mark][1] * datas[key]['volume'])
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change'] / 100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_flag = 0
                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d'))*1000
                                         , int(now_money)])


                elif (datas[key + 1]['volume'] >= all_buy_marks[buy_mark][0] * datas[key]['volume']
                        and datas[key+1]['volume'] <= all_buy_marks[buy_mark][1] * datas[key]['volume']) \
                        or (datas[key]['ma5'] <= datas[key]['ma20'] and datas[key+1]['ma5'] >= datas[key+1]['ma20']):

                    print('买入', data['date'], datas[key]['ma5'], datas[key]['ma20'], datas[key + 1]['ma5'],
                          datas[key + 1]['ma20'])
                    print('买入', datas[key + 1]['volume'], all_buy_marks[buy_mark][0], all_buy_marks[buy_mark][0] * datas[key]['volume'],
                          all_buy_marks[buy_mark][1], all_buy_marks[buy_mark][1] * datas[key]['volume'])
                    buy_flag = 1
                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])

                else:
                    if buy_flag == 1:
                        now_money = now_money * (1 + datas[key - 1]['p_change']/100)

                    if max < now_money:
                        max = now_money
                    if min > now_money:
                        min = now_money

                    buy_datas.append([time.mktime(time.strptime(data['date'].strftime('%Y-%m-%d'), '%Y-%m-%d')) * 1000
                                         , int(now_money)])


    for data in buy_datas:
        print(data)

    print(buy_datas[-1], '*' * 10, min, max)
    end_money = buy_datas[-1][1]


    context = {
        'cateId': 4,
        'test_name': test_name,
        'share_id': share_id,
        'start_money': int(money),
        'end_money': end_money,
        'sell_mark': sell_mark,
        'k_mark': k_mark,
        'buy_mark': buy_mark,
        'start_time': start_time.strftime('%Y-%m-%d'),
        'end_time': end_time.strftime('%Y-%m-%d'),
        'time_length': time_length,
        'share_status': share_status,
        'buy_datas': buy_datas,
        'min': int(min) - 100,
        'max': int(max) + 100,
    }
    return render(request, 'calculation_mode3.html', context=context)
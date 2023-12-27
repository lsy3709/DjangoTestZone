from django.http import HttpResponse
from django.shortcuts import render
from burgers.models import Burger

def main(request):
    # return HttpResponse("hi, main 입니다.")
    return render(request, 'main.html')

def burger_list(request):
    # return HttpResponse("pyburger 햄버거 목록")
    burgers = Burger.objects.all()

    print("전체 햄버거 목록: ", burgers)

    context = {
        "burgers": burgers,
    }

    return render(request, 'burger_list.html', context)

def burger_search(request):
    # print(request.GET)
    keyword = request.GET.get('keyword')
    print(keyword)
    burgers = Burger.objects.filter(name__contains=keyword)
    print(burgers)
    return render(request, 'burger_search.html')

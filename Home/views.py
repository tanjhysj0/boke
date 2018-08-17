# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from Article.models import Article
from Article.models import Column
import re
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# import pdb;pdb.set_trace()
import datetime
import time
def index(request):


    try:
        list = Article.objects.all()[0:100]
        paginator = Paginator(list, 10)
        page = request.GET.get('page')

        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)


    return render(request,"index.html",{'list':contacts,'paginator':paginator})
def list(request,column_id):
    if(re.match(r"^(\d+)-(\d+)-(\d+)$",column_id)):
        # return HttpResponse("date")
        imeArray = time.strptime(column_id,"%Y-%m-%d")

        year = int(time.strftime("%Y",imeArray))
        month = int(time.strftime("%m",imeArray))
        day = int(time.strftime("%d",imeArray))
        date_from = datetime.datetime(year, month, day, 0, 0, 0)
        date_to = datetime.datetime(year,month,day, 23, 59, 59)

        list = Article.objects.filter(pub_date__range=(date_from, date_to))
    else:
        # return HttpResponse('no date')
        list = Article.objects.filter(column=column_id)

    paginator = Paginator(list, 10)
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "list.html", {'list': contacts, 'paginator': paginator})




def show(request,id):
    one = Article.objects.get(id=id)

    return render(request,"show.html",{'one':one})


from django.conf import settings as original_settings
from Article.models import Column
from collections import defaultdict
from django.db import connection
from django.db.models import Count
from Article.models import Article
def column(request):
    list_column = Column.objects.all()
    return {'list_column':list_column}

def right(request):
    #Archives
    select = {'day':connection.ops.date_trunc_sql('day','pub_date')}
    result = Article.objects.extra(select=select).values("day").annotate(number=Count('id'))
    #recent posts
    list_recent = Article.objects.order_by("-pub_date")[0:5]

    return {'result':result,'list_recent':list_recent}
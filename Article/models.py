# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from DjangoUeditor.models import UEditorField

#Create your models here.
class Column(models.Model):
    class Meta:
        db_table = 'column'
    name = models.CharField('栏目名称',max_length=50)
    def __unicode__(self):
        return self.name

class Article(models.Model):
    class Meta:
        db_table = 'article'

    title = models.CharField('标题',max_length=256)
    column = models.ManyToManyField(Column,verbose_name='所属栏目')
    description = models.TextField(u'描述',blank=True)
    keywords = models.CharField(u'标签',max_length=255,blank=True)
    content = UEditorField(u'内容',width=600, height=300, toolbars="full", imagePath="", filePath="", upload_settings={"imageMaxSize":1204000},settings={},command=None,blank=True)
    transshipment = models.URLField(u'转载地址',blank=True)



    pub_date = models.DateTimeField('发表时间',auto_now_add=True,editable=True)
    update_time = models.DateTimeField('更新时间',auto_now=True,null=True)

    def __unicode__(self):  # 在Python3中用 __str__ 代替 __unicode__
        return self.title


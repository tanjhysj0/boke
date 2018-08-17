from django.contrib import admin

# Register your models here.
from .models import Column,Article
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','pub_date','update_time',)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Article,ArticleAdmin)
admin.site.register(Column,ColumnAdmin)
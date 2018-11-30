from django.contrib import admin
from .models import *


# 1.声明Author高级管理类

class AuthorAdmin(admin.ModelAdmin):
	# 1.定义显示在页面的字段
	list_display=('name','age','email')
	# 2.生成一个能够链接到具体页面的超链接,该值必须出现在list_display中
	list_display_links = ('name', 'email')
	# 3.生成一个允许被修改的字段列表
	list_editable = ('age',)
	# 4.生成一个允许被搜索的列表
	search_fields = ('name', 'email')
	# 5.生成一个过滤器
	list_filter = ('age', 'name')
	# 6.生成具体显示的字段列表
	#fields = ('name', 'age', 'email','picture')
	# 7.实现属性的分组
	# fieldsets = (
	# 	('基本设置', {'fields': ('name', 'age','publisher')}),
	# 	('高级设置', {
	# 		'fields': ('email', 'picture'),
	# 		'classes': ('collapse',)
	# 	})
	# )

# 2.声明Book高级管理类
class BookAdmin(admin.ModelAdmin):
	date_hierarchy = 'publication_date'

# 3.声明Publisher高级管理类
class PublisherAdmin(admin.ModelAdmin):
	# 1、在实体列表页上显示 name,address,city属性
	list_display = ('name', 'address', 'city')
	# 2、address和city是可以被编辑的
	list_editable = ('address', 'city')
	# 3、点击 name 时能够进入到实体详细页面中
	list_display_links = ('name',)
	# 4、右侧增加一个过滤器，允许按照address 和 city 进行筛选
	list_filter = ('address', 'city')
	# 5、分组显示
    #     name,address,city 为基本选项
    #     country,website 为可选选项，并可以折叠
	fieldsets = (
		('基本選項', {'fields': ('name', 'address', 'city')}),
		('可選選項', {
			'fields': ('country', 'website'),
			'classes': ('collapse',)
		})
	)



# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Wife)
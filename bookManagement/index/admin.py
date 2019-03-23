from django.contrib import admin
from .models import *




class AuthorAdmin(admin.ModelAdmin):
	
	list_display=('name','age','email')
	
	list_display_links = ('name', 'email')
	
	list_editable = ('age',)
	
	search_fields = ('name', 'email')
	
	list_filter = ('age', 'name')
	


class BookAdmin(admin.ModelAdmin):
	date_hierarchy = 'publication_date'


class PublisherAdmin(admin.ModelAdmin):
	
	list_display = ('name', 'address', 'city')
	
	list_editable = ('address', 'city')
	
	list_display_links = ('name',)
	
	list_filter = ('address', 'city')
	
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

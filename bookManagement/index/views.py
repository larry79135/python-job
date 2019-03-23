from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.db.models import F,Q

# Create your views here.


def parent_views(request):
	return render(request, 'parent.html')

def child_views(request):
	return render(request, 'child.html')

def add_author_views(request):
	
	Author.objects.create(name='王寶強', age=33, email='wangbaoqiang@green.com')

	
	obj = Author(name='賈乃亮', age=35, email='jianailiang@green.com')
	obj.save()
	
	
	dic = {
	 	'name': '陳羽凡',
	 	'age': 38,
	 	'email': 'chenyufan@green.com'
	}
	obj = Author(**dic)
	obj.save()
	return HttpResponse('Add OK')

def add_book_views(request):
	Book.objects.create(title='紅樓夢', publication_date='1995-12-12')
	obj = Book(title='西游记', publication_date='1982-10-12')
	obj.save()

	dic={
		'title':'三國演義',
		'publication_date': '1990-3-5'
	}
	book = Book(**dic)
	book.save()

	return HttpResponse('Add Book OK')

def add_publisher_views(request):
	Publisher.objects.create(name='中國人民出版社', address='五道口',
							city='北京', country='中國', website='http://www.renmin.com')	

	obj = Publisher(name='中國動畫片出版社', address='潘家園', city='北京',
                    country='中國', website='http://www.donghuapian.com')
	obj.save()

	dic = {
		'name': '中國文玩出版社',
		'address': '潘家園',
		'city': '北京',
		'country': '中國',
		'website': 'http://www.wenwan.com'
	}
	publisher = Publisher(**dic)
	publisher.save()

	return HttpResponse("Add Publisher OK")

def get_author_views(request):
	
	authors = Author.objects.all()
	
	authors = Author.objects.order_by('-age')
	return render(request,'show_authors.html',locals())



def filter_author_views(request):
	
	inner = Author.objects.filter(name='王寶強').values('age')
	authors=Author.objects.filter(age__gt = inner)
	return render(request,'query_authors.html',locals())


def author_list_views(request):
	authors = Author.objects.all()
	return render(request,'author_list.html',locals())

def del_user_views(request,uid):
	Author.objects.get(id=uid).delete()
	return HttpResponseRedirect('/author_list')

def update_author_views(request):
	
	

	
	Author.objects.all().update(age=50)

	
	return HttpResponseRedirect('/author_list/')
def doF_views(request):
	
	Author.objects.all().update(age=F('age') + 10) 
	return HttpResponseRedirect('/author_list') 

def doQ_views(request):
	authors=Author.objects.filter(Q(id=1)|Q(age__gte=35))
	return render(request,'q.html',locals())

def raw_views(request):
	sql="select * from index_author where email like '%%@green.com';"
	authors=Author.objects.raw(sql)
	return render(request, 'raw.html', locals())

def all_authors_views(request):
	authors=Author.objects.all()
	return render(request,'all_authors.html',locals())

def oto_views(request):
	
	w = Wife.objects.get(id=1)
	a = w.author

	
	au = Author.objects.get(name='陳羽凡')
	wi = au.wife
	return render(request,'oto.html',locals())

def otm_views(request):
	
	book =Book.objects.get(id=1)
	publisher =book.publisher
	
	pub=Publisher.objects.get(id=1)
	books= pub.book_set.all()
	return render(request,'otm.html',locals())


def mtm_views(request):
	
	author=Author.objects.get(id=1)
	pubList=author.publisher.all()
	
	pub = Publisher.objects.get(id=3)
	auList = pub.author_set.all()
	return render(request,'mtm.html',locals())

def book_author_views(request):
	
	book = Book.objects.get(id=3)
	auList = book.author.all()

	
	au = Author.objects.get(id=3)
	bookList = au.book_set.all()
	return HttpResponse("Query OK")

def name_count_views(request):
	count = Author.objects.name_count('寶強')
	authors = Author.objects.lt_age(33)
	return HttpResponse(count)

def title_count_views(request):
	count = Book.objects.title_count('紅樓夢')
	
	return HttpResponse(count)	

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
	#1.Entry.objects.create()插入数据
	Author.objects.create(name='王寶強', age=33, email='wangbaoqiang@green.com')

	#2.obj=Entry(xx='xx') obj.save()
	obj = Author(name='賈乃亮', age=35, email='jianailiang@green.com')
	obj.save()
	
	#3.使用字典完成对象的构建
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
		'name': '中国文玩出版社',
		'address': '潘家园',
		'city': '北京',
		'country': '中国',
		'website': 'http://www.wenwan.com'
	}
	publisher = Publisher(**dic)
	publisher.save()

	return HttpResponse("Add Publisher OK")

def get_author_views(request):
	#1.查询所有的信息
	authors = Author.objects.all()
	
	#2.查询所有行的name列的值
	# authors = Author.objects.all().values('name')
	

	#3.查询所有行的name,age的值
    #authors = Author.objects.all().values('name', 'age')

    # 4.查询id为3的作者的信息
	#auth = Author.objects.get(id=4,name='陳羽凡')
        
    # 5.查询 age 不是 35 的作者的信息
	#authors = Author.objects.exclude(age=35)
	
	# 6.查询所有信息并按照age降序排序
	authors = Author.objects.order_by('-age')
	return render(request,'show_authors.html',locals())


# 通过filter函数完成的查询操作
def filter_author_views(request):
	 # 1.查询id=1的作者的信息
	#authors=Author.objects.filter(id__exact=2)
	
	#2.查询 name 值中,包含羽字的作者的信息
	#authors = Author.objects.filter(name__contains='羽')
	
	# 3. 查询年龄大于王宝强的年龄的作者的信息
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
	# 1.获取单个实体对象
	#auth = Author.objects.get(id=3)
	# 2.修改实体对象的信息	
	#auth.name='Chen Yufan'
	#auth.email = 'yufan@happy.com'	
	# 3.将实体信息保存
	#auth.save()

	# 跳转到 author_list_views 以便实现模板的展现
	#return author_list_views(request)
	

	# 2.批量修改
	Author.objects.all().update(age=50)

	# 使用重定向的方式完成视图的跳转
	return HttpResponseRedirect('/author_list/')
def doF_views(request):
	# 将所有人的年龄+10岁
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
	# 1.通过Wife找Author
	w = Wife.objects.get(id=1)
	a = w.author

	# 2.反向查询,通过Author找Wife
	au = Author.objects.get(name='陳羽凡')
	wi = au.wife
	return render(request,'oto.html',locals())

def otm_views(request):
	# 1.正向查询:通过Book查询Publisher
	book =Book.objects.get(id=1)
	publisher =book.publisher
	# 2.反向查询:通过Publisher查询所有相关的Book
	pub=Publisher.objects.get(id=1)
	books= pub.book_set.all()
	return render(request,'otm.html',locals())


def mtm_views(request):
	# 1.通过 author 找 publisher们
	author=Author.objects.get(id=1)
	pubList=author.publisher.all()
	# 2.通过Publisher 找 Author 们
	pub = Publisher.objects.get(id=3)
	auList = pub.author_set.all()
	return render(request,'mtm.html',locals())

def book_author_views(request):
	# 通过 Book 查询 所有的 Author(正向查询)
	book = Book.objects.get(id=3)
	auList = book.author.all()

	# 通过 Author 查询 所有的 Book(反向查询)
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
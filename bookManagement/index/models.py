from django.db import models
import datetime


class AuthorManager(models.Manager):
	def name_count(self,keywords):
		return self.filter(name__contains=keywords).count()
	def lt_age(self, tar):
		return self.filter(age__lt=tar)

class BookManager(models.Manager):
	def title_count(self,keywords):
		return self.filter(title__contains=keywords).count()



# Create your models here.
# 实体类 : Publisher
# 对应到数据库中的一张表
# 该类中的每个属性,会对应到数据表中的每个字段


class Publisher(models.Model):
	name=models.CharField(max_length=30, default='匿名', verbose_name='名稱')
	address=models.CharField(max_length=60, verbose_name='地址')
	city=models.CharField(max_length=30, verbose_name='所在城市')
	country=models.CharField(max_length=30, verbose_name='國家')
	website = models.URLField(verbose_name='網址')

	def __str__(self):
		return self.name
	
	class Meta:
		db_table = 'publisher'
		verbose_name = '出版社'
		verbose_name_plural = verbose_name	
	


class Author(models.Model):
	objects=AuthorManager()
	name = models.CharField(max_length=30, verbose_name='姓名')
	age = models.IntegerField(verbose_name='年龄')
	email = models.EmailField(null=True, verbose_name='郵箱')
	picture= models.ImageField(null=True, upload_to='static/upload/usrimg',verbose_name='用戶頭像')
	# 创建多对多关系 Author(M):Publisher(N)
	publisher = models.ManyToManyField(Publisher, verbose_name='簽約出版社')



	def __str__(self):
		return self.name

	class Meta:
		db_table='author'
		verbose_name = '作者'
		verbose_name_plural = verbose_name
		ordering = ['-age', 'id']

class Book(models.Model):
	objects=BookManager()

	title = models.CharField(max_length=50, verbose_name='書名')
	publication_date = models.DateField(verbose_name='出版日期')
	# 增加 1:M 的映射 , 引用 Publisher
	publisher = models.ForeignKey(Publisher, null=True, verbose_name='出版社')
	# 多对多
	author = models.ManyToManyField(Author, verbose_name='作者')
	
	def __str__(self):
		return self.title
	
	class Meta:
		db_table = 'book'
		verbose_name = '圖書'
		verbose_name_plural = verbose_name
		ordering = ['-publication_date']	

class Wife(models.Model):
	name=models.CharField(max_length=30,verbose_name='姓名')
	age = models.IntegerField(verbose_name='年龄')
	# 增加一对一的关系映射(关联到Author)
	author = models.OneToOneField(Author,null=True, verbose_name='相公')

	def __str__(self):
		return self.name

	class Meta:
		db_table='wife'
		verbose_name='妻子'
		verbose_name_plural = verbose_name



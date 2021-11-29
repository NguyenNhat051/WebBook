from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.forms.models import modelformset_factory # Delete chill obj

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length = 100, unique=True)
	icon = models.FileField(upload_to = "category/")
	create_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.name

class Writer(models.Model):
	name = models.CharField(max_length = 100)
	about = models.TextField()
	pic = models.FileField(upload_to = "writer/")
	create_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.name

class Book(models.Model):
	writer = models.ForeignKey(Writer, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100)
	price = models.IntegerField()
	stock = models.IntegerField()
	coverpage = models.FileField(upload_to = "coverpage/")
	bookpage = models.FileField(upload_to = "bookpage/")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	star = models.IntegerField(default=0)
	totalrating = models.IntegerField(default=0)
	review_count = models.IntegerField(default=0)
	description = models.TextField()
	favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)

	def __str__(self):
	    return self.name

class Review(models.Model):
	customer = models.ForeignKey(User, on_delete = models.CASCADE)
	book = models.ForeignKey(Book, on_delete = models.CASCADE)
	review_star = models.IntegerField(default=0)
	review_text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
	    return self.customer

#new
class Order(models.Model):
	customer = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):
	book = models.ForeignKey(Book,on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def	get_total(self):
		total = self.book.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
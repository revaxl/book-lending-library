from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
import datetime
# Create your models here.


class Tags(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Tags"


class Book(models.Model):
	book_name = models.CharField(max_length=200)
	slug = models.CharField(max_length=255, unique=True)
	author_name = models.CharField(max_length=200)
	isbn = models.IntegerField(verbose_name='ISBN', unique=True)
	status = models.BooleanField(default=True)
	description = models.TextField(null=True, blank=True)
	tags = models.ManyToManyField(Tags)
	image = models.ImageField(
			null=True, 
			blank=True, 
			width_field="width_field", 
			height_field="height_field")	
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	created = models.DateField(auto_now_add=True)
	number_of_pages = models.IntegerField()
	publish_date = models.DateField()
	publish_place = models.CharField(max_length=200)
	edition = models.CharField(max_length=100)
	borrower = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)


	def __str__(self):
		return self.book_name

	def get_tags(self):
		tags = ','.join([tag.name for tag in self.tags.all()])
		return tags

	def get_absolute_url(self):
		return reverse("books:detail", kwargs={"id" : self.id})

	def get_instance(self):
		instance = self
		return instance

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.book_name)
    if new_slug is not None:
        slug = new_slug
    qs = Book.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_receiver, sender=Book)


class BookBorrow(models.Model):
	date_borrow_start = models.DateField()
	date_borrow_end = models.DateField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	note = models.TextField(blank=True, null=True)
	book_borrowed = models.ForeignKey(Book, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.date_borrow_start)


def pre_save_post_receiver2(sender, instance, *args, **kwargs):
	date_borrow_start = instance.date_borrow_start
	date_borrow_end = date_borrow_start + datetime.timedelta(days=21)

pre_save.connect(pre_save_post_receiver2, sender=BookBorrow)
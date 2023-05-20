from django.db import models


# Create your models here.
class Files(models.Model):
    url = models.TextField()
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    age = models.IntegerField(default=25)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Files"

class Temp_Data_Bulk_Create(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    age = models.IntegerField(default=25)
    created_at = models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    photo = models.FileField(upload_to='book_picture', blank=True, null=True)
    book_name = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(default=25)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

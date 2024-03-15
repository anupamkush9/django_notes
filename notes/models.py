from django.db import models
import hashlib

# Create your models here.
class Files(models.Model):
    url = models.TextField()
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    age = models.IntegerField(default=25)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def hash_id(self):
        # Create an instance of the SHA-256 hash object
        sha256_hash = hashlib.sha256()

        # Convert the entity_number and fileurl to bytes
        hash_data = f"{self.name}".encode('utf-8')

        # Update the hash object with the data
        sha256_hash.update(hash_data)

        # Get the hexadecimal representation of the hash digest
        hash_result = sha256_hash.hexdigest()

        return hash_result

    class Meta:
        verbose_name_plural = "Files"

    def str(self):
        return self.name

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


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Mobiles(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    class Meta:
        verbose_name = 'Mobile'
        verbose_name_plural = 'Mobiles'

    def __str__(self):
        return self.name

from django.db import models
from django.db import models, transaction

# Create your models here.
class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    score = models.DecimalField(max_digits=10,decimal_places=3)

    def __str__(self):
        return self.id+self.name+self.score

class Customer(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    balance = models.DecimalField(max_digits=8, decimal_places=2)

class Purchase(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # def process_purchase(self):
    #     with transaction.atomic():
    #         self.customer.balance -= self.price
    #         self.customer.save()
    #         # Simulate an error by raising an exception
    #         raise Exception('Something went wrong')
    #         self.save()

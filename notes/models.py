from django.db import models


# Create your models here.
class Files(models.Model):
    url = models.TextField()
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    age = models.IntegerField(default=25)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Files"

# Create your models here.
class Temp_Data_Bulk_Create(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    age = models.IntegerField(default=25)
    created_at = models.DateTimeField(auto_now_add=True)




from django.db import models

# Create your models here.
class Tokens(models.Model):
    token = models.CharField(max_length=250)
    public_key = models.CharField(max_length=250)
    ceated_date = models.DateField()
    user_id = models.IntegerField()
    def __str__(self):
        return self.ceated_date

class Restaurants(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    adress = models.TextField()
    lng = models.TextField()
    lat = models.TextField()

# if need add custom field to default django users model
# class Users(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
    
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class NewUser(AbstractUser):
    class Meta:
        db_table='newuser'
        ordering=["-id"]


class Role(models.Model):
    name=models.CharField(max_length=128)
    relationship=models.ManyToManyField(to=settings.AUTH_USER_MODEL,related_name='role_user')
    relationpermiss=models.ManyToManyField(to='Permission',related_name='role_permiss')
    class Meta:
        db_table='role'


class Menu(models.Model):
    name=models.CharField(max_length=128)
    order=models.IntegerField()
    class Meta:
        db_table='menu'



class Permission(models.Model):
    name=models.CharField(max_length=128)
    nameurl=models.CharField(max_length=128)
    namemethod=models.CharField(max_length=56)
    relationself=models.ForeignKey(to='self',related_name='permission_self',blank=True,null=True,on_delete=models.CASCADE)
    relationship=models.ForeignKey(to='Menu',related_name='permission_menu',blank=True,null=True,on_delete=models.CASCADE)
    class Meta:
        db_table='permission'
        ordering=['-id']







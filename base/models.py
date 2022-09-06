import datetime
import re
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


# validators
def check_tel(value):
    try:
        if re.match(r'[0-9]{2}[0-9]{5}[0-9]{4}', value):
            int(value)
        else:
            raise ValidationError('Telefone inválido, gentileza verificar')
    except (ValueError,TypeError):
        raise ValidationError('Telefone inválido, gentileza verificar')

def only_int(value):
    try:
        int(value)
    except (ValueError, TypeError):
        raise ValidationError('Valor digitado não é um número')
# models here.
class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    codintfunc = models.PositiveSmallIntegerField()
    uf = models.CharField(max_length=2)
    dt_admfunc = models.DateField()
    dt_nascfunc = models.DateField()
    nomefunc = models.CharField(max_length=100)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    user_ref = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=11, validators=[check_tel], blank=True, null=True)
    ramal = models.CharField(max_length=3, validators=[only_int], blank=True, null=True)
    filial = models.CharField(max_length=3, null=True, blank=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='images/', null=True, blank=True)
    data_cadastro = models.DateTimeField(default=timezone.now)
    ultimo_acesso = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create(username=instance.username, password=make_password(instance.password))
        instance.user_ref = user
        instance.save()

@receiver(post_save, sender=Profile)
def save_user_profile(sender, instance, **kwargs):
    instance.user_ref.save()

class Posts(models.Model):
    text = models.TextField()
    autor = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-pub_date']

class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    pub_date = models.DateTimeField(default=timezone.now)
    post_ref = models.ForeignKey(Posts, on_delete=models.CASCADE)

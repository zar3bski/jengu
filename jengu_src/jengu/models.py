from django.db import models
from django.contrib.auth.models import User # nécessaire pour la foreign key -> chaque user ne voit que ses données

# Create your models here.# 

class Patients(models.Model):
    '''foreign key on users -> encapsulate data'''
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    birth_date = models.DateField()
    inscription = models.DateTimeField(auto_now_add=True)
    tel = models.CharField(max_length=20, null=True)
    #mail = models.EmailField(max_length=80, null=True) # passer en charfield pour ne pas être emmerdé par la cryptographie
    mail = models.CharField(max_length=80, null=True) # Modif pour données encodées côté client
    notes = models.TextField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
    	return '{}, {}, {}'.format(self.last_name,self.first_name,self.birth_date)

class Consultations(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date = models.DateTimeField()
    payed = models.FloatField(null=True) 

'''ensure unicity of emails on the table user'''
User._meta.get_field('email')._unique = True


class Revenues(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    january = models.FloatField(default=0.0)
    february = models.FloatField(default=0.0)
    march = models.FloatField(default=0.0)
    april = models.FloatField(default=0.0)
    may = models.FloatField(default=0.0)
    june = models.FloatField(default=0.0)
    july = models.FloatField(default=0.0)
    august = models.FloatField(default=0.0)
    september = models.FloatField(default=0.0)
    october = models.FloatField(default=0.0)
    november = models.FloatField(default=0.0)
    december = models.FloatField(default=0.0)

class Unpayed(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    january = models.IntegerField(default=0)
    february = models.IntegerField(default=0)
    march = models.IntegerField(default=0)
    april = models.IntegerField(default=0)
    may = models.IntegerField(default=0)
    june = models.IntegerField(default=0)
    july = models.IntegerField(default=0)
    august = models.IntegerField(default=0)
    september = models.IntegerField(default=0)
    october = models.IntegerField(default=0)
    november = models.IntegerField(default=0)
    december = models.IntegerField(default=0)

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    is_chauffeur = models.BooleanField('Chauffeur status', default=False)
    is_passager = models.BooleanField('Passager status', default=False)
    date_naissance=models.DateField(max_length=8,default=timezone.now)
    latitude = models.FloatField(default=31.932940)
    longitude = models.FloatField(default=-4.423060)


class Passager(models.Model):
    passager = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.passager.username


class Chauffeur(models.Model):
    chauffeur = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    PermisConduire  = models.CharField(max_length=30)
    PermisConfiance = models.CharField(max_length=30)
    CIN = models.CharField(max_length=30)
    aPropos = models.TextField()

    def __str__(self):
        return self.chauffeur.username

class Demande(models.Model):
    depart = models.CharField(max_length=100)
    latitudeDepart = models.FloatField(default=31.932940)
    longitudeDepart = models.FloatField(default=-4.423060)
    destination  = models.CharField(max_length=100)
    dateDemande = models.DateTimeField(default=timezone.now)
    nombrePlaces = models.PositiveSmallIntegerField()
    statut = models.BooleanField('Demande status', default=False)
    utilisateur = models.ForeignKey(Passager, on_delete=models.CASCADE)
    chauffeur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.depart


class Taxi(models.Model):
    matricule = models.CharField(max_length=30)
    nombrePlaces = models.PositiveSmallIntegerField()
    marque = models.CharField(max_length=40)
    carteGrise = models.CharField(max_length=40)
    cin_proprietaire = models.CharField(max_length=30, null=True,blank=True)
    PermisConduire_proprietaire = models.CharField(max_length=30, null=True, blank=True)
    PermisConfiance_proprietaire = models.CharField(max_length=30, null=True, blank=True)
    chauffeur = models.OneToOneField(Chauffeur, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.marque

#class Conduire(models.Model):
    #activeActuelement = models.BooleanField(default=False)
    #chauffeur = models.ForeignKey(Chauffeur, on_delete=models.CASCADE)
    #taxi = models.ForeignKey(Taxi, on_delete=models.CASCADE)


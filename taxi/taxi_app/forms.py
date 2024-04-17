from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CustomUser,Chauffeur,Passager
from dobwidget import DateOfBirthWidget




class PassagerSignUpForm(UserCreationForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password1 = forms.CharField(label="Mot de passe",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation du mot de passe",widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'date_naissance']
        widgets = {
            'date_naissance': DateOfBirthWidget(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_passager = True
        if commit:
            user.save()
            passag = Passager.objects.create(passager=user)
        return user


class ChauffeurSignUpForm(UserCreationForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password1 = forms.CharField(label="Mot de passe",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation du mot de passe",widget=forms.PasswordInput)

    PermisConduire = forms.CharField(max_length=30,label="Permis de conduire")
    PermisConfiance = forms.CharField(max_length=30,label="Permis de confiance")
    CIN = forms.CharField(max_length=30)
    aPropos = forms.TextInput()
    date_naissance = forms.DateInput()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','date_naissance']
        widgets = {
            'date_naissance': DateOfBirthWidget(),
        }


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_chauffeur = True
        user.save()
        PC  = self.cleaned_data.get('PermisConduire')
        PCF = self.cleaned_data.get('PermisConfiance')
        CIN = self.cleaned_data.get('CIN')
        chauff = Chauffeur.objects.create(chauffeur=user,PermisConduire=PC,PermisConfiance=PCF,CIN=CIN)
        return user

class passagerUpdateForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.CharField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'date_naissance']
        widgets = {
            'date_naissance': DateOfBirthWidget(),
        }

class chauffeurUpdateForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.CharField(label="Email")
    date_naissance = forms.DateInput()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'date_naissance']
        widgets = {
            'date_naissance': DateOfBirthWidget(),
        }

class chauffeurINFO_UpdateForm(forms.ModelForm):
    PermisConduire = forms.CharField(max_length=30,label="Permis de conduire")
    PermisConfiance = forms.CharField(max_length=30,label="Permis de confiance")
    CIN = forms.CharField(max_length=30)
    aPropos = forms.TextInput()

    class Meta(UserCreationForm.Meta):
        model = Chauffeur
        fields = ['PermisConduire', 'PermisConfiance', 'CIN' , 'aPropos']

    def __init__(self, *args, **kwargs):
        super(chauffeurINFO_UpdateForm, self).__init__(*args, **kwargs)
        self.fields['aPropos'].label = "A propos de vous"
from django.shortcuts import render , redirect
from django.views.generic import CreateView
from .models import CustomUser,Chauffeur,Demande,Passager
from .forms import ChauffeurSignUpForm,PassagerSignUpForm,chauffeurUpdateForm,passagerUpdateForm,chauffeurINFO_UpdateForm
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import passager_required,chauffeur_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages






@csrf_exempt
def demande_passager(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            demande = Demande()
            passag  = Passager.objects.get(passager_id=request.user.id)
            passag.save()
            utilisateur1 = CustomUser.objects.get(id=request.user.id)
            demande.depart          =  request.POST['depart']
            demande.latitudeDepart  =  utilisateur1.latitude
            demande.longitudeDepart =  utilisateur1.longitude
            demande.statut          =  False
            demande.utilisateur     =  passag
            demande.destination     =  request.POST['destination']
            demande.nombrePlaces    =  request.POST['nombreDePlaces']
            demande.save()
        return HttpResponse('demande envoyé')

@csrf_exempt
def demande_accepter(request):
    if request.method == 'POST':
        demande = Demande.objects.get(id=request.POST['id'])
        demande.statut =  True
        demande.chauffeur_id = request.POST['id_chauff']
        demande.save()
    return HttpResponse('demande accepter')


@csrf_exempt
def update_lat_lng(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            utilisateur = CustomUser.objects.get(id=request.user.id)
            utilisateur.latitude =  request.POST['Latitude']
            utilisateur.longitude =  request.POST['Longitude']
            utilisateur.save()
        return HttpResponse('update successful')

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    update_lat_lng(request)
    if request.user.is_authenticated:
        if request.user.is_passager:
            return redirect('home_passager')
        else:
            return redirect('home_chauffeur')
    return render(request, 'home.html')





@login_required #I add it
@passager_required
def home_passager(request):
    update_lat_lng(request)
    p = Demande.objects.last()
    if p :

        if p.statut and p.utilisateur.passager.username == request.user.username:
            context={'chauffeur'     : p.chauffeur,
                     'statut'        : p.statut,
                     'lat'           : p.chauffeur.latitude,
                     'lng'           : p.chauffeur.longitude
                     }
            messages.success(request, f'DEMANDE ACCEPTER par %s' % p.chauffeur)
            return render(request, "home_passager.html", context)
        else:
            context={'chauffeur'     : p.chauffeur,
                     'statut'        : p.statut,
                     'lat'           : 'vide',
                     'lng'           : 'vide'
                     }
            #messages.success(request, f'DEMANDE REFUSEE!')
            return render(request,"home_passager.html", context)




@login_required #I add it
@chauffeur_required
def home_chauffeur(request):
    update_lat_lng(request)
    data = Demande.objects.all()
    p = Demande.objects.last()
    if p :
        context={'data'     : data,
                 'id'       : p.id,
                 'depart'   : p.depart,
                 'userc'    : p.utilisateur,
                 'dest'     : p.destination,
                 'nbPlaces' : p.nombrePlaces,
                 'Latitude' : p.latitudeDepart,
                 'Longitude': p.longitudeDepart,
                 }
        return render(request,"home_chauffeur.html",context)
    else :
        return render(request, "home_chauffeur.html")

@login_required
@passager_required
def profile_passager(request):
    if request.method == "POST":
        u_form = passagerUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request,f'Account updated!')
            return redirect('profile_passager')
    else:
        u_form = passagerUpdateForm(instance=request.user)


    context={
        'u_form' : u_form,
    }
    return render(request,"profile_passager.html",context)

@login_required
@chauffeur_required
def profile_chauffeur(request):
    if request.method == "POST":
        c_form = chauffeurUpdateForm(request.POST, instance=request.user)
        i_form = chauffeurINFO_UpdateForm(request.POST, instance=request.user.chauffeur)
        if c_form.is_valid() and i_form.is_valid():
            c_form.save()
            i_form.save()
            messages.success(request, f'Account updated!')
            return redirect('profile_chauffeur')
    else:
        c_form = chauffeurUpdateForm(instance=request.user)
        i_form = chauffeurINFO_UpdateForm(instance=request.user.chauffeur)

    context = {
        'c_form': c_form,
        'i_form': i_form
    }
    return render(request,"profile_chauffeur.html",context)

class ChauffeurSignUpView(CreateView):
    model = CustomUser
    form_class = ChauffeurSignUpForm
    template_name = 'registration/signup_form.html'


    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'chauffeur'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home_chauffeur')

class PassagerSignUpView(CreateView):
    model = CustomUser
    form_class = PassagerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'passager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home_passager')

def contacter(request):
    return render(request, 'contact.html')

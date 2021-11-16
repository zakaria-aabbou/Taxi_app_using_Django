from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns = [

    path('',views.home,name='home'),
    path('contacter/', views.contacter, name='contacter'),

    #path('chauffeur/', include(([path('', views.home_chauffeur, name='home_chauffeur'),], 'users'), namespace='chauffeurs')),
    #path('passager/',  include(([path('', views.home_passager,  name='home_passager'), ], 'users'), namespace='passagers')),

    url(r'^demande_passager/', views.demande_passager),
    url(r'^demande_accepter/', views.demande_accepter),

    url(r'^update_lat_lng/',   views.update_lat_lng),

    path('chauffeur/chauffeur_profile/', views.profile_chauffeur, name='profile_chauffeur'),
    path('passager/passager_profile/', views.profile_passager, name='profile_passager'),

    path('chauffeur/', views.home_chauffeur, name='home_chauffeur'),
    path('passager/',  views.home_passager,  name='home_passager'),


    path('inscription_chauffeur/',views.ChauffeurSignUpView,name='ins_chauffeur'),
    path('inscription_passager/',views.PassagerSignUpView,name='ins_passager'),


    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/chauffeur/', views.ChauffeurSignUpView.as_view(), name='chauffeur_signup'),
    path('accounts/signup/passager/', views.PassagerSignUpView.as_view(), name='passager_signup'),
]

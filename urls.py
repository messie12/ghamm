from django.conf import settings
from django.contrib import admin
from django.urls import path 
from Nova.settings import STATIC_URL
from comptes.views import inscription, deconnexion,connexion,index
from principal.views import create_client,delete_client,edit_client,agents,listsMOTO,engistrePOS,search_clients,get_donnees,detailMotard
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('perceptron$supernova12@*ù', inscription, name='inscription'),
    path('', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='logout'),
    path('index', index, name='index'),
    path('create_client',create_client, name='create_client'),
    path('delete_client/<int:client_id>/', delete_client, name='delete_client'),
    path('uptadate/<int:client_id>/',edit_client, name='edit_client'),
    path('agents', agents, name='agents'),
    path('liste', listsMOTO, name='listsMOTO'),
    path('T1/', engistrePOS, name='engistrePOS'),
    path('search/',search_clients, name='search_clients'),
    path('get_donnees/',get_donnees, name='get_donnees'),
    path('details/<int:client_id>/',detailMotard, name='detailMotard'),
    
]

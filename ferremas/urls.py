from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('doctors/', views.Productos_view, name='Productos'),
    path('patients/', views.patient_list, name='patient_list'),
    path('pintura/', views.Pintura_view, name='Pintura'),
    path('seguridad/', views.Seguridad_view, name='Seguridad'),
    path('', views.inicio, name='inicio'),
    
    #crud
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('accounts/profile/', views.profile_view, name='profile'),
    #test
    path('forms/', views.forms, name='forms'),
    path('cita_list/', views.cita_list, name='cita_list')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

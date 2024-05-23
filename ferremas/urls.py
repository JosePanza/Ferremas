from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('Productos/', views.Productos_view, name='Productos'),
    path('Pintura/', views.Pintura_view, name='Pintura'),
    path('Seguridad/', views.Seguridad_view, name='Seguridad'),
    path('', views.inicio, name='inicio'),
    
    #crud
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('Carrito_views/', views.Carrito_views, name='Carrito_views'),

    path('Carrito/', views.Carrito_views, name='Carrito'),
  
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

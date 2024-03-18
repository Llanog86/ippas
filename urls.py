"""
URL configuration for Ippas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import registro_usuario, iniciar_sesion, pagina_bienvenida, cerrar_sesion, recuperar_contrasena, perfil_empresa, baja_empresa, registrar_cliente, consulta_clientes

urlpatterns = [
    path('registro/', registro_usuario, name='registro'),
    path('login/', iniciar_sesion, name='login'),
    path('bienvenida/', pagina_bienvenida, name='bienvenida'),
    path('logout/', cerrar_sesion, name='logout'),
    path('recupero/', recuperar_contrasena, name='recupero'),
    path('Perfil/', perfil_empresa, name='Perfil'),
    path('baja_empresa/<str:cuit>/', baja_empresa, name='baja_empresa'),
    path('Clientes/', registrar_cliente, name='Clientes'),
    path('consulta_clientes/', consulta_clientes, name= 'consulta_clientes'),
    # Otras URLs de tu aplicación
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

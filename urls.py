"""weHelp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import url, include
from api import vk_auth_views
from django.views.generic import TemplateView
from chat.views import lobby
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls

#router = routers.DefaultRouter()
#router.register(r'api/users', UserViewSet)

EMAIL_CONFIRMATION = r'^auth/confirm-email/(?P<key>[-:\w]+)$'

PASSWORD_RESET = (
    r'^auth/password/reset/confirm/'
    '(?P<uidb64>[0-9A-Za-z_\-]+)-'
    '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$'
)

OAUTH_CALLBACK = 'accounts/{provider}/login/callback'

auth_url_patterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
]

vk_urlpatterns = [
    path('auth-server/', vk_auth_views.Login.as_view(), name='vk_auth_server'),
    path(
        'login/',
        vk_auth_views.CallbackCreate.as_view(),
        name='vk_callback_login',
    ),
    path(
        'connect/',
        vk_auth_views.CallbackConnect.as_view(),
        name='vk_callback_connect',
    ),
]

urlpatterns = [
    # add your own patterns here
    #url(r'^', include(router.urls)),
    url(r'api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('auth/', include(auth_url_patterns)),
    path('auth/social/vk/', include(vk_urlpatterns)),
    path(
        'accounts/vk/login/callback',
        TemplateView.as_view(),
        name='vk_callback',
    ),
    path('lobby/', lobby, name='lobby'),
    path('chat/', include('chat.urls', namespace='chat')),
] + aldryn_addons.urls.patterns() + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)

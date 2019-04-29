"""iotsettings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import django
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
import views
from material.frontend import urls as frontend_urls


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls),
    url(r'^', include('canonical.urls')),
    url(r'^', include('graph_types.urls')),
    url(r'^', include('dashboard.urls')),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
urlpatterns += [
 url(r'^accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    url(r'^$', views.index, name='index'),
]

urlpatterns += [
    url(r'^registro/', include('canonical.urls_register')),
]

js_info_dict = {
    'packages' : ('recurrence', ), 
}

#jsi18n can be anything you like here
urlpatterns += [
   url(r'^jsi18n/$', django.views.i18n.javascript_catalog,js_info_dict),
]

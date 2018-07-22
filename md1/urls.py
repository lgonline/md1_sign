"""md1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url,include
from sign import views as sing_views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    # url(r'^blog/$', include('blog.urls')),
    # url(r'^$',include('sign.urls')),
    # url(r'^login_action/$',include('sign.urls')),
    # url(r'^event_mgmt/$',include('sign.urls')),
    url(r'^$',sing_views.index),
    url(r'^index/$',sing_views.index),
    url(r'^login_action/$',sing_views.login_action),
    url(r'^event_mgmt/$',sing_views.event_mgmt),
    url(r'^search_name/$',sing_views.search_name),
    url(r'^guest_mgmt/$',sing_views.guest_mgmt),
    url(r'^sign_index/(?P<eid>[0-9]+)/$',sing_views.sign_index),
    url(r'^sign_index_action/(?P<eid>[0-9]+)/$',sing_views.sign_index_action),
    url(r'^logout/$',sing_views.logout),
    url(r'^api/$',include('sign.urls',namespace='sign'))
]

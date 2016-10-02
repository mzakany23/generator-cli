from django.conf.urls import url, include
from django.conf.urls.static import static

from django.contrib import admin
from django.conf import settings

import home.views as home_views

# base
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

# home 
urlpatterns += [
	url(r'^$', home_views.home,name='home'),
]
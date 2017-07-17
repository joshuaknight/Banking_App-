from django.conf.urls import include, url
from django.contrib import admin
from bank_app import urls as bank_url 

urlpatterns = [

    url(r'^account/', include(bank_url)),
    url(r'^admin/', include(admin.site.urls)),
]

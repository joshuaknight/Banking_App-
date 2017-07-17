

from django.conf.urls import url 
from .banking_api import account_api_json,account_api_xml
from .banking_app import create_account


urlpatterns =  [
		url(r'api/account_lis/json$',account_api_json,name="json"),		
		url(r'api/account_lis/xml$',account_api_xml,name="xml"),
		url(r'add$',create_account,name="create_acc"),
] 

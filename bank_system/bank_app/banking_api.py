


from django.shortcuts import render 
from django.http import *

import sqlite3 
import json 


from xml.etree.ElementTree import Element,SubElement,tostring   


def account_api_json(request):			# json response 
	json_lis = []
	if request.method == 'GET':
		def get_from_database():
			conn = sqlite3.connect("db.sqlite3")
			cursor = conn.execute(
				"""
				select * from Account;
				"""
			)
			return cursor.fetchall()		
		content = get_from_database()
		for i in content:			
			dic = {}
			dic['account_no'] = int(i[0])
			dic['account_name'] = str(i[1])
			dic['balance'] = i[2]
			dic['date_of_creation'] = str(i[3])
			dic['contact_id'] = int(i[4])
			dic['customer_id'] = int(i[5])
			dic['account_type'] =  str(i[6])
			dic['user_password'] = str(i[7])
			dic['joint_account'] = str(i[8])		
			json_lis.append(dic)
		return JsonResponse(json_lis,safe=False)



def account_api_xml(request): 			# xml response
	root = Element('account')
	child = SubElement(root,'banking')
	child.text = "2500"	

	return HttpResponse(tostring(root))




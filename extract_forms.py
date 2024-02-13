#!/usr/bin/env python 

import requests
from BeautifulSoup import BeautifulSoup
import urlparse

def request(url):
	try:
		return requests.get(url)
	except requests.exceptions.ConnectionError:
		pass

target_url="http://10.0.2.14/dvwa/login.php"
response = request(target_url)
#print(response)
#print(response.content)

parsed_html = BeautifulSoup(response.content)
forms_list = parsed_html.findAll("form")
#print(forms_list)

for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    print(post_url)
    #print(action)
    method = form.get("method")
    #print(method)

    inputs_list = form.findAll("input")
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        #print(input)
        #print(input_name)
        input_type = input.get("type")
        #print(input_type)
        input_value = input.get("value")
	print(action)
	print(input_name)
	print(input_type)
	print(input_value)

        if input_type == "text":
            input_value = "test"

        post_data[input_name] = input_value
    result = requests.post(post_url, data=post_data)
    print(result)
    #print(result.content)


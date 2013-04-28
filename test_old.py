#!/usr/bin/env python3

import requests
from getpass import getpass
from xml.etree import ElementTree as ET

session = requests.Session()


# Authenticate
username = input('Username: ')
password = getpass()
user = input('Anybody\'s Username: ') #Totally unintended, but apparently you can craft queries for anybody's data (even teachers!)

authpayload = {
		'SubmitCreds': 'Log On',
		'curl': 'Z2F',
		'flags': 0,
		'forcedownlevel': 0,
		'formdir': 3,
		'password': password,
		'trusted': 0,
		'username': username + '@exeter.edu',
		}
session.post('https://connect.exeter.edu/CookieAuth.dll?Logon', data=authpayload);

query = "<soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetUserProfileByName xmlns='http://microsoft.com/webservices/SharePointPortalServer/UserProfileService' ><AccountName>i:0#.w|master\\" + user + "</AccountName></GetUserProfileByName></soap:Body></soap:Envelope>"

#print(session.post('https://connect.exeter.edu/student/_vti_bin/UserProfileService.asmx', data=query, headers={'content-type': 'text/xml'}).text);
r = ET.XML(session.post('https://connect.exeter.edu/student/_vti_bin/UserProfileService.asmx', data=query, headers={'content-type': 'text/xml'}).text);
info = {};
for child in r[0][0][0]:
	def firstname(node):
		info['FirstName'] = node[4][0][0].text
	def lastname(node):
		info['LastName'] = node[4][0][0].text
	def courses(node):
		list = []
		for child in node[4]:
			course = {}
			arr = child[0].text.split('#')
			course['name'] = arr[0]
			course['path'] = arr[1]
			list.append(course)
		info['Courses'] = list

	handle = {
			'FirstName': firstname,
			'LastName': lastname,
			'Courses': courses,
			}
	try:
		#print(child[2].text)
		handle[child[2].text](child)
	except:
		pass

print('\nHello %(FirstName)s %(LastName)s!' % info)
print('Your Courses:\n')
[print('%(path)s\t\t%(name)s' % course) for course in info['Courses']]


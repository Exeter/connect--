#!/usr/bin/env python2

from suds.client import Client
from suds.transport.https import HttpAuthenticated
from suds.sudsobject import asdict
from getpass import getpass
import json

url = 'https://connect.exeter.edu/student/_vti_bin/UserProfileService.asmx?WSDL' 
credentials = dict(username=raw_input('Username: ') +'@exeter.edu', password=getpass())
t = HttpAuthenticated(**credentials);

client = Client(url, transport=t)

def getinfo(user):
	"""Returns dict of user's information"""
	def recursive_asdict(d):
		"""From http://stackoverflow.com/a/15678861"""
		out = {}
		for k, v in asdict(d).iteritems():
			if hasattr(v, '__keylist__'):
				out[k] = recursive_asdict(v)
			elif isinstance(v, list):
				out[k] = []
				for item in v:
					if hasattr(item, '__keylist__'):
						out[k].append(recursive_asdict(item))
					else:
						out[k].append(item)
			else:
				out[k] = v
		return out
	def filterinfo(data):
		dict = recursive_asdict(data)
		info = {}
		for x in dict['PropertyData']:
			k = x['Name']
			values = x['Values']
			if values == "":
				continue
			v = []
			for value in values['ValueData']:
				v.append(value['Value'])
			if len(v) == 1:
				v = v[0]
			info[k] = v
		return info

	profile = client.service.GetUserProfileByName('i:0#.w|master\\' + user)
	return(filterinfo(profile))

def download_all():
	"""hehe. downloads a lot of data. PLEASE DO NOT RUN, ask slee2 for full data.json"""
	emails = json.loads(open('top_secret/emails.json').read())
	users = [email[:email.index('@')] for email in emails]

	data = {}
	print('Downloading data of %i users' % len(users))
	for index, user in enumerate(users):
		try:
			data[user] = getinfo(user);
		except:
			pass
		print(str(index) + '\t' + user)
	f = open('top_secret/data.json', 'w')
	f.write(json.dumps(data))

print(json.dumps(getinfo(raw_input('Anybody\'s Username: ')), indent=4))

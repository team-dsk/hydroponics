# -*- coding: utf-8 -*-
import httplib2
import numpy as np

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

class SpreadSheet(object):
	def __init__(self, key_filename,sheet_id,range,length):
		self.sheetId			 = sheet_id
		self.key_filename	= key_filename
		self.append_range	= range
		self.append_length = length 

		credentials = ServiceAccountCredentials.from_json_keyfile_name(key_filename, scopes=SCOPES)
		http_auth = credentials.authorize(httplib2.Http())
		discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?''version=v4')
		self.service = discovery.build('sheets', 'v4', http=http_auth, discoveryServiceUrl=discoveryUrl)

	def append(self, values):
		assert np.array(values).shape==(self.append_length,) , "The shape of value %s must be %s" % (np.array(values).shape,self.append_length)

		value_range_body = {'values':[values]}
		result = self.service.spreadsheets().values().append(spreadsheetId=self.sheetId, range=self.append_range, valueInputOption='USER_ENTERED', body=value_range_body).execute()
		#print(result)

if __name__ == '__main__':
	sheet = SpreadSheet("1nZhut2Sp8ZlijdCSqxCs4__dDsPXPXUYnu891RYcHqE")
	sheet.append(["test", "test", 0,1])

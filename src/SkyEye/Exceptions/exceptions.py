'''
Created on Jan 19, 2016

@author: Me
'''
import constants

class SkyEyeError(Exception):
	def __init__(self, msg=constants.kErrBase):
		self.msg = msg
		
	def __str__(self):
		return repr(self.msg)
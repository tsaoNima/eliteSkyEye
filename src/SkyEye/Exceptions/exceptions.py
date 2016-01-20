'''
Created on Jan 19, 2016

@author: Me
'''
import constants

class SkyEyeError(Exception):
	def __init__(self, msg):
		self.msg = msg
		
	def __str__(self):
		return repr(self.msg)

class UnsupportedPlatformError(SkyEyeError):
	"""Raised if the given platform doesn't support a requested function.
	"""
	def __init__(self, msg=constants.kErrUnsupportedPlatform):
		self.msg = msg

class PasswordInvalidError(SkyEyeError):
	"""Raised if a password can't actually log the requested user in.
	"""
	def __init__(self, msg=constants.kErrPasswordInvalid):
		self.msg = msg
		
class PasswordMissingError(SkyEyeError):
	"""Raised if a user's password is missing.
	"""
	def __init__(self, user=constants.kUnknownUser):
		self.msg = constants.kFmtErrPasswordMissing.format(user)

#Server errors.
class ServerError(SkyEyeError):
	"""Base class for problems originating on the server.
	"""
	def __init__(self, msg):
		self.msg = msg

class InternalServiceError(ServerError):
	"""Raised if there was a problem connecting server-side code to a server-side service,
	such as the database.
	"""
	def __init__(self, msg):
		self.msg = msg
		
class WrongModeError(ServerError):
	"""Raised if the server cannot complete an operation in its current mode
	(batch mode preventing user input, for example).
	"""
	def __init__(self, msg):
		self.msg = msg
		
#Client errors.
class ClientError(SkyEyeError):
	"""Base class for problems originating from a client request.
	"""
	def __init__(self, msg):
		self.msg = msg
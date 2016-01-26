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

class TestFailedError(SkyEyeError):
	"""Raised if a unit test failed.
	"""
	def __init__(self, testName=constants.kUnknownTest):
		self.msg = constants.kFmtErrTestFailed.format(testName)

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

class IncompleteCommandError(SkyEyeError):
	"""Raised if a command does not have enough parameters
	passed to be evaluatable. 
	"""
	
	def __init__(self, command = None, missingParameters=None):
		"""
		Parameters:
			command: The command to be evaluated as a string. Passed parameters are optional.
			missingParameters: The parameters that were missing from the command, as a tuple of strings.
		"""
		commandStr = constants.kErrIncompleteCommandNameUnknown
		if command is not None:
			commandStr = constants.kFmtErrIncompleteCommandName.format(command)
		parametersStr = constants.kErrIncompleteCommandParametersUnknown
		if missingParameters is not None:
			parametersStr = constants.kFmtErrIncompleteCommandParameters.format(missingParameters) 
			
		self.msg = constants.kFmtErrIncompleteCommand.format(commandStr, parametersStr)

class InvalidParameterError(SkyEyeError):
	"""Raised if parameters given to a function are mutually exclusive
	or set to some forbidden state.
	"""
	
	def __init__(self, msg=constants.kErrInvalidParameter):
		self.msg = msg

#Server errors.
class ServerError(SkyEyeError):
	"""Base class for problems originating on the server.
	"""
	def __init__(self, msg=constants.kErrServerBase):
		self.msg = msg

class NotConnectedError(SkyEyeError):
	"""Raised if the operation requires a connection that hasn't been established.
	"""
	def __init__(self, msg=constants.kErrNotConnected):
		self.msg = msg

class InternalServiceError(ServerError):
	"""Raised if there was a problem connecting server-side code to a server-side service,
	such as the database.
	"""
	def __init__(self, msg=constants.kErrInternalServiceError):
		self.msg = msg
		
class WrongModeError(ServerError):
	"""Raised if the server cannot complete an operation in its current mode
	(batch mode preventing user input, for example).
	"""
	def __init__(self, msg=constants.kErrWrongMode):
		self.msg = msg
		
#Client errors.
class ClientError(SkyEyeError):
	"""Base class for problems originating from a client request.
	"""
	def __init__(self, msg=constants.kErrClientBase):
		self.msg = msg
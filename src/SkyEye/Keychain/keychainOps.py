'''
Created on Jan 19, 2016

@author: Me
'''
import keyring
import sys
import os
import getpass
import win32api
import win32con
import constants
from .. import genericStrings
from ..Exceptions import exceptions
from getpass import GetPassWarning
from ..Logging import log

sLog = log.GetLogInstance()

def getCurrentUser():
	"""Gets the current user ID.
	"""
	
	result = None
	#What system are we on?
	#If POSIX, use os.getuid().
	if (sys.platform.startswith(genericStrings.kPlatformPrefixLinux) or
	sys.platform.startswith(genericStrings.kPlatformPrefixApple)):
		result = os.getuid()  # @UndefinedVariable
	#Otherwise os.getuid() is undefined;
	#use platform-specific call.
	elif sys.platform.startswith(genericStrings.kPlatformPrefixWindows):
		result = win32api.GetUserNameEx(win32con.NameSamCompatible)
	else:
		raise exceptions.UnsupportedPlatformError()
		result = constants.kInvalidUser
	
	return str(result)

def GetPassword(serviceName):
	"""Attempts to get the password for the given service for the current user.
	Returns: The password, or None if no password was found.
	"""
	
	return keyring.get_password(serviceName, getCurrentUser())

def SetPassword(serviceName, password):
	"""Sets the password for the given service for the current user.
	"""
	
	keyring.set_password(serviceName, getCurrentUser(), password)

def PromptPassword(pPrompt = constants.kDefaultPassPrompt):
	"""Requests the user to enter a password via standard input.
	Returns: the password the user entered.
	"""
	
	password = None
	try:
		password = getpass.getpass(prompt=pPrompt)
	except GetPassWarning:
		print constants.kWarnInsecurePrompt
		sLog.LogWarning(constants.kWarnInsecurePrompt, constants.kTagKeychainOps, constants.kMethodRequestPassword)
	finally:
		return password
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
from getpass import GetPassWarning
from ..Logging import log

sLog = log.GetLogInstance()

'''
Gets the current user ID.
'''
def getCurrentUser():
	result = None
	#What system are we on?
	#If POSIX, use os.getuid().
	if (sys.platform.startswith("linux") or
	sys.platform.startswith("darwin")):
		result = os.getuid()  # @UndefinedVariable
	#Otherwise os.getuid() is undefined;
	#use platform-specific call.
	elif sys.platform.startswith("win32"):
		result = win32api.GetUserNameEx(win32con.NameSamCompatible)
	else:
		raise OSError("getCurrentUser(): Unsupported platform!")
		result = ""
	
	return str(result)

'''
Attempts to get the password for the given service for the current user.
Returns: The password, or None if no password was found.
'''
def GetPassword(serviceName):
	return keyring.get_password(serviceName, getCurrentUser())

'''
Sets the password for the given service for the current user.
'''
def SetPassword(serviceName, password):
	keyring.set_password(serviceName, getCurrentUser(), password)

'''
Requests the user to enter a password via standard input.
Returns: the password the user entered.
'''
def RequestPassword(pPrompt = constants.kDefaultPassPrompt):
	password = None
	try:
		password = getpass.getpass(prompt=pPrompt)
	except GetPassWarning:
		print constants.kWarnInsecurePrompt
		sLog.LogWarning(constants.kWarnInsecurePrompt, constants.kTagKeychainOps, constants.kMethodRequestPassword)
	finally:
		return password
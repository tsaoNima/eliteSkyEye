'''
Created on Jan 18, 2016

@author: Me
'''
from Database import setupTables

'''
Represents the server connection.
'''
class Server(object):
	#Database connections for subsystems.
	gdwDatabase = None
	rdaDatabase = None
	batchMode = True
	loggedIn = False
	
	#Returns True if given new credentials, returns False otherwise.
	def requestNewCredentials(self):
		#	Are we in batch mode?
		#		If true, fail.
		#		Otherwise, ask for login.
		pass
	
	def __init__(self, pBatchMode = True):
		self.gdwDatabase = None
		self.rdaDatabase = None
		self.batchMode = True
		self.loggedIn = False
	
	
	'''
	Returns True if we successfully logged in, False otherwise.
	'''
	def Login(self):
		#First, see if we have valid credentials.
		#Do we have any credentials, and if so can we log in with them?
		pass
	
		#If we don't, enter new credentials loop (max 3 tries):
		#	Request new credentials.
		#	If the credentials work, exit loop.
		#	Otherwise continue.
		pass
	
		#Maximum tries exceeded, abort login.
		return False
	
	def FirstTimeSetup(self):
		#Login loop:
		#	Ask for the admin password to the DB. DO NOT STORE THIS.
		#	Logon to "postgres" as the admin "postgres".
		
		#Create our DB admin. Ask for DB admin password.
		#Perform the CREATE USER query. This is the DB admin,
		#so it should have rights to create a database.
		#Store DB admin password in keychain.
		
		#Logout from server admin!
		
		#Login as DB admin.
		#Create all default tables.
		setupTables.SetupTables(user, password)
		#Ideally, fill in the tables with default data.
		pass
	
	def VerifyTables(self):
		#Abort if we're not logged in.
		
		#Get the admin login, pass that to the verify function.
		return setupTables.VerifyTables(user, password)
	
	def Logout(self):
		#Disconnect from subsystems.
		self.loggedIn = False
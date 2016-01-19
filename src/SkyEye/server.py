'''
Created on Jan 18, 2016

@author: Me
'''

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
	def login(self):
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
	
	def firstTimeSetup(self):
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
		#Ideally, fill in the tables with default data.
		
		#Setup guest group role.
		#Guest can read tables, but not modify.
		#Setup base user group role.
		#Base users can see and update data.
		#Finally set up verifier group role.
		#Verifiers can confirm submitted data as valid.
		pass
	
	def logout(self):
		#Disconnect from subsystems.
		self.loggedIn = False
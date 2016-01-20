'''
Created on Jan 15, 2016

@author: Me
'''
import schemas
import constants
import verifyProblem
from ..Database import database
from ..Logging import log
from ..Exceptions import exceptions

sLog = log.GetLogInstance()
subSystems = ((constants.kGDWDatabaseName, schemas.GDWSchemas()),
				(constants.kRDADatabaseName, schemas.RDASchemas()))

def connectToSubsystem(subsystemName, user, password):
	"""Attempts to connect to the requested subsystem's database.
	Returns: A Database object representing the subsystem's database.
	Raises:
		* PasswordInvalidError if the given password can't be used to login. 
		* InternalServiceError if we could not connect to the database for any other reason.
	"""
	db = database.Database()
	try:
		db.Connect(subsystemName, user, password)
	#If login failed, abort.
	except exceptions.PasswordInvalidError as e:
		sLog.LogError(constants.kFmtErrBadCredentials.format(user),
					constants.kTagSetupTables,
					constants.kMethodConnectToSubsystem)
		raise e
	return db

def iterateTables(user, password, callerContext, onTableExists, onTableDoesNotExist):
	"""Used to test/setup all databases.
	Parameters:
		* onTableExists: Callback function. Should take four parameters:
			* callerContext: Same as callerContext passed to iterateTables.
			* subsystemName: Name of the subsystem.
			* db: The database connection.
			* schema: The table schema.
		* onTableDoesNotExist: Callback function, called when a table of the given name could not be found.
		Should take four parameters:
			* callerContext: Same as callerContext passed to iterateTables.
			* subsystemName: Name of the subsystem.
			* db: The database connection.
			* schema: The table schema.
	Raises: 
		* PasswordInvalidError if the given password can't be used to login. 
		* InternalServiceError if we could not connect to the database for any other reason.
	"""
	
	#For each subsystem:
	for s in subSystems:
		dbName = s[0]
		
		#Log in to that subsystem's database.
		db = connectToSubsystem(dbName, user, password)
		
		#Iterate through the table schemas.
		for schema in vars(s):
			#Does this table already exist?
			if db.TableExists(schema.schemaName):
				#If so, enter callback.
				onTableExists(callerContext, dbName, db, schema)
			else:
				#Otherwise enter other callback.
				onTableDoesNotExist(callerContext, dbName, db, schema)
				
		#Remember to disconnect from each system's DB!
		db.Disconnect()

#For verification.
def verifyOnTableExists(callerContext, subsystemName, db, schema):
	"""
	Callback for VerifyTables(), called when the requested table exists.
	"""
	#Check the individual columns...
	for column in schema.schemaColumns:
		#If the column doesn't exist, add to list of problems.
		#Otherwise, check schema details:
		#	Does the column name match?
		#	Does the column type match?
		#	Does the precision match, if precision was specified?
		#	If the column is NOT NULL in the schema, is it NOT NULL in the table?
		#Get all constraints relating to this column:
		#	Does each column's contraint match?
		#	If constraint is a foreign key, is it to the right table?
		#If any of this fails, add as a problem.
		pass

def verifyOnTableDoesNotExist(callerContext, subsystemName, db, schema):
	"""
	Callback for VerifyTables(), called when the requested table does not exist.
	"""
	#Add to error list.
	problem = (subsystemName, schema.schemaName, verifyProblem.TableMissing(schema.schemaName))
	callerContext.append(problem)

#For setup.
def setupOnTableExists(callerContext, subsystemName, db, schema):
	"""
	Callback for SetupTables(), called when the requested table exists.
	"""
	#Drop the current table.
	db.DropTable(schema.schemaName)
	#Create the table.
	db.CreateTable(schema)

def setupOnTableDoesNotExist(callerContext, subsystemName, db, schema):
	"""
	Callback for SetupTables(), called when the requested table exists.
	"""
	#Create the table.
	db.CreateTable(schema)

def VerifyTables(user, password):
	"""Checks that all tables in the server match the schema.
	Returns: A list of problems, if any, with the tables and columns of the server.
	Each problem is a tuple consisting of the following:
		1. Database name.
		2. Table name.
		3. The problem as an object. Problems have an error code (accessible as ".problemCode")
		and a detailed error string (accessible as ".problemString" or __str__()). 
	Raises: 
		* PasswordInvalidError if the given password can't be used to login. 
		* InternalServiceError if we could not connect to the database for any other reason.
	"""
	
	#Ideally we should check schema version first.
	raise NotImplementedError()
	
	#The list of things that failed verification.
	#Elements are tuples:
	
	results = []
	iterateTables(user, password, results, verifyOnTableExists, verifyOnTableDoesNotExist)
	return results

def DropTables(user, password):
	"""Drops all tables used by the server.
	Raises: 
		* PasswordInvalidError if the given password can't be used to login. 
		* InternalServiceError if we could not connect to the database for any other reason,
		or a table was not successfully dropped.
	"""
	for s in subSystems:
		dbName = s[0]
		
		#Log in to that subsystem's database.
		db = connectToSubsystem(dbName, user, password)
		
		#Iterate through the table schemas.
		for schema in vars(s):
			#Drop the table!
			if not db.DropTable(schema.schemaName):
				raise exceptions.InternalServiceError("Failed to drop table {0}".format(schema.SchemaName))
				
		#Remember to disconnect from each system's DB!
		db.Disconnect()

def SetupTables(user, password):
	"""Drops all tables used by the server,
	then creates all tables specified in the schema.
	All data will be lost!
	Raises: 
		* PasswordInvalidError if the given password can't be used to login. 
		* InternalServiceError if we could not connect to the database for any other reason.
	"""
	
	#Would be nice to back up the data first, but one step at a time.
	pass

	#Drop any existing data.
	DropTables(user, password)
	
	#Create the tables.
	iterateTables(user, password, None, setupOnTableExists, setupOnTableDoesNotExist)
	
	#Ideally, fill in the tables with default data afterwards.
	pass
	sLog.LogWarning("TODO: Implement default data initialization!",
				constants.kTagSetupTables,
				"setupTables.SetupTables()")
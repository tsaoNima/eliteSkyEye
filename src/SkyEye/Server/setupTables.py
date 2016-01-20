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

def connectToSubsystemAndRun(subsystem, user, password, onSubsystem, onSubsystemParameters=()):
	dbName = subsystem[0]
	#Log in to that subsystem's database.
	db = connectToSubsystem(dbName, user, password)
	subsystemSchemas = vars(subsystem[1])
	#Iterate through the table schemas.
	sLog.LogVerbose(("Connect to subsystem ", dbName, " and run with schemas ", subsystemSchemas))
	onSubsystem(subsystemSchemas, db, dbName, *onSubsystemParameters)
			
	#Remember to disconnect from each system's DB!
	db.Disconnect()
	
def connectToAllSubsystemsAndRun(user, password, onSubsystem, onSubsystemParameters=()):
	sLog.LogVerbose(("Connect and run with subsystems: ", subSystems))
	for s in subSystems:
		connectToSubsystemAndRun(s, user, password, onSubsystem, onSubsystemParameters)

def connectToAdminDBAndRunOnAllSubsystems(user, password, onSubsystem, onSubsytemParameters=()):
	sLog.LogWarning(constants.kFmtWarnAdminDBConnectionAttempted.format(user),
				constants.kTagSetupTables,
				constants.kMethodConnectToAdminDBAndRunOnAllSubsystems)
	db = connectToSubsystem(constants.kSysAdminDatabaseName, user, password)
	sLog.LogVerbose(("Connect to ADMIN and run with subsystems: ", subSystems))
	for s in subSystems:
		subsystemName = s[0]
		subsystemSchemas = vars(s[1])
		sLog.LogVerbose(("Connect to ADMIN and run on subsystem " ,
						subsystemName,
						" with schemas ",
						subsystemSchemas))
		onSubsystem(subsystemSchemas, db, subsystemName, *onSubsytemParameters)
	db.Disconnect()

#For verification.
def verifyOnTableExists(callerContext, subsystemName, db, schema):
	"""
	Callback for VerifyDatabases(), called when the requested table exists.
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
	Callback for VerifyDatabases(), called when the requested table does not exist.
	"""
	#Add to error list.
	problem = (subsystemName, schema.schemaName, verifyProblem.TableMissing(schema.schemaName))
	callerContext.append(problem)

def dropSubsystemTables(subsystemSchemas, db, subsystemName):
	for schema in subsystemSchemas:
		#Drop the table!
		if not db.DropTable(schema.schemaName):
			raise exceptions.InternalServiceError("Failed to drop table {0}".format(schema.SchemaName))

def setupSubsystemTables(subsystemSchemas, db, subsystemName):
	for schema in subsystemSchemas:
		#Create the table.
		if not db.CreateTable(schema):
			raise exceptions.InternalServiceError("Failed to create table {0}".format(schema.SchemaName))

def verifySubsystemTables(subsystemSchemas, db, subsystemName, callerContext):
	for schema in subsystemSchemas:
		#Does this table already exist?
		if db.TableExists(schema.schemaName):
			#If so, enter callback.
			verifyOnTableExists(callerContext, subsystemName, db, schema)
		else:
			#Otherwise enter other callback.
			verifyOnTableDoesNotExist(callerContext, subsystemName, db, schema)

def DropTablesForDatabase(user, password, subsystem):
	"""Raises: 
		* PasswordInvalidError if the given password can't be used to login. 
		* InternalServiceError if we could not connect to the database for any other reason,
		or a table was not successfully dropped.
	"""
	sLog.LogWarning(constants.kFmtWarnDroppingTablesForDatabase.format(subsystem),
				constants.kTagSetupTables,
				constants.kMethodDropTablesForDatabase)
	connectToSubsystemAndRun(subsystem, user, password, dropSubsystemTables)

def SetupTablesForDatabase(user, password, subsystem):
	"""Raises: 
		* PasswordInvalidError if the given password can't be used to login. 
		* InternalServiceError if we could not connect to the database for any other reason,
		or a table was not successfully dropped.
	"""
	sLog.LogDebug(constants.kFmtCreatingTablesForDatabase.format(subsystem),
				constants.kTagSetupTables,
				constants.kMethodSetupTablesForDatabase)
	connectToSubsystemAndRun(subsystem, user, password, setupSubsystemTables)

def VerifyTablesForDatabase(user, password, subsystem):
	"""Raises: 
		* PasswordInvalidError if the given password can't be used to login. 
		* InternalServiceError if we could not connect to the database for any other reason,
		or a table was not successfully dropped.
	"""
	sLog.LogDebug(constants.kFmtVerifyingTablesForDatabase.format(subsystem),
				constants.kTagSetupTables,
				constants.kMethodVerifyTablesForDatabase)
	results = []
	connectToSubsystemAndRun(subsystem, user, password, verifySubsystemTables, (results,))
	return results

def VerifyDatabases(user, password):
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
	sLog.LogWarning(constants.kVerifyAllDatabasesStarting,
				constants.kTagSetupTables,
				constants.kMethodVerifyDatabases)
	
	#Ideally we should check schema version first.
	raise NotImplementedError("VerifyDatabases() not implemented!")
	
	#The list of things that failed verification.
	results = []
	
	for s in subSystems:
		VerifyTablesForDatabase(user, password, s)
	
	return results
	
def dropSubsystemDatabase(subsystemSchemas, db, subsystemName):
	if not db.DropDatabase(subsystemName):
			raise exceptions.InternalServiceError(constants.kFmtExcDropDatabaseFailed.format(subsystemName))

def createSubsystemDatabase(subsystemSchemas, db, subsystemName):
	if not db.CreateDatabase(subsystemName):
			raise exceptions.InternalServiceError(constants.kFmtExcCreateDatabaseFailed.format(subsystemName))
	
def DropDatabases(user, password):
	"""Drops all databases!
	Raises: 
		* PasswordInvalidError if the given password can't be used to login. 
		* InternalServiceError if we could not connect to the database for any other reason,
		or a table was not successfully dropped.
	"""
	sLog.LogWarning(constants.kWarnDroppingAllDatabases, constants.kTagSetupTables, constants.kMethodDropDatabases)
	connectToAdminDBAndRunOnAllSubsystems(user, password, dropSubsystemDatabase)
		
def SetupDatabases(user, password):
	"""Drops all databases,
	then creates them again as specified in the schema.
	All data will be lost!
	"""
	sLog.LogWarning(constants.kWarnEnteringServerSetup,
				constants.kTagSetupTables,
				constants.kMethodSetupDatabases)
	
	#Would be nice to back up the data first, but one step at a time.
	pass
	sLog.LogWarning("TODO: Implement data backup!",
				constants.kTagSetupTables,
				"setupTables.SetupDatabases()")
	
	#Drop everything!
	DropDatabases(user, password)
	
	#Create the databases first.
	connectToAdminDBAndRunOnAllSubsystems(user, password, createSubsystemDatabase)
	
	#Now setup the databases.
	sLog.LogDebug(constants.kCreateTablesStarting,
				constants.kTagSetupTables,
				constants.kMethodSetupDatabases)
	for s in subSystems:
		SetupTablesForDatabase(user, password, s)
		
	#Ideally, fill in the tables with default data afterwards.
	pass
	sLog.LogWarning("TODO: Implement default data initialization!",
				constants.kTagSetupTables,
				"setupTables.SetupDatabases()")
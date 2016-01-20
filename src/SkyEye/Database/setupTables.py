'''
Created on Jan 15, 2016

@author: Me
'''
import schemas
import constants
import database
import verifyProblem
from ..Logging import log

sLog = log.GetLogInstance()

'''
Used to test/setup all databases.
Parameters:
	* onTableExists: Callback function. Should take four parameters:
		* callerContext: Same as callerContext passed to iterateTables.
		* subsystemName: Name of the subsystem.
		* db: The database connection.
		* schema: The schema.
	* onTableDoesNotExist: Callback function, called when a table of the given name could not be found.
	Should take four parameters:
		* callerContext: Same as callerContext passed to iterateTables.
		* subsystemName: Name of the subsystem.
		* db: The database connection.
		* schema: The schema.
Returns: True if all subsystems could be iterated, False otherwise.
'''
def iterateTables(user, password, callerContext, onTableExists, onTableDoesNotExist):
	#Check - do we have credentials?
	#If not, ask for login.
	
	#Check each subsystem.
	subSystems = ((constants.kGDWDatabaseName, schemas.GDWSchemas()),
				(constants.kRDADatabaseName, schemas.RDASchemas()))
	#For each subsystem:
	for s in subSystems:
		dbName = s[0]
		#Log in to that subsystem's database.
		db = database.Database()
		#If login failed, abort.
		if not db.Connect(dbName, user, password):
			sLog.LogError("Couldn't connect to database {0}, aborting!".format(dbName),
						"SetupTables",
						"setupTables.iterateTables()")
			return False
		#Iterate through the table schemas.
		for schema in vars(s):
			#Does this table already exist?
			if db.TableExists(schema.schemaName):
				#If so, enter callback.
				onTableExists(callerContext, dbName, db, schema)
			else:
				#Otherwise enter other callback.
				onTableDoesNotExist(callerContext, dbName, db, schema)
	return True

#For verification.
def verifyOnTableExists(callerContext, subsystemName, db, schema):
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
	#Add to error list.
	problem = (subsystemName, schema.schemaName, verifyProblem.TableMissing(schema.schemaName))
	callerContext.append(problem)

def VerifyTables(user, password):
	#Ideally we should check schema version first.
	pass
	
	#The list of things that failed verification.
	#Elements are tuples:
	#	1. Database name.
	#	2. Table name.
	#	3. The problem as an object.
	results = []
	iterateTables(user, password, results, verifyOnTableExists, verifyOnTableDoesNotExist)
	return results

#For setup.
def setupOnTableExists(callerContext, subsystemName, db, schema):
	#Drop the current table.
	db.DropTable(schema.schemaName)
	#Create the table.
	db.CreateTable(schema)

def setupOnTableDoesNotExist(callerContext, subsystemName, db, schema):
	#Create the table.
	db.CreateTable(schema)

def SetupTables(user, password):
	return iterateTables(user, password, None, setupOnTableExists, setupOnTableDoesNotExist)
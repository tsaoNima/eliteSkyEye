'''
Created on Jan 15, 2016

@author: Me
'''
import psycopg2
import constants
import queries
import verificationProblems
import SkyEye.Database.schemaBase as schemas
from SkyEye.Logging import log
from SkyEye.Logging.structs import LogLevel
from SkyEye.Exceptions import exceptions
from psycopg2.errorcodes import INVALID_PASSWORD

sLog = log.GetLogInstance()

def addColumnMissing(self, problemList, tableName, columnName):
	problemList.append(verificationProblems.ColumnMissing(tableName, columnName))

def addColumnMismatch(self, problemList, columnName, expectedValue, actualValue):
	problemList.append(verificationProblems.ColumnSchemaMismatch(columnName, expectedValue, actualValue))

def addConstraintMissing(self, problemList, tableName, columnName, constraintType):
	problemList.append(verificationProblems.ColumnConstraintMissing(tableName, columnName, constraintType))

def addConstraintMismatch(self, problemList, columnName, constraintType, expectedValue, actualValue):
	problemList.append(verificationProblems.ColumnSchemaMismatch(columnName, constraintType, expectedValue, actualValue))
	
class Database(object):
	"""Represents a database connection.
	"""

	def execute(self, callerName, query, queryParams, failMsg, failMsgParams = (), runInAutoCommit=False):
		"""Executes the requested query, passing any given parameters.
		Parameters: TODO
		Returns: True if query was successful, False otherwise.
		failMsg should be a format string where the last parameter is the error string.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		#Abort if we don't have a connection.
		if not self.connected:
			sLog.LogVerbose(constants.kErrNotConnected, constants.kTagDatabase, constants.kMethodExecute)
			raise exceptions.NotConnectedError()
			return False
		try:
			isolationLevel = self.connection.isolation_level
			newIsolationLevel = isolationLevel
			if runInAutoCommit:
				newIsolationLevel = 0
			
			self.connection.set_isolation_level(newIsolationLevel)
			sLog.LogVerbose(constants.kFmtQueryAttempted.format(query), constants.kTagDatabase, constants.kMethodExecute)
			self.cursor.execute(query,
						queryParams)
			self.connection.set_isolation_level(isolationLevel)
			
		except psycopg2.Error as e:
			#If failMsgParams is not a tuple, make it a tuple.
			allParams = failMsgParams + (e,)
			sLog.LogError(failMsg.format(*allParams), constants.kTagDatabase, callerName)
			sLog.LogVerbose(constants.kFmtErrErrorCodeWas.format(e.pgcode), constants.kTagDatabase, callerName)
			self.connection.rollback()
			return False
		self.connection.commit()
		sLog.LogVerbose(constants.kQueryExecuted, constants.kTagDatabase, constants.kMethodExecute)
		return True
	
	def executeOnTable(self, callerName, tableName, query, queryParams, failMsg, failMsgParams = (), runInAutocommit=False):
		"""
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		#Sanity check.
		if not tableName:
			sLog.LogWarning(constants.kFmtErrBadTableName.format(tableName), constants.kTagDatabase, constants.kMethodExecuteOnTable)
			return False
		
		return self.execute(callerName, query, queryParams, failMsg, failMsgParams, runInAutocommit)
	
	
	
	def buildSingleColumn(self, column):
		"""Generates column information for CREATE TABLE.
		This function formats a single column's creation line.
		"""
		
		#Does this have precision?
		precisionStr = ""
		if column.Precision > 0:
			precisionStr = constants.kFmtColumnPrecision.format(column.Precision)
		#Does this have constraints?
		constraints = column.Constraints
		constraintStr = ""
		#Build the constraint string, space separating each constraint.
		if len(constraints) > 0:
			constraintStr = constraints[0]
			for c in constraints[1:]:
				constraintStr += constants.kConstraintSeparator + str(c)
		#Also add the foreign key if it exists.
		if column.ForeignKey:
			leading = ""
			if len(constraints) > 0:
				leading = constants.kConstraintSeparator
			constraintStr += leading + schemas.Modifiers.references + constants.kConstraintSeparator + column.ForeignKey
		#Convert that into the final constraint string.
		if constraintStr:
			constraintStr = constants.kFmtColumnConstraints.format(constraintStr)
		#Now build our column.
		return constants.kFmtCreateColumn.format(column.Name,
													column.Type,
													precisionStr,
													constraintStr)
	
	def buildColumnString(self, schema):
		"""Generates column information for CREATE TABLE.
		This function creates the full parameter list that
		creates all columns in the table.
		"""
		
		if not schema:
			return ""
		#Generally a column goes:
		#"[name] [type]([precision]),"
		#Constrained columns have the format:
		#"[name] [type]([precision]) [constraints],"
		#Build the first column.
		result = self.buildSingleColumn(schema[0])
		for column in schema[1:]:
			result += constants.kCreateColumnSeparator + self.buildSingleColumn(column)
		return result
	
	def abort(self):
		"""Throws away all current database references.
		"""
		
		sLog.LogVerbose(constants.kAbortingConnection,
					constants.kTagDatabase,
					constants.kMethodAbort)
		self.dbName = ""
		#The cursor, the thing that you perform database operations on.
		self.cursor = None
		#PostgreSQL connection.
		self.connection = None
		self.connected = False
	
	def __init__(self):
		"""Constructor.
		"""
		
		#Initialize values to defaults.
		self.abort()
	
	def IsConnected(self):
		return self.connected
	
	def Connect(self, pDatabase, pUser, pPassword):
		"""Attempts to connect to the requested database
		on this machine.
		Returns True if the connection was successful, False otherwise.
		Raises:
			* PaswordInvalidError if the given password was invalid.
			* InternalServiceError if any other connection error occurred.
		"""
		
		port = constants.kDefaultDatabasePort
		sLog.LogDebug(constants.kFmtConnectionAttempted.format(pDatabase, port, pUser),
				constants.kTagDatabase,
				constants.kMethodConnect)
		try:
			#Open the connection.
			#We probably want an autocommit connection, no point being explicit.
			#Host is localhost and port is going to be 5432.
			self.connection = psycopg2.connect(database=pDatabase, user=pUser, password=pPassword)
			self.connection.autocommit = True
			#Now get a cursor to start operations.
			self.cursor = self.connection.cursor();
			self.dbName = pDatabase
			self.connected = True
			sLog.LogDebug(constants.kFmtConnectionSucceeded.format(pDatabase, port, pUser),
					constants.kTagDatabase,
					constants.kMethodConnect)
			return True
		except psycopg2.Error as e:
			#Something bad happened.
			newError = None
			#Was it just a bad password?
			if e.pgcode == INVALID_PASSWORD:
				#If so, report that.
				newError = exceptions.PasswordInvalidError()
			#Otherwise, pack into a larger error.
			else:
				newError = exceptions.InternalServiceError(str(e))
			#Abort connection and bubble exception up.
			sLog.LogError(constants.kFmtErrConnectionFailed.format(pDatabase, port, pUser, e),
						constants.kTagDatabase,
						constants.kMethodConnect)
			sLog.LogVerbose(constants.kFmtErrErrorCodeWas.format(e.pgcode),
						constants.kTagDatabase,
						constants.kMethodConnect)
			self.Disconnect()
			raise newError
			return False
		
	
	def Disconnect(self):
		"""Closes database connection.
		"""
		sLog.LogVerbose(constants.kFmtDisconnectStarted.format(self.dbName),
					constants.kTagDatabase,
					constants.kMethodDisconnect)
		if self.cursor is not None:
			self.cursor.close()
		if self.connection is not None:
			self.connection.close()
		sLog.LogVerbose(constants.kFmtDisconnectComplete.format(self.dbName),
					constants.kTagDatabase,
					constants.kMethodDisconnect)
		self.abort()
	
	def TableExists(self, tableName):
		"""Returns: True if the requested table exists,
		False otherwise.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		if self.executeOnTable(constants.kMethodTableExists,
							tableName,
							constants.kQueryCheckTableExists,
							(tableName,),
							constants.kFmtErrTableExistsFailed):
			return self.cursor.fetchone()[0]
		return False

	def DescribeTable(self, tableName):
		"""Describes a given table.
		Returns: The table's schema if successful,
		or an empty tuple if the table could not be found for any reason.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		if self.executeOnTable(constants.kMethodDescribeTable,
							tableName,
							constants.kQueryDescribeTable,
							(tableName,),
							constants.kFmtErrDescribeTableFailed):
			return self.cursor.fetchall()
		return ()
	
	def DropTable(self, tableName):
		"""Attempts to drop the requested table.
		Returns: True if the table was dropped or if the table did not exist, False otherwise.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
	
		queryStr = constants.kQueryDropTable.format(tableName)
		sLog.LogWarning(constants.kFmtWarnDroppingTable.format(tableName),
					constants.kTagDatabase,
					constants.kMethodDropTable)
		return self.executeOnTable(constants.kMethodDropTable,
								tableName,
								queryStr,
								(),
								constants.kFmtErrDropTableFailed)
		
	def DropDatabase(self, dbName):
		"""Attempts to drop the requested *database*.
		Returns: True if the table was dropped or if the database did not exist, False otherwise.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""

		queryStr = constants.kQueryDropDatabase.format(dbName)
		sLog.LogWarning(constants.kFmtWarnDroppingDatabase.format(dbName),
					constants.kTagDatabase,
					constants.kMethodDropDatabase)
		return self.execute(constants.kMethodDropDatabase,
								queryStr,
								(),
								constants.kFmtErrDropDatabaseFailed,
								runInAutoCommit = True)
	
	def DropUser(self, userName):
		"""Attempts to drop the requested user.
		Returns: True if the user was dropped or if the user did not exist, False otherwise.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		queryStr = constants.kQueryDropUser.format(userName)
		sLog.LogWarning(constants.kFmtWarnDroppingUser.format(userName),
					constants.kTagDatabase,
					constants.kMethodDropUser)
		return self.execute(constants.kMethodDropUser,
								queryStr,
								(),
								constants.kFmtErrDropUserFailed,
								runInAutoCommit = True)
		
	def CreateTable(self, schema):
		"""Attempts to create the requested table with the given schema.
		Returns: True if the table was created, False otherwise.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
	
		#Sanity check.
		if not schema.Name:
			sLog.LogError(constants.kFmtErrBadTableName.format(schema.Name), constants.kTagDatabase, constants.kMethodCreateTable)
			return False
		
		#Build the CREATE TABLE string.
		columns = self.buildColumnString(schema.Columns)
		
		#Do our query!
		createString = constants.kFmtQueryCreateTable.format(schema.Name, columns)
		sLog.LogDebug(constants.kFmtCreatingTable.format(createString),
					constants.kTagDatabase,
					constants.kMethodCreateTable)
		return self.execute(constants.kMethodCreateTable,
						createString,
						(),
						constants.kFmtErrCreateTableFailed)
		
	def CreateDatabase(self, dbName):
		"""Attempts to create the requested database.
		Returns: True if the database was created, False otherwise.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		#Sanity check.
		if not dbName:
			return False
			
		queryStr = constants.kQueryCreateDatabase.format(dbName)
		sLog.LogDebug(constants.kFmtCreatingDatabase.format(dbName),
					constants.kTagDatabase,
					constants.kMethodCreateDatabase)
		return self.execute(constants.kMethodCreateDatabase,
								queryStr,
								(),
								constants.kFmtErrCreateDatabaseFailed,
								runInAutoCommit = True)
		
	def CreateUser(self, userName, userPassword, isSuperUser=False, canCreateDB=False, canCreateUsers=False, connectionLimit=-1):
		"""Attempts to create the requested user.
		Returns: True if the user was created, False otherwise.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		#Sanity check.
		if not userName or not userPassword:
			return False
		
		logStr = constants.kFmtCreatingUser.format(userName)
		logLevel = LogLevel.Debug
		
		#Build the query.
		queryStr = constants.kQueryCreateUser.format(userName, userPassword)
		if isSuperUser:
			queryStr += " " + constants.kUserIsSuperUser
			logStr = constants.kFmtCreatingSuperUser.format(userName)
			logLevel = LogLevel.Warning
		else:
			if canCreateDB:
				queryStr += " " + constants.kUserCanCreateDB
			if canCreateUsers:
				queryStr += " " + constants.kUserCanCreateUsers
			
		if connectionLimit >= 0:
			queryStr += " " + constants.kFmtUserConnectionLimit.format(connectionLimit)
		sLog.Log(logStr,
				logLevel,
				constants.kTagDatabase,
				constants.kMethodCreateUser)
		return self.execute(constants.kMethodCreateUser,
								queryStr,
								(),
								constants.kFmtErrCreateUserFailed,
								runInAutoCommit = True)
	
	def getInformationSchemaQueryForTable(self, methodName, queryStr, tableName, failMsg):
		"""Helper function for the following verifyXYZ() functions.
		queryStr is some SQL query that takes a single table name (tableName) as a parameter.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		#Run the specified query.
		if not self.execute(methodName,
								queryStr,
								(tableName,),
								failMsg):
			#Get mad if the query failed.
			raise exceptions.InternalServiceError()
		
		#Otherwise return all rows.
		return self.cursor.fetchall()
	
	def verifyTableDatatypes(self, tableSchema, results):
		"""Verifies that all columns in the requested table fit the given schema.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		query = queries.kQueryGetTableDatatypeInfo
		columnNameIdx = query.IndexForColumn("column_name")
		dataTypeIdx = query.IndexForColumn("data_type")
		charMaxLenIdx = query.IndexForColumn("character_maximum_length")
		dateTimePrecisionIdx = query.IndexForColumn("datetime_precision")
		isNullableIdx = query.IndexForColumn("is_nullable")
		
		#Check column datatype via information_schema.columns on table_name = [our table name].
		datatypeRows = self.getInformationSchemaQueryForTable(constants.kMethodVerifyTableDatatypes,
															query.QueryString,
															tableSchema.Name,
															constants.kFmtErrGetTableDatatypeInfoFailed)
		for column in tableSchema.Columns:
			#If the column doesn't exist in the result set,
			#add it to the list of problems.
			rowsForColumn = [row for row in datatypeRows if row[columnNameIdx] == column.Name]
			if not rowsForColumn:
				addColumnMissing(results, tableSchema.Name, tableSchema.Columns)
				
			#Otherwise, check schema details:
			else:
				#There should only be one row for this column name,
				#since we selected by table.
				assert len(rowsForColumn) == 1
				rowsForColumn = rowsForColumn[0]
				
				#Does the column type match (data_type)?
				expectedType = column.Type.lower()
				actualType = rowsForColumn[dataTypeIdx]
				if actualType != expectedType:
					#If not, mark mismatch.
					addColumnMismatch(results, column.Name + ".data_type", expectedType, actualType)
				
				#If this is a string type or time/timestamp/interval type and precision was specified:
				if column.Precision > 0 and column.Type in schemas.TypesWithPrecision:
					#If this is a string type, does the character maximum length match (character_maximum_length)?
					if column.Type in schemas.StringTypes:
						actualPrecision = rowsForColumn[charMaxLenIdx]
						if actualPrecision != column.Precision:
							#If not, mark mismatch.
							addColumnMismatch(results, column.Name + ".character_maximum_length", column.Precision, actualPrecision)
					#Else if this is a time type, does the precision (datetime_precision) match?
					elif column.Type in schemas.TimeTypes:
						actualPrecision = rowsForColumn[dateTimePrecisionIdx]
						if actualPrecision != column.Precision:
							#If not, mark mismatch.
							addColumnMismatch(results, column.Name + ".datetime_precision", column.Precision, actualPrecision)
					
				#Also check for nullability:
				#	Does this column have a NULL or NOT NULL constraint?
				nullConstraint = [constraint for constraint in column.Constraints if
								isinstance(constraint, basestring) and constraint in schemas.NullConstraints]
				assert len(nullConstraint) <= 1
				if nullConstraint:
					nullConstraint = nullConstraint[0]
					#If so, does it match the is_nullable column in IS.columns?
					expectedValue = schemas.ConstraintIsNullable[nullConstraint] 
					actualValue = rowsForColumn[isNullableIdx]
					if actualValue != expectedValue:
						#If not, mark mismatch.
						addColumnMismatch(results, column.Name + ".is_nullable", expectedValue, actualValue)
	
	def verifyTablePrimaryOrUniqueColumns(self, tableSchema, primaryOrUniqueColumns, results):
		"""Verifies that the requested table has the same PRIMARY KEY/UNIQUE columns
		that were specified in its schema.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		#Get all constraints on the table.
		#Do UNIQUE/PRIMARY KEY first via information_schema.table_constraints.
		#(Use 'public' for constraint_schema and the database name for constraint_catalog.)
		#Select the table_constraints rows (constraint_name, constraint_type).
		query = queries.kQueryGetTablePrimaryOrUniqueInfo
		constraintNameIdx = query.IndexForColumn("constraint_name")
		constraintTypeIdx = query.IndexForColumn("constraint_type")
		datatypeRows = self.getInformationSchemaQueryForTable(constants.kMethodVerifyTablePrimaryOrUniqueCols,
															query.QueryString,
															tableSchema.Name,
															constants.kFmtErrGetTablePrimaryOrUniqueColsInfoFailed)
		
		#For each existing column:
		for column in primaryOrUniqueColumns:
			#Get any UNIQUE/PRIMARY KEY markers.
			nonReferentialConstraints = [constraint for constraint in column.Constraints if
								isinstance(constraint, basestring) and constraint in schemas.NonReferentialConstraints]
			#For each such constraint on the column:
			for constraint in nonReferentialConstraints:
				#Does said constraint exist?
				#Build the constraint_name:
				#[table name]_[column name]_[constraint type suffix].
				constraintName = tableSchema.Name + "_" + column.Name + "_" + schemas.ConstraintToISConstraintNameSuffix[constraint]
				#Get the constraint_type matching that constraint_name.
				constraintRow = [row for row in datatypeRows if row[constraintNameIdx] == constraintName]
				assert len(constraintRow) <= 1
				#If it's missing, add a problem.
				if not constraintRow:
					addConstraintMissing(results, column.Name, constraint)
				#Does the DB constraint type match schema constraint type?
				else:
					constraintRow = constraintRow[0]
					expectedValue = schemas.ConstraintToISConstraintType[constraint]
					actualValue = constraintRow[constraintTypeIdx]
					#If not, add a problem.
					if actualValue != expectedValue:
						addConstraintMismatch(results, column.Name, constraint, expectedValue, actualValue)
	
	def verifyTableForeignColumns(self, tableSchema, foreignColumns, results):
		"""Verifies that all FOREIGN KEY columns in a table
		match their specifications in the table's schema.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		#Finally, check ON DELETE/UPDATE constraints via information_schema.referential_constraints.
		#Select our rows (constraint_name, unique_constraint_name, update_rule, delete_rule).
		#(Use 'public' for constraint_schema and the database name for constraint_catalog.)
		query = queries.kQueryGetTablePrimaryOrUniqueInfo
		constraintNameIdx = query.IndexForColumn("constraint_name")
		uniqueConstraintNameIdx = query.IndexForColumn("unique_constraint_name")
		updateRuleIdx = query.IndexForColumn("update_rule")
		deleteRuleIdx = query.IndexForColumn("delete_rule")
		datatypeRows = self.getInformationSchemaQueryForTable(constants.kMethodVerifyTableForeignCols,
															query.QueryString,
															tableSchema.Name + "%",
															constants.kFmtErrGetTableForeignColsInfoFailed)
		
		#For each remaining column:
		for column in foreignColumns:
			#Build the constraint_name: [table name]_[column_name]_fkey.
			#(Only foreign keys can have an ON DELETE/UPDATE.)
			constraintName = tableSchema.Name + "_" + column.Name + "_fkey"
			constraintRow = [row for row in datatypeRows if row[constraintNameIdx] == constraintName]
			assert len(constraintRow) <= 1
			
			#Does the constraint exist?
			if not constraintRow:
				#If not, mark it as missing.
				addConstraintMissing(results, tableSchema.Name, column.Name, "FOREIGN_KEY")
			#If it does...
			else:
				#Does it refer to the right table ([foreign table name]_pkey)?
				constraintRow = constraintRow[0]
				foreignTableName = column.ForeignKey + "_pkey"
				
				actualValue = constraintRow[uniqueConstraintNameIdx]
				if not actualValue != foreignTableName:
					#If not, record mismatch.
					addConstraintMismatch(results, column.Name, "FOREIGN_KEY", foreignTableName, actualValue)
					
				#Does the ON DELETE RESTRICT/CASCADE option match what's given for our row?
				onDeleteModifier = schemas.RestrictOrCascadeToModifier[schemas.Delete][constraintRow[deleteRuleIdx]]
				if onDeleteModifier and onDeleteModifier not in column.Constraints:
					#If the delete modifier doesn't match, mark the mismatch.
					addConstraintMissing(results, tableSchema.Name, column.Name, onDeleteModifier)
					
				#Does the update modifier match?
				onUpdateModifier = schemas.RestrictOrCascadeToModifier[schemas.Update][constraintRow[updateRuleIdx]]
				if onUpdateModifier and onUpdateModifier not in column.Constraints:
					#If the update modifier doesn't match, mark the mismatch.
					addConstraintMissing(results, tableSchema.Name, column.Name, onUpdateModifier)
	
	def VerifyTable(self, tableSchema):
		"""Checks that the table described by the given schema
		exists and matches the schema.
		Each problem is a tuple consisting of the following:
			1. Database name.
			2. Table name.
			3. The problem as an object. Problems have an error code (accessible as ".problemCode")
			and a detailed error string (accessible as ".problemString" or __str__()). 
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
		"""
		
		#This could take a while, warn the user.
		sLog.LogWarning(constants.kFmtVerifyTableStarting.format(tableSchema.Name),
					constants.kTagDatabase,
					constants.kMethodVerifyTable)
		results = []
		
		#Pull out the columns that have PRIMARY KEY/FOREIGN KEY/UNIQUE modifiers.
		primaryOrUniqueColumns = [column for column in tableSchema.Columns if
								schemas.Modifiers.Unique in column.Constraints or
								schemas.Modifiers.PrimaryKey in column.Constraints]
		foreignColumns = [column for column in tableSchema.Columns if column.ForeignKey]
		
		#Each part of the schema is listed on totally different INFORMATION_SCHEMA
		#tables; split the operation along those tables.
		self.verifyTableDatatypes(tableSchema, results)
		self.verifyTablePrimaryOrUniqueColumns(primaryOrUniqueColumns, results)
		self.verifyTableForeignColumns(foreignColumns, results)
		
		#Return results.
		if results:
			results = [verificationProblems.TableSchemaMismatch(tableSchema.Name),].append(results)
		return results
	
	def VerifyDatabase(self, databaseDefinition):
		"""Checks that all tables in the server match the schema.
		Returns: A list of problems, if any, with the tables and columns of the server.
		Each problem is a tuple consisting of the following:
			1. Database name.
			2. Table name.
			3. The problem as an object. Problems have an error code (accessible as ".problemCode")
			and a detailed error string (accessible as ".problemString" or __str__()). 
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
			* InvalidParameterError if the database definition's name doesn't match this database's name.
		"""
		#Abort if the definiton's name doesn't match the current connection.
		if self.dbName != databaseDefinition.Name:
			raise exceptions.InvalidParameterError(constants.kFmtErrDefinitionNameDoesNotMatch.format(databaseDefinition.Name,
																									self.dbName))
		
		sLog.LogWarning(constants.kFmtVerifyDatabaseStarting.format(self.dbName),
					constants.kTagDatabase,
					constants.kMethodVerifyDatabase)
		
		#Ideally we should check schema version first.
		pass
		
		#The list of things that failed verification.
		results = []
		
		#Now check each table.
		for tableSchema in databaseDefinition.AllSchemas:
			#Check that this table exists.
			if self.TableExists(tableSchema.Name):
				#If it does, check its columns.
				results.append(self.VerifyTable(tableSchema))
			else:
				#Record that the table doesn't exist.
				results.append(verificationProblems.TableMissing(tableSchema.Name))
		
		return results
	
	def SetupDatabase(self, databaseDefinition):
		"""Attempts to create all tables specified in the database definition.
		Returns: True if the database definition's name matches the
		currently connected database's name and all tables were created.
		False otherwise.
		Raises:
			* NotConnectedError if Database.Connect() has not been successfully called.
			* InvalidParameterError if the database definition's name doesn't match this database's name.
		"""
		#Abort if the definiton's name doesn't match the current connection.
		if self.dbName != databaseDefinition.Name:
			raise exceptions.InvalidParameterError(constants.kFmtErrDefinitionNameDoesNotMatch.format(databaseDefinition.Name,
																									self.dbName))
		
		#Now setup the tables.
		sLog.LogDebug(constants.kFmtSetupDatabaseStarting.format(databaseDefinition.Name),
					constants.kTagDatabase,
					constants.kMethodSetupDatabase)
		for tableSchema in databaseDefinition.AllSchemas:
			#If any table could not be created, log error and abort.
			if not self.CreateTable(tableSchema):
				sLog.LogError(constants.kFmtErrSetupDatabaseFailed.format(databaseDefinition.Name),
						constants.kTagDatabase,
						constants.kMethodSetupDatabase)
				return False
			
		#Ideally, fill in the tables with default data afterwards.
		pass
		sLog.LogWarning("TODO: Implement default data initialization!",
					constants.kTagDatabase,
					"setupTables.SetupDatabases()")
		return True
'''
Created on Jan 15, 2016

@author: Me
'''
import psycopg2
import constants
from ..Logging import log
from ..Logging.structs import LogLevel
from ..Exceptions import exceptions
from psycopg2.errorcodes import INVALID_PASSWORD

sLog = log.GetLogInstance()

class Database(object):
	"""Represents a database connection.
	"""

	def execute(self, callerName, query, queryParams, failMsg, failMsgParams = ()):
		"""
		Returns True if query was successful, False otherwise.
		failMsg should be a format string where the last parameter is the error string.
		"""
		if not self.connected:
			sLog.LogVerbose(constants.kErrNotConnected, constants.kTagDatabase, constants.kMethodExecute)
			return False
		try:
			sLog.LogVerbose(constants.kFmtQueryAttempted.format(query), constants.kTagDatabase, constants.kMethodExecute)
			self.cursor.execute(query,
						queryParams)
		except psycopg2.Error as e:
			allParams = failMsgParams + (e,)
			sLog.LogError(failMsg.format(*allParams), constants.kTagDatabase, callerName)
			self.connection.rollback()
			return False
		self.connection.commit()
		sLog.LogVerbose(constants.kQueryExecuted, constants.kTagDatabase, constants.kMethodExecute)
		return True
	
	def executeOnTable(self, callerName, tableName, query, queryParams, failMsg, failMsgParams = ()):
		#Sanity check.
		if not tableName:
			sLog.LogWarning(constants.kFmtErrBadTableName.format(tableName), constants.kTagDatabase, constants.kMethodExecuteOnTable)
			return False
		
		return self.execute(callerName, query, queryParams, failMsg, failMsgParams)
	
	def buildConstraintString(self, constraint):
		result = ""
		#Is this constraint a string?
		if isinstance(constraint, basestring):
			#If it is, return without expanding.
			result = constraint
		else:
			#Otherwise, use subsequent elements as parameters.
			#In practice only REFERENCES has parameters, and for now it only refers to the table;
			#We don't FK on anything besides the referent's PK, so that's fine.
			assert len(constraint) > 1
			result = constraint[0] + " " + constraint[1]
		return result
	
	def buildSingleColumn(self, column):
		#Does this have precision?
		precisionStr = ""
		if len(column) > constants.kSchemaColumnMinElems:
			precisionStr = constants.kFmtColumnPrecision.format(column[constants.kSchemaColumnPrecisionIdx])
		#Does this have constraints?
		constraints = column[constants.kSchemaColumnConstraintIdx]
		constraintStr = ""
		#Build the constraint string, space separating each constraint.
		if len(constraints) > 0:
			constraintStr = self.buildConstraintString(constraints[0])
			for c in constraints[1:]:
				constraintStr += constants.kConstraintSeparator + self.buildConstraintString(c)
			#Convert that into the final constraint string.
			constraintStr = constants.kFmtColumnConstraints.format(constraintStr)
		#Now build our column.
		return constants.kFmtCreateColumn.format(column[constants.kSchemaColumnNameIdx],
													column[constants.kSchemaColumnTypeIdx],
													precisionStr,
													constraintStr)
	
	#Builds a column string based on the given schema.
	#Returns the column string.
	def buildColumnString(self, schema):
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
	
	#Throws away all current database references.
	def abort(self):
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
		"""Returns True if the requested table exists,
		False otherwise.
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
		Returns the table's schema if successful,
		or an empty tuple if the table could not be found for any reason.
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
		Returns True if the table was dropped or if the table did not exist, False otherwise.
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
		Returns True if the table was dropped or if the database did not exist, False otherwise.
		"""
		isolationLevel = self.connection.isolation_level
		#Switch to autocommit mode to allow this operation.
		self.connection.set_isolation_level(0)
		
		queryStr = constants.kQueryDropDatabase.format(dbName)
		sLog.LogWarning(constants.kFmtWarnDroppingDatabase.format(dbName),
					constants.kTagDatabase,
					constants.kMethodDropDatabase)
		result = self.execute(constants.kMethodDropDatabase,
								queryStr,
								(),
								constants.kFmtErrDropDatabaseFailed)
		
		#Switch back to original isolation level.
		self.connection.set_isolation_level(isolationLevel)
		return result
	
	def DropUser(self, userName):
		"""Attempts to drop the requested user.
		Returns True if the user was dropped or if the user did not exist, False otherwise.
		"""
		isolationLevel = self.connection.isolation_level
		#Switch to autocommit mode to allow this operation.
		self.connection.set_isolation_level(0)
		
		queryStr = constants.kQueryDropUser.format(userName)
		sLog.LogWarning(constants.kFmtWarnDroppingUser.format(userName),
					constants.kTagDatabase,
					constants.kMethodDropUser)
		result = self.execute(constants.kMethodDropUser,
								queryStr,
								(),
								constants.kFmtErrDropUserFailed)
		
		#Switch back to original isolation level.
		self.connection.set_isolation_level(isolationLevel)
		return result
		
	def CreateTable(self, schema):
		"""Attempts to create the requested table with the given schema.
		Returns True if the table was created, False otherwise.
		"""
	
		#Sanity check.
		if not schema.SchemaName:
			sLog.LogWarning(constants.kFmtErrBadTableName.format(schema.SchemaName), constants.kTagDatabase, constants.kMethodCreateTable)
			return
		
		#Build the CREATE TABLE string.
		columns = self.buildColumnString(schema.SchemaColumns)
		
		#Do our query!
		createString = constants.kFmtQueryCreateTable.format(schema.SchemaName, columns)
		sLog.LogDebug(constants.kFmtCreatingTable.format(createString),
					constants.kTagDatabase,
					constants.kMethodCreateTable)
		return self.execute(constants.kMethodCreateTable,
						createString,
						(),
						constants.kFmtErrCreateTableFailed)
		
	def CreateDatabase(self, dbName):
		"""Attempts to create the requested database.
		Returns True if the database was created, False otherwise.
		"""
		isolationLevel = self.connection.isolation_level
		#Switch to autocommit mode to allow this operation.
		self.connection.set_isolation_level(0)
		
		queryStr = constants.kQueryCreateDatabase.format(dbName)
		sLog.LogDebug(constants.kFmtCreatingDatabase.format(dbName),
					constants.kTagDatabase,
					constants.kMethodCreateDatabase)
		result = self.execute(constants.kMethodCreateDatabase,
								queryStr,
								(),
								constants.kFmtErrCreateDatabaseFailed)
		
		#Switch back to original isolation level.
		self.connection.set_isolation_level(isolationLevel)
		return result
		
	def CreateUser(self, userName, userPassword, isSuperUser=False, canCreateDB=False, connectionLimit=-1):
		"""Attempts to create the requested user.
		Returns True if the user was created, False otherwise.
		"""
		
		#Sanity check.
		if not userName or not userPassword:
			return False
		
		isolationLevel = self.connection.isolation_level
		#Switch to autocommit mode to allow this operation.
		self.connection.set_isolation_level(0)
		logStr = constants.kFmtCreatingUser.format(userName)
		logLevel = LogLevel.Debug
		
		#Build the query.
		queryStr = constants.kQueryCreateUser.format(userName, userPassword)
		if isSuperUser:
			queryStr += " " + constants.kUserIsSuperUser
			logStr = constants.kFmtCreatingSuperUser.format(userName)
			logLevel = LogLevel.Warning
		if canCreateDB:
			queryStr += " " + constants.kUserCanCreateDB
		if connectionLimit >= 0:
			queryStr += " " + constants.kFmtUserConnectionLimit.format(connectionLimit)
		sLog.Log(logStr,
				logLevel,
				constants.kTagDatabase,
				constants.kMethodCreateUser)
		result = self.execute(constants.kMethodCreateUser,
								queryStr,
								(),
								constants.kFmtErrCreateUserFailed)
		
		#Switch back to original isolation level.
		self.connection.set_isolation_level(isolationLevel)
		return result
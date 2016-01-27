'''
Created on Jan 16, 2016

@author: Me
'''

kDefaultDatabasePort = 5432

#Method names...
kMethodAbort = "Database.abort()"
kMethodExecute = "Database.Execute()"
kMethodExecuteOnTable = "Database.ExecuteOnTable()"
kMethodConnect = "Database.Connect()"
kMethodDisconnect = "Database.Disconnect()"
kMethodTableExists = "Database.TableExists()"
kMethodDescribeTable = "Database.DescribeTable()"
kMethodDropTable = "Database.DropTable()"
kMethodDropDatabase = "Database.DropDatabase()"
kMethodDropUser = "Database.DropUser()"
kMethodCreateTable = "Database.CreateTable()"
kMethodCreateDatabase = "Database.CreateDatabase()"
kMethodCreateUser = "Database.CreateUser()"
kMethodVerifyTable = "Database.VerifyTable()"
kMethodSetupDatabase = "Database.SetupDatabase()"
kMethodVerifyDatabase = "Database.VerifyDatabase()"
kMethodVerifyTableDatatypes = "Database.verifyTableDatatypes()"
kMethodVerifyTablePrimaryOrUniqueCols = "Database.verifyTablePrimaryOrUniqueColumns()"
kMethodVerifyTableForeignCols = "Database.verifyTableForeignColumns()"

#Tags...
kTagDatabase = "Database"

#Log strings...
kErrNotConnected = "Not connected to database, aborting"
kFmtQueryAttempted = "Query requested: {0}"
kQueryExecuted = "Query executed."
kFmtConnectionAttempted = "Connecting to {0}:{1} as {2}..."
kFmtConnectionSucceeded = "Connection to {0}:{1} as {2} successful."
kFmtErrConnectionFailed = "Connection to {0}:{1} as {2} failed with error: {3}"
kAbortingConnection = "Invalidating any existing connection."
kFmtDisconnectStarted = "Disconnecting from {0}..."
kFmtDisconnectComplete = "Disconnect from {0} complete."
kFmtErrBadTableName = "Invalid table name {0} passed, aborting"
kFmtWarnDroppingTable = "Drop requested! Dropping table {0}"
kFmtErrDropTableFailed = "Table drop failed with error: {0}"
kFmtWarnDroppingDatabase = "Database drop requested! Dropping DATABASE {0}"
kFmtErrDropDatabaseFailed = "Database drop failed with error: {0}"
kFmtWarnDroppingUser = "User drop requested! Dropping user {0}"
kFmtErrDropUserFailed = "User drop failed with error: {0}"
kFmtCreatingTable = "Table creation requested.\nCreate string: \"{0}\""
kFmtErrCreateTableFailed = "Table create failed with error: {0}"
kFmtCreatingDatabase = "Database creation requested. Creating database {0}"
kFmtErrCreateDatabaseFailed = "Database create failed with error: {0}"
kFmtCreatingUser = "User creation requested. Creating user {0}"
kFmtCreatingSuperUser = "Superuser creation requested! Creating superuser {0}"
kFmtErrCreateUserFailed = "User create failed with error: {0}"
kFmtErrTableExistsFailed = "Table existence check failed with error: {1}"
kFmtErrDescribeTableFailed = "Table description failed with error: {0}"
kFmtErrGetTableDatatypeInfoFailed = "Table datatype retrieval failed with error: {0}" 
kFmtErrGetTablePrimaryOrUniqueColsInfoFailed = "Table primary/unique column info retrieval failed with error: {0}"
kFmtErrGetTableForeignColsInfoFailed = "Table foreign column info retrieval failed with error: {0}"
kFmtVerifyTableStarting = "Verifying table {0}..."
kFmtVerifyDatabaseStarting = "Verifying database {0}..."
kFmtErrDefinitionNameDoesNotMatch = "Database definition is for database {0}, but was passed to database {1}."
kFmtSetupDatabaseStarting = "Generating database {0} from definition..."
kFmtErrSetupDatabaseFailed = "Failed to generate database {0}!"
kFmtErrErrorCodeWas = "Error code: {0}"

#Queries...
kQueryDescribeTable = ("SELECT column_name, data_type, character_maximum_length, is_nullable "  
"FROM information_schema.columns WHERE table_name = %s;")
"""Describes the requested table.
	0: Table name.
"""

kQueryCheckTableExists = ("SELECT EXISTS (SELECT * FROM information_schema.tables "
						"WHERE table_name = %s);")
"""Returns true if the requested table exists, false otherwise.
Note that this doesn't check the current schema!
	0: Table name.
"""

kQueryDropTable = "DROP TABLE IF EXISTS {0};"
"""Drops the requested table.
	0: Table name.
"""

kQueryDropDatabase = "DROP DATABASE IF EXISTS {0};"
"""Drops the requested database.
	0: Database name.
"""

kQueryDropUser = "DROP USER IF EXISTS {0};"
"""Drops the requested user.
	0: User name.
"""

kFmtQueryCreateTable = "CREATE TABLE {0} ({1});"
"""Creates the requested table.
	0: Table name.
	1: Column info. Should be prebuilt and filled in with the formatter.
"""

#Column formatting strings.
kFmtCreateColumn = "{0} {1}{2}{3}"
"""
	0: Column name.
	1: Column type.
	2: Column precision, if any.
	3: Column constraints, if any.
"""
kSchemaColumnMinElems = 3
kSchemaColumnNameIdx = 0
kSchemaColumnTypeIdx = 1
kSchemaColumnConstraintIdx = 2
kSchemaColumnPrecisionIdx = 3
kFmtColumnPrecision = "({0})"
"""
	0: The column's precision. If there is no precision,
	use an empty string instead of this constant.
"""
kFmtColumnConstraints = " {0}"
"""
	0: The column's constraints. If there are no constraints,
	use an empty string instead of this constant.
"""
kConstraintSeparator = " "
kCreateColumnSeparator = ", "

kQueryCreateDatabase = "CREATE DATABASE {0};"
"""Creates the requested database.
	0: Database name.
"""

kQueryCreateUser = "CREATE USER {0} WITH ENCRYPTED PASSWORD '{1}'"
"""Creates the requested user.
	0: User name.
	1: User password.
"""
kUserIsSuperUser = "SUPERUSER"
kUserCanCreateDB = "CREATEDB"
#"CREATEUSER" is actually an alias for "SUPERUSER";
#since superusers totally bypass any access restrictions,
#we don't actually want that.
kUserCanCreateUsers = "CREATEROLE"
kFmtUserConnectionLimit = "CONNECTION LIMIT {0}"
"""
	0: Maximum number of simultaneous connections.
"""

kFmtDatatypeEquals = "data_type = {0}"
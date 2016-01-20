'''
Created on Jan 16, 2016

@author: Me
'''

kSchemaNameLenMax = 255
kDefaultDatabasePort = 5432
 
kSysAdminDatabaseName = "postgres"
kSysAdminUserName = "postgres"

#Method names...
kMethodExecute = "Database.execute()"
kMethodExecuteOnTable = "Database.executeOnTable()"
kMethodConnect = "Database.connect()"
kMethodTableExists = "Database.tableExists()"
kMethodDescribeTable = "Database.describeTable()"
kMethodDropTable = "Database.dropTable()"
kMethodCreateTable = "Database.createTable()"
kMethodVerifyGDW = "Database.verifyGDW()"
kMethodVerifyRDA = "Database.verifyRDA()"

#Tags...
kTagDatabase = "Database"

#Log strings...
kErrNotConnected = "Not connected to database, aborting"
kFmtConnectionAttempted = "Connecting to {0}:{1} as {2}..."
kFmtConnectionSucceeded = "Connection to {0}:{1} as {2} successful."
kFmtErrConnectionFailed = "Connection failed with error: {0}"
kFmtErrBadTableName = "Invalid table name {0} passed, aborting"
kFmtWarnDroppingTable = "Drop requested! Dropping table {0}"
kFmtErrDropTableFailed = "Table drop failed with error: {0}"
kFmtCreatingTable = "Table creation requested.\nCreate string: \"{0}\""
kFmtErrCreateTableFailed = "Table create failed with error: {0}"
kFmtErrTableExistsFailed = "Table existence check failed with error: {1}"
kFmtErrDescribeTableFailed = "Table description failed with error: {0}"

#Queries...
#Describes the requested table.
#0: Table name.
kQueryDescribeTable = ("SELECT column_name, data_type, character_maximum_length, is_nullable "  
"FROM information_schema.columns WHERE table_name = %s;")
#Returns true if the requested table exists, false otherwise.
#Note that this doesn't check the current schema!
#0: Table name.
kQueryCheckTableExists = ("SELECT EXISTS (SELECT * FROM information_schema.tables "
						"WHERE table_name = %s);")
#Drops the requested table.
#0: Table name.
kQueryDropTable = "DROP TABLE \"{0}\";"
#Creates the requested table.
#0: Table name.
#1: Column info. Should be prebuilt and filled in with the formatter.
kFmtQueryCreateTable = "CREATE TABLE {0} ({1});"
#0: Column name.
#1: Column type.
#2: Column precision, if any.
#3: Column constraints, if any.
kFmtCreateColumn = "{0} {1}{2}{3}"
kSchemaColumnMinElems = 3
kSchemaColumnNameIdx = 0
kSchemaColumnTypeIdx = 1
kSchemaColumnConstraintIdx = 2
kSchemaColumnPrecisionIdx = 3
#0: The column's precision. If there is no precision,
#use an empty string instead of this constant.
kFmtColumnPrecision = "({0})"
#0: The column's constraints. If there are no constraints,
#use an empty string instead of this constant.
kFmtColumnConstraints = " {0}"
kConstraintSeparator = " "
kCreateColumnSeparator = ", "
'''
Created on Jan 16, 2016

@author: Me
'''

kSchemaNameLenMax = 255

kGDWDatabaseName = "GeoDataWarehouse"
kRDADatabaseName = "ReconDataAnalyzer"

#Log strings...
kFmtErrConnectionFailed = "Database.connect(): Connection failed with error: {0}"
kFmtErrBadTableName = "{0}: invalid table name passed, aborting"
kFmtErrDropTableFailed = "{0}: Table drop failed with error: {1}"
kFmtErrCreateTableFailed = "{0}: Table create failed with error: {1}"
kFmtErrDescribeTableFailed = "Database.describeTable(): Table description failed with error: {0}"
kFmtWarnVerificationFailed = "Database.verifyAll(): {0} failed verification!"
kVerificationAllPassed = "Database.verifyAll(): All modules passed verification."
kFmtWarnSchemaFailed = "{0}: Schema {1} failed verification!"
kMethodDescribeTable = "Database.describeTable()"
kMethodDropTable = "Database.dropTable()"
kMethodCreateTable = "Database.createTable()"
kMethodVerifyGDW = "Database.verifyGDW()"
kMethodVerifyRDA = "Database.verifyRDA()"

#Queries...
#Describes the requested table.
kQueryDescribeTable = "select column_name, data_type, character_maximum_length, is_nullable "
"from INFORMATION_SCHEMA.COLUMNS where table_name = (%s);"
#Drops the requested table.
kQueryDropTable = "drop table (%s);"
#Creates the requested table.
#Column info should be prebuilt and filled in with the formatter.
kFmtQueryCreateTable = "create table (%s) ({0});"
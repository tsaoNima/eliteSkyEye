'''
Created on Jan 16, 2016

@author: Me
'''

#Log strings...
kFmtErrConnectionFailed = "Database.connect(): Connection failed with error: {0}"
kFmtErrDescribeTableBadTableName = "Database.describeTable(): invalid table name passed, aborting"
kFmtErrDescribeTableFailed = "Database.describeTable(): Table description failed with error: {0}"
kFmtWarnVerificationFailed = "Database.verifyAll(): {0} failed verification!"
kVerificationAllPassed = "Database.verifyAll(): All modules passed verification."
kFmtWarnSchemaFailed = "{0}: Schema {1} failed verification!"
kMethodVerifyGDW = "Database.verifyGDW()"
kMethodVerifyRDA = "Database.verifyRDA()"

#Queries...
#Describes the requested table.
kFmtQueryDescribeTable = ("select column_name, data_type, character_maximum_length "
"from INFORMATION_SCHEMA.COLUMNS where table_name = (%s);")
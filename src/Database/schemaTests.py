'''
Created on Jan 16, 2016

@author: Me
'''

#All tests must return True iff the schema matches exactly, false otherwise.

def verifySchema(database, schema):
	#Make sure the table exists on the database.
	#If it does, iterate over columns:
	#	Does the column name match?
	#	Does the column type match?
	#	Does the precision match, if precision was specified?
	#	If the column is NOT NULL in the schema, is it NOT NULL in the table?
	#Next, iterate over constraints (primary, foreign, unique):
	#	Does each column's contraint match?
	#	If constraint is a foreign key, is it to the right table?
	pass

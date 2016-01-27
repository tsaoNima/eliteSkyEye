'''
Created on Jan 16, 2016

@author: Me
'''
import constants

version = (1, 0)
"""Specifies what version of the schema definition this is.
"""

kSchemaNameLenMax = 255
"""The default maximum number of characters in a text field.
"""

class Types:
	"""Specifies the valid SQL data types.
	"""
	int = "INTEGER"
	real = "REAL"
	float = "DOUBLE PRECISION"
	bool = "BOOLEAN"
	varchar = "CHARACTER VARYING"
	char = "CHARACTER"
	text = "TEXT"
	timestamp = "TIMESTAMP"
	timestampTimeZone = "TIMESTAMP WITH TIME ZONE"
	date = "DATE"
	time = "TIME"
	timeTimeZone = "TIME WITH TIME ZONE"
	interval = "INTERVAL"

class Modifiers:
	"""Specifies valid column modifiers.
	"""
	
	notNull = "NOT NULL"
	unique = "UNIQUE"
	primaryKey = "PRIMARY KEY"
	references = "REFERENCES"
	onDeleteRestrict = "ON DELETE RESTRICT"
	onDeleteCascade = "ON DELETE CASCADE"
	onUpdateRestrict = "ON UPDATE RESTRICT"
	onUpdateCascade = "ON UPDATE CASCADE"
	nullDefault = "NULL"

ConstraintToISConstraintType = {
							Modifiers.unique : "UNIQUE",
							Modifiers.primaryKey : "PRIMARY_KEY",
							Modifiers.references : "FOREIGN_KEY"
							}
"""Maps constraint names to INFORMATION_SCHEMA constraint_type strings.
"""

ConstraintToISConstraintNameSuffix = {
							Modifiers.unique : "key",
							Modifiers.primaryKey : "pkey",
							Modifiers.references : "fkey"
							}
"""Maps constraint names to INFORMATION_SCHEMA constraint_name suffixes.
Note that these are lowercased!
"""

TypesWithPrecision = set(
					Types.varchar,
					Types.char,
					Types.timestamp,
					Types.timestampTimeZone,
					Types.time,
					Types.timeTimeZone,
					Types.interval
					)

StringTypes = set(
			Types.varchar,
			Types.char,
			Types.text
			)

TimeTypes = set(
			Types.timestamp,
			Types.timestampTimeZone,
			Types.date,
			Types.time,
			Types.timeTimeZone,
			Types.interval
			)

NullConstraints = set(
					Modifiers.notNull,
					Modifiers.nullDefault
					)

ConstraintIsNullable = {
					Modifiers.notNull : False,
					Modifiers.nullDefault : True
					}

NonReferentialConstraints = set(
					Modifiers.unique,
					Modifiers.primaryKey
					)

ReferentialConstraints = set(
					Modifiers.references,
					Modifiers.onDeleteCascade,
					Modifiers.onDeleteRestrict,
					Modifiers.onUpdateCascade,
					Modifiers.onUpdateRestrict
					)

Delete = "delete"
Update = "update"
NoAction = "NO ACTION"
Restrict = "RESTRICT"
Cascade = "CASCADE"
RestrictOrCascadeToModifier = {
							Delete : {
									Restrict : Modifiers.onDeleteRestrict,
									Cascade : Modifiers.onDeleteCascade,
									NoAction : ""									
									},
							Update : {
									Restrict : Modifiers.onUpdateRestrict,
									Cascade : Modifiers.onUpdateCascade,
									NoAction : ""
									}
							}

class Column(object):
	"""Describes a column in a SQL table.
	"""
	
	def __init__(self, pName, pType, pConstraints=(), pPrecision=-1, pForeignKey=""):
		self.Name = pName
		self.Type = pType
		self.Constraints = pConstraints
		self.Precision = pPrecision
		self.ForeignKey = pForeignKey
	
class TableDefinition(object):
	"""Describes a SQL table's schema.
	"""
	
	def __init__(self, pName, pColumns):
		self.Name = pName
		self.Columns = pColumns

class DatabaseDefinition(object):
	"""Describes a SQL database.
	"""
	
	def __init__(self):
		self.Name = ""
		self.AllSchemas = []
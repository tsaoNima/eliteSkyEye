'''
Created on Jan 16, 2016

@author: Me
'''
from SkyEye.Logging import log
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
	
	Int = "INTEGER"
	Real = "REAL"
	Float = "DOUBLE PRECISION"
	Bool = "BOOLEAN"
	VarChar = "CHARACTER VARYING"
	Char = "CHARACTER"
	Text = "TEXT"
	Timestamp = "TIMESTAMP"
	TimestampTimeZone = "TIMESTAMP WITH TIME ZONE"
	Date = "DATE"
	Time = "TIME"
	TimeTimeZone = "TIME WITH TIME ZONE"
	Interval = "INTERVAL"

class Modifiers:
	"""Specifies valid column modifiers.
	"""
	
	NotNull = "NOT NULL"
	Unique = "UNIQUE"
	PrimaryKey = "PRIMARY KEY"
	NullDefault = "NULL"
	
class DeleteUpdateModifiers:
	"""Specifies valid modifiers for ON DELETE/ON CASCADE.
	"""
	
	NoAction = 0
	Restrict = 1
	Cascade = 2

ConstraintToISConstraintType = {
							Modifiers.Unique : "UNIQUE",
							Modifiers.PrimaryKey : "PRIMARY_KEY"
							}
"""Maps constraint names to INFORMATION_SCHEMA constraint_type strings.
"""

ConstraintToISConstraintNameSuffix = {
							Modifiers.Unique : "key",
							Modifiers.PrimaryKey : "pkey"
							}
"""Maps constraint names to INFORMATION_SCHEMA constraint_name suffixes.
Note that these are lowercased!
"""

TypesWithPrecision = set(
					[Types.VarChar,
					Types.Char,
					Types.Timestamp,
					Types.TimestampTimeZone,
					Types.Time,
					Types.TimeTimeZone,
					Types.interval]
					)

StringTypes = set(
			[Types.VarChar,
			Types.Char,
			Types.Text]
			)

TimeTypes = set(
			[Types.Timestamp,
			Types.TimestampTimeZone,
			Types.Date,
			Types.Time,
			Types.TimeTimeZone,
			Types.interval]
			)

NullConstraints = set(
					[Modifiers.NotNull,
					Modifiers.NullDefault]
					)

ConstraintIsNullable = {
					Modifiers.NotNull : False,
					Modifiers.NullDefault : True
					}

NonReferentialConstraints = set(
					[Modifiers.Unique,
					Modifiers.PrimaryKey]
					)

Delete = "delete"
Update = "update"
NoAction = "NO ACTION"
OnDelete = "ON DELETE"
OnUpdate = "ON UPDATE"
Restrict = "RESTRICT"
Cascade = "CASCADE"
OnDeleteRestrict = OnDelete + " " + Restrict
OnDeleteCascade = OnDelete + " " + Cascade
OnUpdateRestrict = OnUpdate + " " + Restrict
OnUpdateCascade = OnUpdate + " " + Cascade
ForeignKey = "FOREIGN_KEY"
References = "REFERENCES"
RestrictOrCascadeToModifier = {
							Restrict : DeleteUpdateModifiers.Restrict,
							Cascade : DeleteUpdateModifiers.Cascade,
							NoAction : DeleteUpdateModifiers.NoAction
							}
DeleteModifierToString = {
						DeleteUpdateModifiers.Restrict : OnDeleteRestrict,
						DeleteUpdateModifiers.Cascade : OnDeleteCascade,
						DeleteUpdateModifiers.NoAction : ""
						}
UpdateModifierToString = {
						DeleteUpdateModifiers.Restrict : OnUpdateRestrict,
						DeleteUpdateModifiers.Cascade : OnUpdateCascade,
						DeleteUpdateModifiers.NoAction : ""
						}

sLog = log.GetLogInstance()

class Column(object):
	"""Describes a column in a SQL table.
	"""
	
	def __init__(self, pName, pType,
				pConstraints=(),
				pPrecision=-1,
				pForeignKey="",
				pDeleteRule=DeleteUpdateModifiers.NoAction,
				pUpdateRule=DeleteUpdateModifiers.NoAction):
		self.Name = pName
		self.Type = pType
		self.Constraints = pConstraints
		#Constraints must be a tuple;
		#There's a lot of columns with just one constraint though,
		#so the schema writer might forget a comma.
		#If the schema's a string, coerce it to a 1-tuple.
		if not isinstance(self.Constraints, tuple):
			#(Note that it'll definitely be a string,
			#since all constraints are defined as strings.)
			#Warn user if we coerced input into a tuple.
			sLog.LogWarning(constants.kFmtWarnCoercingConstraintString.format(self.Constraints),
						constants.kTagSchemaBase,
						constants.kMethodColumnInit)
			#TODO: have a strict mode?
			self.Constraints = (str(self.Constraints),)
		self.Precision = pPrecision
		self.ForeignKey = pForeignKey
		self.DeleteRule = pDeleteRule
		self.UpdateRule = pUpdateRule
	
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
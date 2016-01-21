'''
Created on Jan 16, 2016

@author: Me
'''
import constants

version = (1, 0)
"""Specifies what version of the schema definition this is.
"""

class Types:
	"""Specifies the valid SQL data types.
	"""
	int = "INTEGER"
	real = "REAL"
	float = "DOUBLE PRECISION"
	numeric = "NUMERIC"
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
class Column(object):
	def __init__(self, pName, pType, pConstraints=(), pPrecision=-1):
		self.Name = pName
		self.Type = pType
		self.Constraints = pConstraints
		self.Precision = pPrecision
	
class Schema(object):
	def __init__(self, pName, pColumns):
		self.SchemaName = pName
		self.SchemaColumns = pColumns

class DatabaseDefinition(object):
	def __init__(self):
		self.Name = ""
		self.AllSchemas = {}

class GDWSchemas(DatabaseDefinition):
	"""Describes all GDW tables.
	"""
	
	def __init__(self):
		self.Name = constants.kGDWDatabaseName
		self.AllSchemas = [
						Schema("celestial_types",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
												Column("is_star", Types.bool, (Modifiers.notNull,)))
												),
						Schema("ring_types",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
											),
						Schema("celestial_relationships",
														(Column("id", Types.int, (Modifiers.primaryKey,)),
														Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
														),
						Schema("governments",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
											Column("generates_police", Types.bool, (Modifiers.notNull,)))
											),
						Schema("economies",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
											),
						Schema("superpowers",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
											),
						Schema("cz_intensities",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
												),
						Schema("global_states",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
												),
						Schema("system_states",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
												),
						Schema("factions",
										(Column("id", Types.int, (Modifiers.primaryKey,)),
										Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
										Column("government", Types.int, (Modifiers.notNull, (Modifiers.references, "governments"))),
										Column("superpower", Types.int, (Modifiers.notNull, (Modifiers.references, "superpowers"))),
										Column("current_global_state", Types.int, (Modifiers.notNull, (Modifiers.references, "global_states"))),
										Column("pending_global_state", Types.int, (Modifiers.notNull, (Modifiers.references, "global_states"))))
										),
						Schema("systems",
										(Column("id", Types.int, (Modifiers.primaryKey,)),
										Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
										Column("coord_x", Types.float),
										Column("coord_y", Types.float),
										Column("coord_z", Types.float),
										Column("owning_faction", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))))
										),
						Schema("system_celestials",
													(Column("id", Types.int, (Modifiers.primaryKey,)),
													Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
													Column("celestial_type", Types.int, (Modifiers.notNull, (Modifiers.references, "celestial_types"))),
													Column("ring_type", Types.int, (Modifiers.notNull, (Modifiers.references, "ring_types"))),
													Column("distance_from_entry_point", Types.float))
													),
						Schema("structures",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
											Column("owning_faction", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))),
											Column("economy", Types.int, (Modifiers.notNull, (Modifiers.references, "economies"))),
											Column("celestial", Types.int, (Modifiers.notNull, (Modifiers.references, "system_celestials"))),
											Column("distance_from_celestial", Types.float),
											Column("celestial_relationship", Types.int, (Modifiers.notNull, (Modifiers.references, "celestial_relationships"))))
											),
						Schema("wars",
									(Column("id", Types.int, (Modifiers.primaryKey,)),
									Column("faction_1", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))),
									Column("faction_2", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))),
									Column("war_start", Types.timestamp, (Modifiers.notNull,)),
									Column("war_end", Types.timestamp))
									),
						Schema("conflict_zones",
												(Column("id", Types.int, (Modifiers.primaryKey,)),
												Column("celestial", Types.int, (Modifiers.notNull, (Modifiers.references, "system_celestials"))),
												Column("distance_from_celestial", Types.float,
												Column("intensity", Types.int, (Modifiers.notNull, (Modifiers.references, "cz_intensities"))),
												Column("war", Types.int, (Modifiers.notNull, (Modifiers.references, "wars"))),
												Column("faction_1_deployed_cap_ship", Types.bool, (Modifiers.notNull,)),
												Column("faction_2_deployed_cap_ship", Types.bool, (Modifiers.notNull,)),
												Column("is_visible", Types.bool, (Modifiers.notNull,)),
												Column("last_updated", Types.timestamp, (Modifiers.notNull,))))
												),
						Schema("factions_in_system",
													(Column("id", Types.int, (Modifiers.primaryKey,)),
													Column("factions", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))),
													Column("influence", Types.float, (Modifiers.notNull,)),
													Column("current_system_state", Types.int, (Modifiers.notNull, (Modifiers.references, "system_states"))),
													Column("pending_system_state", Types.int, (Modifiers.notNull, (Modifiers.references, "system_states"))),
													Column("entered_system_date", Types.timestamp, ()),
													Column("left_system_date", Types.timestamp, ()),
													Column("last_updated_date", Types.timestamp, (Modifiers.notNull,)))
													)
						]

class RDASchemas(DatabaseDefinition):
	"""Describes all RDA tables.
	"""
	def __init__(self):
		self.Name = constants.kRDADatabaseName
		self.AllSchemas = [
						Schema("event_types",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
											),
						Schema("player_info",
											(Column("id", Types.int, (Modifiers.primaryKey,)),
											Column("user_id", Types.int, ()),
											Column("elite_name", Types.varchar, (), constants.kSchemaNameLenMax))
											),
						Schema("events",
										(Column("id", Types.int, (Modifiers.primaryKey,)),
										Column("event_date", Types.timestamp, (Modifiers.notNull,)))
										)
						]
'''
Created on Jan 16, 2016

@author: Me
'''
import constants

#Specifies what version of the schema definition this is.
version = (1, 0)

#Specifies the valid SQL data types.
class Types:
	int = "INT"
	float = "FLOAT"
	numeric = "NUMERIC"
	bool = "BOOLEAN"
	varchar = "VARCHAR"
	char = "CHAR"
	text = "TEXT"
	timestamp = "TIMESTAMP"
	timestampTimeZone = "TIMESTAMP WITH TIME ZONE"
	date = "DATE"
	time = "TIME"
	timeTimeZone = "TIME WITH TIME ZONE"
	interval = "INTERVAL"

#Specifies valid column modifiers.
class Modifiers:
	notNull = "NOT NULL"
	unique = "UNIQUE"
	primaryKey = "PRIMARY KEY"
	references = "REFERENCES"
	onDeleteRestrict = "ON DELETE RESTRICT"
	onDeleteCascade = "ON DELETE CASCADE"
	onUpdateRestrict = "ON UPDATE RESTRICT"
	onUpdateCascade = "ON UPDATE CASCADE"
	nullDefault = "NULL"

class Schema(object):
	def __init__(self, pName, pColumns):
		self.SchemaName = pName
		self.SchemaColumns = pColumns

class DatabaseDefinition(object):
	def __init__(self):
		self.Name = ""
		self.AllSchemas = {}

#Describes all GDW tables.
class GDWSchemas(DatabaseDefinition):
	def __init__(self):
		self.Name = constants.kGDWDatabaseName
		self.AllSchemas = [
						Schema("celestial_types",
												(("id", Types.int, (Modifiers.primaryKey,)),
												("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
												("is_star", Types.bool, (Modifiers.notNull,)))
												),
						Schema("ring_types",
											(("id", Types.int, (Modifiers.primaryKey,)),
											("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
											),
						Schema("celestial_relationships",
														(("id", Types.int, (Modifiers.primaryKey,)),
														("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
														),
						Schema("governments",
											(("id", Types.int, (Modifiers.primaryKey,)),
											("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
											("generates_police", Types.bool, (Modifiers.notNull,)))
											),
						Schema("economies",
											(("id", Types.int, (Modifiers.primaryKey,)),
											("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
											),
						Schema("superpowers",
											(("id", Types.int, (Modifiers.primaryKey,)),
											("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
											),
						Schema("cz_intensities",
												(("id", Types.int, (Modifiers.primaryKey,)),
												("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
												),
						Schema("global_states",
												(("id", Types.int, (Modifiers.primaryKey,)),
												("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
												),
						Schema("system_states",
												(("id", Types.int, (Modifiers.primaryKey,)),
												("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
												),
						Schema("factions",
										(("id", Types.int, (Modifiers.primaryKey,)),
										("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
										("government", Types.int, (Modifiers.notNull, (Modifiers.references, "governments"))),
										("superpower", Types.int, (Modifiers.notNull, (Modifiers.references, "superpowers"))),
										("current_global_state", Types.int, (Modifiers.notNull, (Modifiers.references, "global_states"))),
										("pending_global_state", Types.int, (Modifiers.notNull, (Modifiers.references, "global_states"))))
										),
						Schema("systems",
										(("id", Types.int, (Modifiers.primaryKey,)),
										("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
										("coord_x", Types.float, ()),
										("coord_y", Types.float, ()),
										("coord_z", Types.float, ()),
										("owning_faction", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))))
										),
						Schema("system_celestials",
													(("id", Types.int, (Modifiers.primaryKey,)),
													("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
													("celestial_type", Types.int, (Modifiers.notNull, (Modifiers.references, "celestial_types"))),
													("ring_type", Types.int, (Modifiers.notNull, (Modifiers.references, "ring_types"))),
													("distance_from_entry_point", Types.float, ()))
													),
						Schema("structures",
											(("id", Types.int, (Modifiers.primaryKey,)),
											("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
											("owning_faction", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))),
											("economy", Types.int, (Modifiers.notNull, (Modifiers.references, "economies"))),
											("celestial", Types.int, (Modifiers.notNull, (Modifiers.references, "system_celestials"))),
											("distance_from_celestial", Types.float, ()),
											("celestial_relationship", Types.int, (Modifiers.notNull, (Modifiers.references, "celestial_relationships"))))
											),
						Schema("wars",
									(("id", Types.int, (Modifiers.primaryKey,)),
									("faction_1", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))),
									("faction_2", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))),
									("war_start", Types.timestamp, (Modifiers.notNull,)),
									("war_end", Types.timestamp, ()))
									),
						Schema("conflict_zones",
												(("id", Types.int, (Modifiers.primaryKey,)),
												("celestial", Types.int, (Modifiers.notNull, (Modifiers.references, "system_celestials"))),
												("distance_from_celestial", Types.float, ()),
												("intensity", Types.int, (Modifiers.notNull, (Modifiers.references, "cz_intensities"))),
												("war", Types.int, (Modifiers.notNull, (Modifiers.references, "wars"))),
												("faction_1_deployed_cap_ship", Types.bool, (Modifiers.notNull,)),
												("faction_2_deployed_cap_ship", Types.bool, (Modifiers.notNull,)),
												("is_visible", Types.bool, (Modifiers.notNull,)),
												("last_updated", Types.timestamp, (Modifiers.notNull,)))
												),
						Schema("factions_in_system",
													(("id", Types.int, (Modifiers.primaryKey,)),
													("factions", Types.int, (Modifiers.notNull, (Modifiers.references, "factions"))),
													("influence", Types.float, (Modifiers.notNull,)),
													("current_system_state", Types.int, (Modifiers.notNull, (Modifiers.references, "system_states"))),
													("pending_system_state", Types.int, (Modifiers.notNull, (Modifiers.references, "system_states"))),
													("entered_system_date", Types.timestamp, ()),
													("left_system_date", Types.timestamp, ()),
													("last_updated_date", Types.timestamp, (Modifiers.notNull,)))
													)
						]

#Describes all RDA tables.
class RDASchemas(DatabaseDefinition):
	def __init__(self):
		self.Name = constants.kRDADatabaseName
		self.AllSchemas = [
						Schema("event_types",
											(("id", Types.int, (Modifiers.primaryKey,)),
											("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax))
											),
						Schema("player_info",
											(("id", Types.int, (Modifiers.primaryKey,)),
											("user_id", Types.int, ()),
											("elite_name", Types.varchar, (), constants.kSchemaNameLenMax))
											),
						Schema("events",
										(("id", Types.int, (Modifiers.primaryKey,)),
										("event_date", Types.timestamp, (Modifiers.notNull,)))
										)
						]
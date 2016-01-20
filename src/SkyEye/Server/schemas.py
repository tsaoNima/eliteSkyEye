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
	schemaName = ""
	schemaColumns = ()
	def __init__(self, pName, pColumns):
		self.schemaName = pName
		self.schemaColumns = pColumns

#Describes all GDW tables.
class GDWSchemas:
	celestial_types = Schema("celestial_types",
						(("id", Types.int, (Modifiers.primaryKey,)),
						("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
						("is_star", Types.bool, (Modifiers.notNull,)))
						)
	ring_types = Schema("ring_types",
					(
			("id", Types.int, (Modifiers.primaryKey,)),
			("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
			))
	celestial_relationships = Schema("celestial_relationships",
								(
					("id", Types.int, (Modifiers.primaryKey,)),
					("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
					))
	governments = Schema("governments", (
				("id", Types.int, (Modifiers.primaryKey,)),
				("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
				("generates_police", Types.bool, (Modifiers.notNull,))
				))
	economies = Schema("economies", (
				("id", Types.int, (Modifiers.primaryKey,)),
				("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				))
	superpowers = Schema("superpowers", (
				("id", Types.int, (Modifiers.primaryKey,)),
				("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				))
	cz_intensities = Schema("cz_intensities", (
					("id", Types.int, (Modifiers.primaryKey,)),
					("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
					))
	global_states = Schema("global_states", (
				("id", Types.int, (Modifiers.primaryKey,)),
				("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				))
	system_states = Schema("system_states", (
				("id", Types.int, (Modifiers.primaryKey,)),
				("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				))
	factions = Schema("factions", (
			("id", Types.int, (Modifiers.primaryKey,)),
			("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
			("government", Types.int, (Modifiers.notNull, (Modifiers.references, governments.schemaName))),
			("superpower", Types.int, (Modifiers.notNull, (Modifiers.references, superpowers.schemaName))),
			("current_global_state", Types.int, (Modifiers.notNull, (Modifiers.references, global_states.schemaName))),
			("pending_global_state", Types.int, (Modifiers.notNull, (Modifiers.references, global_states.schemaName)))
			))
	systems = Schema("systems", (
			("id", Types.int, (Modifiers.primaryKey,)),
			("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
			("coord_x", Types.float, ()),
			("coord_y", Types.float, ()),
			("coord_z", Types.float, ()),
			("owning_faction", Types.int, (Modifiers.notNull, (Modifiers.references, factions.schemaName)))
			))
	system_celestials = Schema("system_celestials", (
					("id", Types.int, (Modifiers.primaryKey,)),
					("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
					("celestial_type", Types.int, (Modifiers.notNull, (Modifiers.references, celestial_types.schemaName))),
					("ring_type", Types.int, (Modifiers.notNull, (Modifiers.references, ring_types.schemaName))),
					("distance_from_entry_point", Types.float, ())
					))
	structures = Schema("structures", (
				("id", Types.int, (Modifiers.primaryKey,)),
				("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
				("owning_faction", Types.int, (Modifiers.notNull, (Modifiers.references, factions.schemaName))),
				("economy", Types.int, (Modifiers.notNull, (Modifiers.references, economies.schemaName))),
				("celestial", Types.int, (Modifiers.notNull, (Modifiers.references, system_celestials.schemaName))),
				("distance_from_celestial", Types.float, ()),
				("celestial_relationship", Types.int, (Modifiers.notNull, (Modifiers.references, celestial_relationships.schemaName)))
				))
	wars = Schema("wars", (
		("id", Types.int, (Modifiers.primaryKey,)),
		("faction_1", Types.int, (Modifiers.notNull, (Modifiers.references, factions.schemaName))),
		("faction_2", Types.int, (Modifiers.notNull, (Modifiers.references, factions.schemaName))),
		("war_start", Types.timestamp, (Modifiers.notNull,)),
		("war_end", Types.timestamp, ()),
		))
	conflict_zones = Schema("conflict_zones", (
				("id", Types.int, (Modifiers.primaryKey,)),
				("celestial", Types.int, (Modifiers.notNull, (Modifiers.references, system_celestials.schemaName))),
				("distance_from_celestial", Types.float, ()),
				("intensity", Types.int, (Modifiers.notNull, (Modifiers.references, cz_intensities.schemaName))),
				("war", Types.int, (Modifiers.notNull, (Modifiers.references, wars.schemaName))),
				("faction_1_deployed_cap_ship", Types.bool, (Modifiers.notNull,)),
				("faction_2_deployed_cap_ship", Types.bool, (Modifiers.notNull,)),
				("is_visible", Types.bool, (Modifiers.notNull,)),
				("last_updated", Types.timestamp, (Modifiers.notNull,))
				))
	factions_in_system = Schema("factions_in_system", (
					("id", Types.int, (Modifiers.primaryKey,)),
					("factions", Types.int, (Modifiers.notNull, (Modifiers.references, factions.schemaName))),
					("influence", Types.float, (Modifiers.notNull,)),
					("current_system_state", Types.int, (Modifiers.notNull, (Modifiers.references, system_states.schemaName))),
					("pending_system_state", Types.int, (Modifiers.notNull, (Modifiers.references, system_states.schemaName))),
					("entered_system_date", Types.timestamp, ()),
					("left_system_date", Types.timestamp, ()),
					("last_updated_date", Types.timestamp, (Modifiers.notNull,))
					))

#Describes all RDA tables.
class RDASchemas:
	event_types = Schema("event_types", (
				("id", Types.int, (Modifiers.primaryKey,)),
				("name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				))
	player_info = Schema("player_info", (
				("id", Types.int, (Modifiers.primaryKey,)),
				("user_id", Types.int, ()),
				("elite_name", Types.varchar, (), constants.kSchemaNameLenMax)
				))
	events = Schema("events", (
			("id", Types.int, (Modifiers.primaryKey,)),
			("event_date", Types.timestamp, (Modifiers.notNull,))
			))
'''
Created on Jan 16, 2016

@author: Me
'''
import constants

#Specifies what version of the schema definition this is.
version = (1, 0)

#Specifies the valid SQL data types.
class Types:
	int = "int"
	float = "float"
	numeric = "numeric"
	bool = "boolean"
	varchar = "varchar"
	char = "char"
	text = "text"
	timestamp = "timestamp"
	timestampTimeZone = "timestamp with time zone"
	date = "date"
	time = "time"
	timeTimeZone = "time with time zone"
	interval = "interval"

#Specifies valid column modifiers.
class Modifiers:
	notNull = "not null"
	unique = "unique"
	primaryKey = "primary key"
	references = "references"
	onDeleteRestrict = "on delete restrict"
	onDeleteCascade = "on delete cascade"
	onUpdateRestrict = "on update restrict"
	onUpdateCascade = "on update cascade"
	nullDefault = "null"

class Schema(object):
	schemaName = ""
	schemaColumns = ()
	def __init__(self, pName, pColumns):
		self.schemaName = pName
		self.schemaColumns = pColumns

#Describes all GDW tables.
class GDWSchemas:
	celestialType = Schema("celestialType",
						(("Id", Types.int, (Modifiers.primaryKey,)),
						("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
						("IsStar", Types.bool, (Modifiers.notNull,)))
						)
	ringType = Schema("ringType",
					(
			("Id", Types.int, (Modifiers.primaryKey,)),
			("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
			))
	celestialRelationship = Schema("celestialRelationship",
								(
					("Id", Types.int, (Modifiers.primaryKey,)),
					("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
					))
	government = Schema("government", (
				("Id", Types.int, (Modifiers.primaryKey,)),
				("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
				("GeneratesPolice", Types.bool, (Modifiers.notNull,))
				))
	economy = Schema("economy", (
				("Id", Types.int, (Modifiers.primaryKey,)),
				("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				))
	superpower = Schema("superpower", (
				("Id", Types.int, (Modifiers.primaryKey,)),
				("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				))
	czIntensity = Schema("czIntensity", (
					("Id", Types.int, (Modifiers.primaryKey,)),
					("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
					))
	globalState = Schema("globalState", (
				("Id", Types.int, (Modifiers.primaryKey,)),
				("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				))
	systemState = Schema("systemState", (
				("Id", Types.int, (Modifiers.primaryKey,)),
				("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				))
	faction = Schema("faction", (
			("Id", Types.int, (Modifiers.primaryKey,)),
			("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
			("Government", Types.int, (Modifiers.notNull, (Modifiers.references, government.schemaName))),
			("Superpower", Types.int, (Modifiers.notNull, (Modifiers.references, superpower.schemaName))),
			("CurrentGlobalState", Types.int, (Modifiers.notNull, (Modifiers.references, globalState.schemaName))),
			("PendingGlobalState", Types.int, (Modifiers.notNull, (Modifiers.references, globalState.schemaName)))
			))
	system = Schema("system", (
			("Id", Types.int, (Modifiers.primaryKey,)),
			("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
			("CoordX", Types.float, ()),
			("CoordY", Types.float, ()),
			("CoordZ", Types.float, ()),
			("OwningFaction", Types.int, (Modifiers.notNull, (Modifiers.references, faction.schemaName)))
			))
	systemCelestial = Schema("systemCelestial", (
					("Id", Types.int, (Modifiers.primaryKey,)),
					("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
					("CelestialType", Types.int, (Modifiers.notNull, (Modifiers.references, celestialType.schemaName))),
					("RingType", Types.int, (Modifiers.notNull, (Modifiers.references, ringType.schemaName))),
					("DistanceFromEntryPoint", Types.float, ())
					))
	structure = Schema("structure", (
				("Id", Types.int, (Modifiers.primaryKey,)),
				("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax),
				("OwningFaction", Types.int, (Modifiers.notNull, (Modifiers.references, faction.schemaName))),
				("Economy", Types.int, (Modifiers.notNull, (Modifiers.references, economy.schemaName))),
				("Celestial", Types.int, (Modifiers.notNull, (Modifiers.references, systemCelestial.schemaName))),
				("DistanceFromCelestial", Types.float, ()),
				("CelestialRelationship", Types.int, (Modifiers.notNull, (Modifiers.references, celestialRelationship.schemaName)))
				))
	war = Schema("war", (
		("Id", Types.int, (Modifiers.primaryKey,)),
		("Faction1", Types.int, (Modifiers.notNull, (Modifiers.references, faction.schemaName))),
		("Faction2", Types.int, (Modifiers.notNull, (Modifiers.references, faction.schemaName))),
		("WarStart", Types.timestamp, (Modifiers.notNull,)),
		("WarEnd", Types.timestamp, ()),
		))
	conflictZone = Schema("conflictZone", (
				("Id", Types.int, (Modifiers.primaryKey,)),
				("Celestial", Types.int, (Modifiers.notNull, (Modifiers.references, systemCelestial.schemaName))),
				("DistanceFromCelestial", Types.float, ()),
				("Intensity", Types.int, (Modifiers.notNull, (Modifiers.references, czIntensity.schemaName))),
				("War", Types.int, (Modifiers.notNull, (Modifiers.references, war.schemaName))),
				("Faction1DeployedCapShip", Types.bool, (Modifiers.notNull,)),
				("Faction2DeployedCapShip", Types.bool, (Modifiers.notNull,)),
				("IsVisible", Types.bool, (Modifiers.notNull,)),
				("LastUpdated", Types.timestamp, (Modifiers.notNull,))
				))
	factionInSystem = Schema("factionInSystem", (
					("Id", Types.int, (Modifiers.primaryKey,)),
					("Faction", Types.int, (Modifiers.notNull, (Modifiers.references, faction.schemaName))),
					("Influence", Types.float, (Modifiers.notNull,)),
					("CurrentSystemState", Types.int, (Modifiers.notNull, (Modifiers.references, systemState.schemaName))),
					("PendingSystemState", Types.int, (Modifiers.notNull, (Modifiers.references, systemState.schemaName))),
					("EnteredSystemDate", Types.timestamp, ()),
					("LeftSystemDate", Types.timestamp, ()),
					("LastUpdatedDate", Types.timestamp, (Modifiers.notNull,))
					))

#Describes all RDA tables.
class RDASchemas:
	eventType = (
				("Id", Types.int, (Modifiers.primaryKey,)),
				("Name", Types.varchar, (Modifiers.notNull,), constants.kSchemaNameLenMax)
				)
	playerInfo = (
				("Id", Types.int, (Modifiers.primaryKey,)),
				("UserId", Types.int, ()),
				("EliteName", Types.varchar, (), constants.kSchemaNameLenMax)
				)
	event = (
			("Id", Types.int, (Modifiers.primaryKey,)),
			("EventDate", Types.timestamp, (Modifiers.notNull,))
			)
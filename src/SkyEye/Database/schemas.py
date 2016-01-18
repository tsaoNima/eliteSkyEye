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

#Describes all GDW tables.
class GDWSchemas:
	celestialType = (
					("id", Types.int, (Modifiers.primaryKey)),
					("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax),
					("isStar", Types.bool, (Modifiers.notNull))
					)
	ringType = (
			("id", Types.int, (Modifiers.primaryKey)),
			("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax)
			)
	celestialRelationship = (
					("id", Types.int, (Modifiers.primaryKey)),
					("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax)
					)
	government = (
				("id", Types.int, (Modifiers.primaryKey)),
				("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax),
				("generatesPolice", Types.bool, (Modifiers.notNull))
				)
	economy = (
				("id", Types.int, (Modifiers.primaryKey)),
				("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax)
				)
	superpower = (
				("id", Types.int, (Modifiers.primaryKey)),
				("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax)
				)
	czIntensity = (
					("id", Types.int, (Modifiers.primaryKey)),
					("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax)
					)
	globalState = (
				("id", Types.int, (Modifiers.primaryKey)),
				("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax)
				)
	systemState = (
				("id", Types.int, (Modifiers.primaryKey)),
				("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax)
				)
	faction = (
			("id", Types.int, (Modifiers.primaryKey)),
			("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax),
			("government", Types.int, (Modifiers.notNull, (Modifiers.references, government))),
			("superpower", Types.int, (Modifiers.notNull, (Modifiers.references, superpower))),
			("currentGlobalState", Types.int, (Modifiers.notNull, (Modifiers.references, globalState))),
			("pendingGlobalState", Types.int, (Modifiers.notNull, (Modifiers.references, globalState)))
			)
	system = (
			("id", Types.int, (Modifiers.primaryKey)),
			("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax)
			("coordX", Types.float, ()),
			("coordY", Types.float, ()),
			("coordZ", Types.float, ()),
			("owningFaction", Types.int, (Modifiers.notNull, (Modifiers.references, faction)))
			)
	systemCelestial = (
					("id", Types.int, (Modifiers.primaryKey)),
					("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax),
					("celestialType", Types.int, (Modifiers.notNull, (Modifiers.references, celestialType))),
					("ringType", Types.int, (Modifiers.notNull, (Modifiers.references, ringType))),
					("distanceFromEntryPoint", Types.float, ())
					)
	structure = (
				("id", Types.int, (Modifiers.primaryKey)),
				("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax),
				("owningFaction", Types.int, (Modifiers.notNull, (Modifiers.references, faction))),
				("economy", Types.int, (Modifiers.notNull, (Modifiers.references, economy))),
				("celestial", Types.int, (Modifiers.notNull, (Modifiers.references, systemCelestial))),
				("distanceFromCelestial", Types.float, ())
				("celestialRelationship", Types.int, (Modifiers.notNull, (Modifiers.references, celestialRelationship)))
				)
	war = (
		("id", Types.int, (Modifiers.primaryKey)),
		("faction1", Types.int, (Modifiers.notNull, (Modifiers.references, faction))),
		("faction2", Types.int, (Modifiers.notNull, (Modifiers.references, faction))),
		("warStart", Types.timestamp, (Modifiers.notNull)),
		("warEnd", Types.timestamp, ()),
		)
	conflictZone = (
				("id", Types.int, (Modifiers.primaryKey)),
				("celestial", Types.int, (Modifiers.notNull, (Modifiers.references, systemCelestial))),
				("distanceFromCelestial", Types.float, ()),
				("intensity", Types.int, (Modifiers.notNull, (Modifiers.references, czIntensity))),
				("war", Types.int, (Modifiers.notNull, (Modifiers.references, war))),
				("faction1DeployedCapShip", Types.bool, (Modifiers.notNull)),
				("faction2DeployedCapShip", Types.bool, (Modifiers.notNull)),
				("isVisible", Types.bool, (Modifiers.notNull)),
				("lastUpdated", Types.timestamp, (Modifiers.notNull))
				)
	factionInSystem = (
					("id", Types.int, (Modifiers.primaryKey)),
					("faction", Types.int, (Modifiers.notNull, (Modifiers.references, faction))),
					("influence", Types.float, (Modifiers.notNull)),
					("currentSystemState", Types.int, (Modifiers.notNull, (Modifiers.references, systemState))),
					("pendingSystemState", Types.int, (Modifiers.notNull, (Modifiers.references, systemState))),
					("enteredSystemDate", Types.timestamp, ()),
					("leftSystemDate", Types.timestamp, ()),
					("lastUpdatedDate", Types.timestamp, (Modifiers.notNull))
					)
	

#Describes all RDA tables.
class RDASchemas:
	eventType = (
				("id", Types.int, (Modifiers.primaryKey)),
				("name", Types.varchar, (Modifiers.notNull), constants.kSchemaNameLenMax)
				)
	playerInfo = (
				("id", Types.int, (Modifiers.primaryKey)),
				("userId", Types.int, ()),
				("eliteName", Types.varchar, (), constants.kSchemaNameLenMax)
				)
	event = (
			("id", Types.int, (Modifiers.primaryKey)),
			("eventDate", Types.timestamp, (Modifiers.notNull))
			)
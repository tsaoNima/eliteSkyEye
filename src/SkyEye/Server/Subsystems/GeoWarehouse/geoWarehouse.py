'''
Created on Jan 26, 2016

@author: Me
'''
from ..subsystemBase import SubsystemBase
from SkyEye.Logging import log
from dbDefinition import GDWSchemas

sLog = log.GetLogInstance()

class GeoWarehouse(SubsystemBase):
	"""Subsystem for the geographic data warehouse (GDW).
	"""

	def onStart(self):
		"""Called when Start() is called.
		Subclasses should override this.
		"""
		pass
	
	def onShutdown(self):
		"""Called when Shutdown() is called
		but before the database connection is closed.
		Subclasses should override this.
		"""
		pass
	
	def onSetup(self):
		#Create metatables to assist in merging:
		#	* A dimension table listing all possible update sources. Should really be
		#	defined in the DB definition to allow us to setup default values
		#	("None" should be a possible source). Should contain:
		#		* Source name (string)
		#	* For each mergeable table, create a corresponding LastUpdatedBy metatable.
		#	Each such metatable should contain:
		#		* The date of the last update (datetime with timezone)
		#		* The ID of the respective record (int FK)
		#		* For each column in the data table,
		#		a column recording the source of the updater (int FK)
		pass
	
	def eddbImport(self):
		#systems.json is a really big file, needs to be split up or streamed in somehow.
		#In any case, has data for each system.
		#It's 23 MB, so we want to stream it.
		#For each system:
		#	* If the system isn't already in the GDW, insert it.
		#	* If the system does exist:
		#		* Find any columns that were NOT last updated by a SkyEye user,
		#		mark those for overwrite via update. Since a column can have no
		#		data source, this also covers NULL cells.
		pass
	
	def insertSystem(self, dataSourceId):
		#Do the INSERT query.
		#For each value we set, mark the update source in the metarow.
		#Do the metatable's INSERT query.
		pass
	
	def updateSystem(self, dataSourceId):
		#Basically consider each element besides the update source optional.
		#Whatever was given a value we then later update the meta for.
		#Do the UPDATE query.
		#For each value we set, mark the update source in the metarow.
		#Do the metatable's UPDATE query.
		pass
	
	def __init__(self):
		schema = GDWSchemas()
		super(GeoWarehouse, self).__init__(schema.Name, schema)
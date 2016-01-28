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
		#Generate default values.
		pass
	
	def eddbImport(self):
		#systems.json is a really big file, needs to be split up or streamed in somehow.
		#In any case, has data for each system.
		#Figure out what data the import can overwrite.
		#Figure out which systems need overwriting.
		#For those systems:
			#Overwrite with EDDB's data.
		pass
	
	def __init__(self):
		schema = GDWSchemas()
		super(GeoWarehouse, self).__init__(schema.Name, schema)
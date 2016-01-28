'''
Created on Jan 26, 2016

@author: Me
'''

kTagSubsystemBase = "SubsystemBase"

kMethodCreate = "SubsystemBase.Create()"
kMethodSetup = "SubsystemBase.Setup()"
kMethodVerify = "SubsystemBase.Verify()"
kMethodStart = "SubsystemBase.Start()"
kMethodShutdown = "SubsystemBase.Shutdown()"

kErrFmtNoDBDefinition = "Database definition not set, {0}!"
kErrFmtCreateNeedsDBDefinition = kErrFmtNoDBDefinition.format("can't create subsystem {0}")
kErrFmtSetupNeedsDBDefinition = kErrFmtNoDBDefinition.format("can't setup subsystem {0}")
kErrFmtVerifyNeedsDBDefinition = kErrFmtNoDBDefinition.format("can't verify subsystem {0}")
kErrFmtStartNeedsDBDefinition = kErrFmtNoDBDefinition.format("can't connect to subsystem {0}")
kErrFmtDropNeedsDBDefinition = kErrFmtNoDBDefinition.format("can't drop subsystem {0}")
kFmtStartingSubsystem = "Starting subsystem '{0}'..."
kFmtStartedSubsystem = "Started subsystem '{0}'."
kFmtShuttingDownSubsystem = "Shutting down subsystem '{0}'..."
kFmtShutDownSubsystem = "Shut down subsystem '{0}'."
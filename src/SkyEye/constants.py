'''
Created on Jan 15, 2016

@author: Me
'''

kSkyEyeDefaultOutPath = "./skyEye.log"
kSkyEyeDefaultSettingsPath = "./settings.yml"

kInitSettings = "Loading settings..."
kInitFirstBoot = "It looks like this is the first time SkyEye's been run, starting first run setup."
kInitServerLogin = "Logging in to databases..."
kInitVerifyServer = "Verifying server tables..."
kInitServer = "Connecting to internal services..."
kInitIO = "Connecting to external I/O services..."
kErrSetupTablesLogInitFailed = "main(): Couldn't setup logger, aborting!"
kErrSkyEyeInitFailed = "main(): Initialization failed, aborting!"
kFmtErrSkyEyeLogOpenFailed = "Couldn't open log file {0}, disabling log file dumping!"
kFmtErrSkyEyeSettingsOpenFailed = "Couldn't open settings file {0}! Loading default settings."
kFmtErrSkyEyeSettingsSaveFailed = "Couldn't save settings file {0}!"
kFmtReason = "Reason: {0}"
kErrLoginFailed = "Couldn't login to server!"
kWarnServerVerifyFailed = "Server tables don't match expected schema!"
kServerInitComplete = "Server init complete."
kServerShutdownStarted = "Server is going down NOW!"
kShutdownSettings = "Saving settings..."
kShutdownServer = "Disconnecting from internal services..."
kShutdownIO = "Disconnecting from external I/O services..."

kTagSkyEye = "SkyEyeDaemon"

kMethodInit = "SkyEyeDaemon.__init__()"
kMethodRun = "SkyEyeDaemon.Run()"
kMethodShutdown = "SkyEyeDaemon.Shutdown()"
kMethodLoadSettings = "SkyEyeDaemon.loadSettings()"
kMethodSaveSettings = "SkyEyeDaemon.saveSettings()"

#Settings.
kDefaultSettings = """\
#If true, this is the first time SkyEye has been run on this machine.
firstRun: True
"""

kSettingsFirstRun = "firstRun"
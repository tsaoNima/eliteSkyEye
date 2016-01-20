'''
Created on Jan 15, 2016

@author: Me
'''

kSkyEyeDefaultOutPath = "./skyEye.log"
kSetupTablesDefaultOutPath = "./setupTables.log"

kErrNewCredentialsFailed = "Server.requestNewCredentials(): Aborting new credential request!"
kErrSetupTablesLogInitFailed = "main(): Couldn't setup logger, aborting!"
kErrSkyEyeInitFailed = "main(): Initialization failed, aborting!"
kFmtErrSkyEyeLogOpenFailed = "SkyEyeDaemon.__init__(): Couldn't open log file {0}, disabling log file dumping!"
kFmtReason = "Reason: {0}"

#For server.py.
kGDWDatabaseName = "GeoDataWarehouse"
kRDADatabaseName = "ReconDataAnalyzer"
kServerDBAdminName = "sky_eye_admin"

kPromptNewDBPassword = "Please enter a new password for the database admin account: "
kMaxNumPrompts = 3

kErrLoginFailed = "Aborting login!"
kErrCredentialRequestFailed = "Couldn't get new credentials!"
kErrTooManyPromptsFailed = "Login attempts exceeded, aborting login!"

kMethodRequestNewCredentials = "Server.requestNewCredentials()"
kMethodLogin = "Server.Login()"
kMethodGetCredentials = "Server.getCredentials()"

kTagServer = "Server"
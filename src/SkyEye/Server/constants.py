'''
Created on Jan 19, 2016

@author: Me
'''
kGDWDatabaseName = "GeoDataWarehouse"
kRDADatabaseName = "ReconDataAnalyzer"
kServerDBAdminName = "sky_eye_admin"

kPromptNewDBPassword = "Please enter a new password for the database admin account: "
kMaxNumPrompts = 3

kErrNewCredentialsFailed = "Aborting new credential request!"
kErrLoginFailed = "Aborting login!"
kErrCredentialRequestFailed = "Couldn't get new credentials!"
kErrTooManyPromptsFailed = "Login attempts exceeded, aborting login!"
kErrNotLoggedIn = "Not logged in, can't complete request!"
kErrNoAdminPassword = "Database admin password not set!"
kLoginComplete = "Administrator connected to server."
kLogoutComplete = "Administrator has logged out."

#Setup strings.
kFirstTimeSetupStarting = "Entering server setup..."
kFirstTimeSetupWarnDataLoss = "Warning - any existing data and users will be lost!"
kFirstTimeSetupCreatingDBAdmin = "Creating database administrator account..."
kFirstTimeSetupDBAdminCreated = "Database administrator account created."
kFirstTimeSetupComplete = "Server setup complete."

kMethodRequestNewCredentials = "Server.requestNewCredentials()"
kMethodLogin = "Server.Login()"
kMethodLogout = "Server.Logout()"
kMethodGetCredentials = "Server.getCredentials()"
kMethodFirstTimeSetup = "Server.FirstTimeSetup()"

kTagServer = "Server"

kFmtErrDBConnectionFailed = "Couldn't connect to database {0}, aborting!"

kMethodIterateTables = "setupTables.iterateTables()"
kTagSetupTables = "SetupTables"
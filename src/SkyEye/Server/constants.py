'''
Created on Jan 19, 2016

@author: Me
'''
kSchemaNameLenMax = 255

kGDWDatabaseName = "geo_data_warehouse"
kRDADatabaseName = "recon_data_analyzer"
kSubsystemNames = (kGDWDatabaseName, kRDADatabaseName)
kServerDBAdminName = "sky_eye_admin"

kSysAdminDatabaseName = "postgres"
kSysAdminUserName = "postgres"

kPromptNewDBPassword = "Please enter a new password for the database admin account: "
kMaxNumPrompts = 3

kErrNewCredentialsFailed = "Aborting new credential request!"
kErrLoginFailed = "Aborting login!"
kErrCredentialRequestFailed = "Couldn't get new credentials!"
kErrTooManyPromptsFailed = "Login attempts exceeded, aborting login!"
kErrNotLoggedIn = "Not logged in, can't complete request!"
kErrNoAdminPassword = "Database admin password not set!"
kFmtErrBadCredentials = "User name or password invalid for user {0}!"
kLoginComplete = "Administrator connected to server."
kLogoutComplete = "Administrator has logged out."

#Setup strings.
kFirstTimeSetupStarting = "Entering server setup..."
kFirstTimeSetupWarnDataLoss = "Warning - any existing data and users will be lost!"
kFirstTimeSetupPromptSysAdminPassword = "Please enter the password for database user \"{0}\"".format(kSysAdminUserName)
kFirstTimeSetupErrSysAdminPasswordInvalid = "Password invalid."
kFirstTimeSetupCreatingDBAdmin = "Creating database administrator account..."
kFirstTimeSetupDBAdminCreated = "Database administrator account created."
kFirstTimeSetupComplete = "Server setup complete. You can now login to the server."
kFmtErrDBDropFailed = "Failed to drop database {0}!"

kMethodRequestNewCredentials = "Server.requestNewCredentials()"
kMethodLogin = "Server.Login()"
kMethodLogout = "Server.Logout()"
kMethodGetCredentials = "Server.getCredentials()"
kMethodFirstTimeSetup = "Server.FirstTimeSetup()"

kTagServer = "Server"

kFmtExcDropDatabaseFailed = "Failed to drop database {0}"
kFmtExcCreateDatabaseFailed = "Failed to create database {0}"
kFmtErrDBConnectionFailed = "Couldn't connect to database {0}, aborting!"
kWarnDroppingAllDatabases = "Dropping all databases!!!"
kFmtWarnDroppingTablesForDatabase = "Dropping all tables in database {0}!"
kWarnEnteringServerSetup = "Entering server setup. All data will be lost!"
kCreateTablesStarting = "Generating all database tables..."
kFmtCreatingTablesForDatabase = "Generating tables for database {0}..."
kVerifyAllDatabasesStarting = "Verifying databases..."
kFmtVerifyingTablesForDatabase = "Verifying tables for database {0}..."
kFmtWarnAdminDBConnectionAttempted = "Connection attempted to system administration database by user {0}"

kMethodIterateTables = "setupTables.iterateTables()"
kMethodConnectToSubsystem = "setupTables.connectToSubsystem()"
kMethodConnectToAdminDBAndRunOnAllSubsystems = "setupTables.connectToAdminDBAndRunOnAllSubsystems()"
kMethodVerifyTablesForDatabase = "setupTables.VerifyTablesForDatabase()"
kMethodDropTablesForDatabase = "setupTables.DropTablesForDatabase()"
kMethodSetupTablesForDatabase = "setupTables.SetupTablesForDatabase()"
kMethodVerifyDatabases = "setupTables.VerifyDatabases()"
kMethodDropDatabases = "setupTables.DropDatabases()"
kMethodSetupDatabases = "setupTables.SetupDatabases()"
kTagSetupTables = "SetupTables"
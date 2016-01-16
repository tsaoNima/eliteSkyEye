def startup():
	#Open the log file!
	
	#Open DB connection.
	#Make sure all the tables we need are actually there;
	#If not, generate defaults.
	
	#Establish connection to outputs (Discord, etc.)
	
	#Establish connection to inputs (HTTP API, etc.)
	#Report that we're open.
	
def shutdown():
	#Close any resources.

def main():
	#Do startup.
	startup()
	
	#Now start listening for events.
	
	#Do shutdown.
	shutdown()

#This is the entry point for the application.
if __name__ == "__main__":
	main()
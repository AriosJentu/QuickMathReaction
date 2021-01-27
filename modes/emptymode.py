class Empty:																	#Empty mode class
	"""
	Empty mode:
		Classes of this type need to contain next methods:
			__init__(self) 				- to initialize default values for game-object
			void set(self, **values) 	- to set specific parameters from initialization for game-object (needs to be universal by keyname and it's value): set(key=value)
			void set_defaults(self)		- to set default values of parameters
			dict get(self)				- to get parameters table with it's values: {"parameter":value, ...}
			string help(self)			- to get help information about mode and it's parameters
			set generate_task(self)		- to generate task of this game-object with it's parameters, set needs to contain 2 values - (string question, string answer)
	"""

	def __init__(self):															#Initialization function
		pass 

	def set(self, **values):													#Function to set current values for element of this class
		pass

	def set_defaults(self):														#Function to set default values
		pass

	def get(self):																#Function to get current values
		return {}

	def help(self):																#Function to print information about ariphmetic mode
		return "Basic empty mode"

	def generate_task(self):													#Function to generate task
		return "Empty task question", "answer"		


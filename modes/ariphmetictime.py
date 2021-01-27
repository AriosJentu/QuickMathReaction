from random import randint

class AriphmeticsTime:															#AriphmeticsTime mode class
	"""
	AriphmeticsTime mode:
		Classes of this type need to contain next methods:
			__init__(self) 				- to initialize default values for game-object
			void set(self, **values) 	- to set specific parameters from initialization for game-object (needs to be universal by keyname and it's value): set(key=value)
			void set_defaults(self)		- to set default values of parameters
			dict get(self)				- to get parameters table with it's values: {"parameter":value, ...}
			string help(self)			- to get help information about mode and it's parameters
			set generate_task(self)		- to generate task of this game-object with it's parameters, set needs to contain 2 values - (string question, string answer)
	"""
	MINTIME = 0
	MAXTIME = 900
	DIFFTIME = 400

	def __init__(self):															#Initialization function
		self.operations = "12"														#Game operations - Can contains [1 - adding time], [2 - subtracting time], [0 - starting time depens of difficulty]
		self.difficulty = 1															#Game difficulty - [1 - only +-30*k sec], [2 - for +-15*k sec], [3 - for +-25*k sec], [4 - for +-35*k sec], [5 - for +- 5*k sec], [6 - random]
		self.separate = False														#Game answer separator - enable or disable (if enable, answer will be for ex. "4:20", else same answer will be "420")
		self.enable_multiplicator = True											#Game multiplicator - enable or disable (if disabled, "k" in difficulty will be constantly "1", else - random)

	def set(self, operations=None, difficulty=None, separate=None, 
			multiplicator=None):												#Function to set current values for element of this class
		if operations:																#Set operations value if it's are not None
			self.operations = operations

		if difficulty:																#Set difficulty value
			self.difficulty = difficulty

		if separate != None and bool(separate) != self.separate:					#Set separator value
			self.separate = bool(separate)

		if multiplicator != None and\
				bool(multiplicator) != self.enable_multiplicator:					#Set enable_multiplicator value
			self.enable_multiplicator = bool(multiplicator)


	def set_defaults(self):														#Function to set default values
		self.operations = "12"
		self.difficulty = 1
		self.separate = False

	def get(self):																#Function to get current values
		return {
			"operations": self.operations,
			"difficulty": self.difficulty,
			"separate": self.separate
		}

	def help(self):																#Function to print information about ariphmetic mode
		return """Basic ariphmetic reaction test for timing with two values.
 Available Operations (can be merged, like "12", etc):
  >> 0 - Starting number depends on difficulty
  >> 1 - Adding time
  >> 2 - Subtracting time;
 Available Difficulties:
  >> 1 - Only +-30 seconds and it's multiplications;
  >> 2 - Only +-15 seconds and it's multiplications;
  >> 3 - Only +-25 seconds and it's multiplications;
  >> 4 - Only +-35 seconds and it's multiplications;
  >> 5 - Only +-5 seconds and it's multiplications;
  >> 6 - Random;
Current Operations: """+self.operations+""";
Current Difficulty: """+str(self.difficulty)+""";
Current Separation state: """+(
	["disabled", "enabled"][bool(self.separate)])+""";
Current Multiplicator state: """+(
	["disabled", "enabled"][bool(self.enable_multiplicator)])+""" (can be disabled only for 1-4 difficulties);"""

	def generate_task(self):													#Function to generate task

		def generate_time():														#Helping function to generate time from available variables in class
			left = randint(AriphmeticsTime.MINTIME,
				AriphmeticsTime.MAXTIME-AriphmeticsTime.DIFFTIME)						#Generating left time
			c = min(left*2, AriphmeticsTime.MAXTIME)									#Get minimal time from available and twice "a" to find right border of right time
			
			if left == 0:																	#If left time is 0, set right border to right time, because "c" is 0, and randint from 1 to 0 can't be possible 
				c = AriphmeticsTime.MAXTIME

			right = randint(left+1, c)													#Generate right time from left time and time above
			return left, right

		def convert_time_to_m_s_string(time, foranswer=False):						#Helping function to convert time in seconds to string with minutes and seconds
			mins = time//60
			secs = time%60

			if foranswer and not self.separate:											#If this is a convertion of time for answer, and its not separable - output specific time without separation
				if mins == 0:																#If there is no minutes - disable them
					mins = ""
				return str(mins)+"%.2i"%secs

			else:																		#If conversion is not for answer, or asnwer is separable - output with separator
				if mins == 0 and foranswer:													#If there is no minutes - disable them
					mins = ""
				else:
					mins = str(mins)+":"

				return mins+"%.2i"%secs

		diff_depends = "0" in self.operations 										#Variable to get information about depending difficulty in start time generation
		def apply_difficulty(start, diff):											#Function for calculating start and diff based on difficulty

			if self.difficulty == 1:												#If difficulty is 1 - difference has a multiplier 30, is difficulty-depending is enabled - start is a multiplier of 30
	
				if self.enable_multiplicator:
					diff = diff - diff%30
				else:
					diff = 30
	
				if diff_depends:
					start = start - start%30
	
			elif self.difficulty == 2:												#If difficulty is 2 - difference has a multiplier 15, is difficulty-depending is enabled - start is a multiplier of 15
	
				if self.enable_multiplicator:
					diff = diff - diff%15
				else:
					diff = 15
	
				if diff_depends:
					start = start - start%15

			elif self.difficulty == 3:												#If difficulty is 3 - difference has a multiplier 25, is difficulty-depending is enabled - start is a multiplier of 5
				if self.enable_multiplicator:
					diff = diff - diff%25
				else:
					diff = 25
	
				if diff_depends:
					start = start - start%5

			elif self.difficulty == 4:												#If difficulty is 4 - difference has a multiplier 35, is difficulty-depending is enabled - start is a multiplier of 5

				if self.enable_multiplicator:
					diff = diff - diff%35
				else:
					diff = 35
	
				if diff_depends:
					start = start - start%5

			elif self.difficulty == 5:												#If difficulty is 5 - difference has a multiplier 5, is difficulty-depending is enabled - start is a multiplier of 5
				diff = diff - diff%5
	
				if diff_depends:
					start = start - start%5

			if diff == 0 and self.difficulty < 6:									#If difference is 0 - it's not the best way to add/subtract 0 from initial time in 1-5 difficulties, set it as default
				diff = [60, 30, 15, 25, 35, 5][self.difficulty%6]

			return start, diff

		def get_time_for_add(left, right):											#Helping function to get start and diff from left and right times for adding
			return left, right-left

		def get_time_for_subtract(left, right):										#Helping function to get start and diff from left and right times for subtracting
			return right, right-left

		tasks = []
		answers = []
		left, right = generate_time()												#Generate time
		if "1" in self.operations:													#If there is adding operation in time
			start, diff = get_time_for_add(left, right)									#Get start and diff from generated time
			start, diff = apply_difficulty(start, diff)									#Apply to generated time difficulty parameters
			tasks.append(convert_time_to_m_s_string(start) + " + " 
						+ convert_time_to_m_s_string(diff))
			answers.append(convert_time_to_m_s_string(start+diff, True))

		if "2" in self.operations:													#If there is subtracting operation in time
			start, diff = get_time_for_subtract(left, right)							#Do the same thing, but for subtract
			start, diff = apply_difficulty(start, diff)
			tasks.append(convert_time_to_m_s_string(start) + " - " 
						+ convert_time_to_m_s_string(diff))
			answers.append(convert_time_to_m_s_string(start-diff, True))

		index = randint(0, len(tasks)-1)
		return tasks[index], answers[index]		


generator = AriphmeticsTime()
generator.set(operations="1", difficulty=4, multiplicator=False)
for i in range(500):
	print(generator.generate_task())
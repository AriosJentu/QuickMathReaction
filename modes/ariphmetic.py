from random import randint, choice

def randint_ex01(a, b):
	return choice([i for i in range(a, b+1) if i not in [0, 1]])

class Ariphmetics:																#Class for ariphmetic tasks
	"""
	Ariphmetic mode:
		Classes of this type need to contain next methods:
			__init__(self) 				- to initialize default values for game-object
			void set(self, **values) 	- to set specific parameters from initialization for game-object (needs to be universal by keyname and it's value): set(key=value)
			void set_defaults(self)		- to set default values of parameters
			dict get(self)				- to get parameters table with it's values: {"parameter":value, ...}
			string help(self)			- to get help information about mode and it's parameters
			set generate_task(self)		- to generate task of this game-object with it's parameters, set needs to contain 2 values - (string question, string answer)
	"""

	def __init__(self):															#Initialization function
		self.operations = "12" 														#Game operations - Can contain [1 - sums], [2 - diffs], [3 - prods], [4 - divs], [0 - only positives mode]
		self.range = [-50, 50]														#Game value ranges - Ranges for generating integers
		self.difficulty = 1 														#Game difficulty - [1 for only +-10*k], [2 for +-5*k], [3 for random] (where k is an integer multiplier)

	def set(self, operations=None, ranges=None, difficulty=None):				#Function to set current values for element of this class
		if operations:																#Set operations value, if it's not None
			self.operations = operations
		
		if ranges and len(ranges) == 2:												#Set ranges for generating, if them is not None, and size of them is 2
			self.range = ranges
			self.range = self._check_ranges(*self.range)							#Check integers for classical values

		if difficulty:																#Set difficulty if it's not none
			self.difficulty = difficulty

	def set_defaults(self):														#Function to set default values
		self.operations = "12"
		self.range = [-50, 50]
		self.difficulty = 1

	def get(self):																#Function to get current values
		return {
			"operations": self.operations,
			"range": self.range,
			"difficulty": self.difficulty
		}

	def _check_ranges(self, a, b):												#Function to check ranges
		if abs(b - a) < 3:															#If values are small enough, set right border to little bit higher (in case of difficulty)
			b += (self.difficulty%3 + 1)*10
		return [min(a, b), max(a, b)]	


	def help(self):																#Function to print information about ariphmetic mode
		return """Basic ariphmetic reaction test with two values.
 Available Operations (can be merged, like "12", etc):
  >> 0 - Only positive available values;
  >> 1 - Available summing;
  >> 2 - Available subtracting;
  >> 3 - Available multiplication;
  >> 4 - Available division;
 Available Difficulties:
  >> 1 - Only +-10 and multiplications;
  >> 2 - Only +-5 and multiplications;
  >> 3 - Random values from range;
Current available integer ranges:
 Min - """+str(min(self.range))+""";
 Max - """+str(max(self.range))+""";
Current Operations: """+self.operations+""";
Current Difficulty: """+str(self.difficulty)+""";"""


	def generate_task(self):													#Function to generate task
		if "0" in self.operations: 													#Operations only for positives mode
			self.range = [(i if i >= 0 else 0) for i in self.range]

		def turn_signs(b, ispositive):												#Helping function to switch signs for sum/diff (if second value is negative)
			arr = [" + ", " - "]
			if b < 0:
				return arr[int(ispositive)]
			else:
				return arr[int(not ispositive)]

		def use_difficulty(a, b):													#Helping function to generate numbers with a part of difficulty
			if self.difficulty == 1:													#For difficulty 1 it needs to have a multiplier of 10
				a = a - a%10
				b = b - b%10 + 10

			elif self.difficulty == 2:													#For difficulty 2 it needs to have a multiplier of 5
				a = a - a%5
				b = b - b%5 + 5

			return a, b

		def for_multiplication(a): 													#Helping function for multiplication, makes value a little bit smaller (for quickly multiplication of small numbers)
			if a > 20:
				return a//10 + a%10 + 10
			return a


		def use_multiplication(a, b):												#Helping function for multiplication, which applies difficulty for previous function
			a = for_multiplication(a)
			b = for_multiplication(b)
			a, b = use_difficulty(a, b)
			return self._check_ranges(a, b)

		a, b = randint_ex01(*self.range), randint_ex01(*self.range)					#Generate two random integers
		a, b = use_difficulty(a, b)
		a, b = self._check_ranges(a, b)
		
		tasks = []
		answers = []
		if "1" in self.operations: 													#If operations variable contains tasks for sums
			tasks.append(str(a) + turn_signs(b, True) + str(abs(b)))
			answers.append(a+b)

		if "2" in self.operations: 													#If operations variable contains tasks for diffs
			tasks.append(str(a) + turn_signs(b, False) + str(abs(b)))
			answers.append(a-b)

		if "3" in self.operations: 													#If operations variable contains tasks for prods
			a, b = use_multiplication(a, b)
			tasks.append(str(a) + " * " + str(b))
			answers.append(a*b)

		if "4" in self.operations: 													#If operations variable contains tasks for divs (based on prods, but with special variable, which is dividend)
			a, b = use_multiplication(a, b)
			if a == 0:																	#Multiplier "a" is a divisor, must not to be 0
				a = randint_ex01(-10, 10)
			s = a*b
			tasks.append(str(s) + " / " + str(a))
			answers.append(b)

		if len(tasks) == 0: 													#If there is fail for operations values, set it to default (1), and regenerate task
			self.set_defaults()
			return self.generate_task()

		index = randint(0, len(tasks)-1)
		return tasks[index], str(answers[index])								#Return task question and answer

"""
generator = Ariphmetics()
generator.set(operations="04", difficulty=3)
for _ in range(100):
	task, sol = generator.generate_task()
	print(task, sol)
"""
import curses
import os

stdout = []																		#Output array to save log information to print them then
class Window:																	#Class for special ncurses window

	"""
	Window:
		This class creates specific ncurses window with input mode.
		Needs to get available alphabet, backspace processing automatically
		Needs to responce user's input immediately
		Has callback function, when pressing key, called "onkeypress" with one argument - key. Called when user pressing key with function "readkey" or "readinput"
	"""

	alphabet = "-1234567890qbsx"												#Class available alphabet
	backspaces = ('KEY_BACKSPACE', '\b', '\x7f')								#Different variations of backspace keystring

	def __init__(self):															#Initialization of window class
		self.window = None															#By default there is no window at start
		self.key = ""																#Parameter for saving current pressed key
		self.word = ""																#Parameter for saving current word
		self.isdrawable = True														#Parameter for showing keypressed values like typing text
		self.onkeypress = lambda key: None											#Parameter callback function when key was pressed

	def init(self):																#Initialization of window with ncurses
		self.window = curses.initscr()												#Create screen

		curses.start_color()														#Initialize terminal color
		curses.use_default_colors()													#Set colors to defaults
		curses.noecho()																#Disable showing key typing by default, it will be configures manually with alphabet
		curses.cbreak()																#Available Ctrl+C for break application

		self.window.nodelay(True)													#Make no delay for keypressing

	def clear(self):															#Default clear ncurses screen
		self.window.clear()

	def write(self, string):													#Write string on screen
		self.window.addstr(string)

	def backspace(self):														#Backspace function for removing last char in ncurses screen
		y, x = self.window.getyx()													#Get current caret position on screen
		self.window.addstr(y, x-1, " ")												#Make previous value as empty space at this line
		self.window.move(y, x-1)													#Move caret to previous character at this line

	def readkey(self):															#Function to read key from ncurses												
		self.key = self.window.getkey()												#Reading key and saving it to the object parameter
		self.onkeypress(self.key)													#Call function "onkeypress" with current saved key
		return self.key

	def readinput(self):														#Function to read all input in current word
		self.readkey()																#Read key from input
		if self.key in CalculatorWindow.alphabet:									#If key in alphabet - add this key in word
			self.word += str(self.key)

		if self.isdrawable:															#If showing keypressed values available, and them in alphabet - draw this keys on screen
			if self.key in CalculatorWindow.alphabet:
				self.write(str(self.key))

			elif self.key in CalculatorWindow.backspaces and len(self.word) > 0:	#But if key not in alphabet, this key is backspace, and length of word is more than 0 (word is not empty)
				self.backspace()														#Apply backspace function
				self.word = self.word[:-1]												#And remove last char from word

		return self.word

	def clearinput(self):														#Function to clear word from input
		if self.isdrawable:															#If drawable - apply backspace for all length of word
			for i in range(len(self.word)):
				self.backspace()
		self.word = ""																#And then clear word

	def checkinput(self, value):												#Function to check input value with another string value
		return self.word == value

	def drawinput(self, boolean):												#Function to set input drawable
		self.isdrawable = boolean

	def endwin(self):															#Default function to stop window drawing and exit
		curses.endwin()


gamewindow = Window()
gamewindow.init()
gamewindow.write("Hello world: ")

x = True
def sonkeypress(key):
	global x
	if key == "q":
		x = False
gamewindow.onkeypress = sonkeypress

err = ""
while x:
	try:
		key = gamewindow.readkey()
		#word = gamewindow.readinput()
	except Exception as e:
		pass

gamewindow.endwin()
print(stdout)
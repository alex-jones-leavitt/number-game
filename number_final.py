#Alex Jones
#04-25-2018
#Final Project: Create login service for number game
import logging
import optparse
from random import randint

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

fh = logging.FileHandler("warnings.log")
fh.setLevel(logging.WARNING)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.addHandler(fh)
#Comment out following line to stop logs to console
logger.addHandler(sh)

file_name = 'user_list.txt'

def credential(user, pasd, lines):
	"""This function checks given credentials against the username and password text file"""
	#Gives 3 login attempts after first failed login
	attempts  = 3
	#Checks for correct password
	if lines[lines.index(user)+1] == pasd:
		logger.debug("Starting game")
		start_game(user)
	else:
		new_pasd = input("Incorrect password, try again. %d attempts remaining.\n(Remeber, if there are spaces in your password, you need to surround it all with quotation marks)" %attempts)
		a = True
		#This while loop allows 3 more login attempts after a first failed login
		while a:
			#This if statement checks the newly entered password, and decreases attempts by 1 if it is incorrect
			if lines[lines.index(user)+1] != new_pasd:
				attempts -= 1
			try:
				#Correct password starts game
				if attempts>0:
					if lines[lines.index(user)+1] == new_pasd:
						logger.debug("DEBUG - Starting game")
						start_game(user)
						a = False
					else:
						new_pasd = input("Incorrect password, try again. %d attempts remaining.\n" %attempts)
						logger.debug("DEBUG - Resending to credential()")
				elif attempts == 0:
					logger.debug("DEBUG - Out of attempts")
					print("Incorrect password.")
					print("BANNED")
					a = False
			#This except is for errors that are given if an entered password does not exist anywhere in the list
			except ValueError:
				logger.warning("WARNING - Invalid input")
				new_pasd = input("Incorrect password, try again. %d attempts remaining.\n" %attempts)
				attempts -= 1
			#credential(user, new_pasd, lines)
		

def create_user(user):
	"""This function adds a user and password to the user list"""
	#This while loop checks for matching passwords before it creates it, and lets the user reenter them if they don't match
	while True:
		pasd = input("What would you like your password to be? *including spaces will end your password at the space, unless surrounded by quotaiton marks.\n")
		pasd_check = input("Please enter your password again.\n")
		#This checks for matching password entries
		if pasd == pasd_check:
			logger.debug("DEBUG - Successful login")
			with open(file_name, 'a+') as f:
				f.write(user+'\n')
				f.write(pasd+'\n')
				print("User created, starting game.\n")
				start_game(user)
				break
		else:
			logger.debug("DEBUG - Incorrect password")
			print("Your passwords did not match.  Try again.")
	

def login(user,pasd):
	"""This function checks the given username against the username list, and sends it to credential or try_again"""
	with open(file_name) as f:
		lines = f.readlines()
		strip_lines = [s.rstrip() for s in lines]
		#Takes all even index items in lines for usernames
		usernames = strip_lines[0:][::2]
		#Takes all odd index items in lines for passwords
		passwords = strip_lines[1:][::2]
		logger.debug("usernames: " +str(usernames))
		logger.debug("passwords: " +str(passwords))
		if user in usernames:
			logger.debug("DEBUG - Valid username")
			credential(user, pasd, strip_lines)
		else:
			logger.debug("DEBUG - Invalid username")
			print("Invalid username.")
			try_again(user, usernames)
				
def try_again(user, usernames):
	"""This function gives the option to try again or create a user on failed first login"""
	ans = input("Would you like to try again (A), create a user (C) or quit (Ctrl+C)?\n(Remember, if there are spaces in your username, you need to surround it all with quotation marks)\n")
	if ans.upper() == 'A':
		logger.debug("DEBUG - Trying login again")
		new_user = input("What is your username?\n(If there are spaces, be sure to use quotation marks)\n")
		if new_user in usernames:
			new_pasd = input("What is your password?\n")
			login(new_user, new_pasd)
		else:
			logger.debug("DEBUG - Invalid username")
			print("That username does not exist.")
			while True:
				option = input("Would you like to create an account? Y/N\n")
				if option.upper() == 'Y':
					logger.debug("DEBUG - Creating user")
					create_user(new_user)
					break
				elif option.upper() == 'N':
					logger.debug("DEBUG - Exiting game")
					print("You're confusing, BYE!\n")
					break
				else:
					print("That is not valid input. Please enter Y for yes, or N for no.")
	elif ans.upper() == 'C':
		logger.debug("DEBUG - Creating user")
		create_user(user)
	else:
		logger.warning("WARNING - Invalid input")
		print("Invalid input, hold Ctrl+C to quit, enter A to try again or enter C to create a user.")
		try_again(user, usernames)

def start_game(user):
	"""This function runs the game"""
	print("Hello %s, welcome to the game." %user)
	difficulty = input("We can make this game as hard as you want.  Enter a number greater than or equal to 10.\nRemember, you still only get 10 guesses, so don't be too adventurous.\nIf you choose a number under 10, you will be defaulted to 10\n")
	a = b = True
	while a:
		try:
			#difficulty = int(input("We can make this game as hard as you want.  Enter a number greater than or equal to 10.\nRemember, you still only get 10 guesses, so don't be too adventurous.\nIf you choose a number under 10, you will be defaulted to 10\n"))
			difficulty = int(difficulty)
			if difficulty < 10:
				logger.warning("WARNING - " +difficulty +" is not a valid number, setting to 10")
				print("That's too small, defaulted to 10.")
				difficulty = 10
			#Generates a random integer in the range specified
			number = randint(1,difficulty)
			logger.debug("Random number is " +str(number))
			
			score = 10
			#This is the bulk of the game, where it takes their input and compares it to the random value, and adjusts their score accordingly
			while b:
				try:
					if score == 0:
						print("YOU LOSE!!!!!!!!! HA HA")
						game_end(user)
						a = False
					guess = int(input("Please guess a number between 1 and %d. \n"%int(difficulty)))
					logger.debug("DEBUG - Valid input: " +str(guess))
					#Tests if their guess is less than the number
					if guess<number:
						logger.debug("DEBUG - Comparison guess < number")
						print("The secret number is LARGER than " +str(guess))
						score -= 1
					#Tests if their guess is greater than the number
					elif guess>number:
						logger.debug("DEBUG - Comparison guess < number")
						print("The secret number is SMALLER than " +str(guess))
						score -=1
					#This runs if their guess is equal to the number
					else:
						logger.debug("DEBUG - Comparison guess = number")
						score = score*int(difficulty)
						print("That is correct! Your score is " +str(score))
						logger.debug("DEBUG - Going to game_end()")
						game_end(user)
						a = b = False
				except ValueError as guess:
					logger.warning("WARNING - Invalid guess: "+str(guess))
					print("That's not a valid number. Try again.")
		#This catches invalid input (anything that is not an integer)
		except ValueError as invalid:
			logger.warning("WARNING - Invalid input: " +str(invalid))
			difficulty = input("That's not a valid number. Try again.\n")
			
def game_end(user):
	"""This function allows the user to play again or quit the game"""
	b = True
	while b:
		answer = input("Do you want to play again??? Y/N\n")
		#This if statement tests to make sure they answered with any capitalization of yes/no
		if answer.upper() == "Y":
			print("SAHWEET!!!")
			logger.debug("DEBUG - Going to play()")
			start_game(user)
			b = False
		elif answer.upper() == "N":
			print("FINE! I didn't want to play with you anyway!")
			logger.debug("DEBUG - Exiting game")
			b = False
		#If they input anything other than yes or no, it will prompt them again, until they give valid input
		else:
			logger.warning("WARNING - Invalid input (answer): " +str(answer))
			print("Enter Y for yes or N for no. Try again.")

def main():
	"""This function sets the options and runs the login function"""
	parser = optparse.OptionParser(add_help_option = False)
	parser.add_option('-h','--help', action='help', help='Enter a username and password, and choose a number for the guessing game. Higher numbers are more difficult but receive higher scores')
	parser.add_option('-u', dest='user', type='string', help='Username for number game')
	parser.add_option('-p', dest='pasd', type='string', help='Password for number game')
	(options, args) = parser.parse_args()
	user = options.user
	pasd = options.pasd
	login(user,pasd)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print("\nQuitter.")
		

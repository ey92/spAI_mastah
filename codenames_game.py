### Created 04/17/2017 by Lauren Hsu and Elizabeth Yam
from __future__ import print_function
import numpy as np 
import random
# import codenames_ai as ai


# DICTIONARY_FILE = "test.txt"
DICTIONARY_FILE = "words.txt"
BLUE_TEAM = 0
RED_TEAM = 1
CIVILIAN = 2
ASSASIAN = 3

#Game states
GAME_START = 0
GAME_RESET = 1
GAME_IN_PROGRESS = 2
GAME_END = 3

game_state = GAME_START
is_spy_master = False
human_team = BLUE_TEAM
current_team = BLUE_TEAM
red_words = 8
blue_words = 8
total_words = 25
word_grid = {}
word_list = []
guessed = [0]*total_words
assasian_word = ""

#TODO Distinguish agent vs. spy master input/output and actions and logic processsing and everything
#TODO Finish game loop
#TODO COLORS


def createGame():
	global current_team
	global blue_words
	global red_words
	##Decide if red or blue goes first
	coin_flip = random.randint(0,1)
	
	#Hard-coded incase of reset
	if coin_flip==BLUE_TEAM:
		print("The blue team will go first")
		current_team = BLUE_TEAM
		blue_words = 9
		red_words = 8
	else:
		print("The red team will go first")
		current_team = RED_TEAM
		blue_words = 8
		red_words = 9	
	
	#Create word grid + assign words to teams
	# return createWordGrid()
	createWordGrid()


def printWordGrid():
	# global word_list

	for x in range(0,5):
		for y in range(0,5):
			position = y+(x*5)
			#If word HAS NOT been guessed yet
			#TODO Colors
			# print(str(position))
			if guessed[position]==0:				
				print(word_list[position]+str(guessed[position])+"\t\t", end="")
			else:
				print(word_list[position]+str(guessed[position])+"\t\t", end="")
		print("\n")

	print("Blue words left: "+str(blue_words))
	print("Red words left: "+str(red_words))


# Populate the word grid
def getWords():
	# grid_words = []
	global word_list

	with open(DICTIONARY_FILE,"r") as file:
		words = file.read()
		sample_list = words.split("\n")
		while len(word_list)<total_words:
			rand_num = random.randint(0,len(sample_list)-1)
			chosen_word = sample_list[rand_num]
			#Format word for printing
			chosen_word = chosen_word.capitalize()
			chosen_word = chosen_word.replace("_", " ")
			#Don't add if already there
			if word_list.count(chosen_word)==0:
				word_list.append(chosen_word)

	# return grid_words

	# print(word_list)


	# word_list = grid_words


#Create word grid with assigning words to teams
def createWordGrid():
	# global word_list
	global word_grid
	global word_list
	global assasian_word
	##Get random set of words in a dictionary
	#Assigned here incase of reset
	word_grid = {} #GLOBAL
	word_list = [] #GLOBAL, resets for every game

	#Populates word_list
	# word_list = getWords()	
	getWords()

	##Assign key as word w/ value as BLUE_TEAM, RED_TEAM, CIVILIAN, or ASSASIAN
	assasian_num = 1
	civilian_num = total_words-blue_words-red_words-assasian_num

	#Insert blue into assigning order
	assign_order = [BLUE_TEAM]*blue_words

	#Insert red in assigning order
	for i in range(0,red_words):
		assign_num = random.randint(0,len(assign_order)-1)
		assign_order.insert(assign_num,RED_TEAM)

	#Insert civilian in assigning order
	for i in range(0,civilian_num):
		assign_num = random.randint(0,len(assign_order)-1)
		assign_order.insert(assign_num,CIVILIAN)

	#Insert assasian in assigning order
	assign_num = random.randint(0,len(assign_order)-1)
	assign_order.insert(assign_num,ASSASIAN)

	# print("Burp")
	# print(assign_order)
	# print(word_list)

	#Assign words a label
	for i in range(0,len(word_list)):
		word = word_list[i]
		assign_num = assign_order[i]
		# print("Word: "+word+", ID:  "+str(assign_num))
		word_grid.update({word:assign_num})	
		if assign_num==ASSASIAN: assasian_word = word

	# return word_list, word_grid

	# print("Derp")
	# print("Word: "+word_list+", ID:  "+word_grid.get())


#Processes a guess made by an agent (the player) 
#[NOTE: assumes from previous procedures that response exists in word_list]
def processGuess(response):
	global word_grid
	# global word_list
	global blue_words
	global red_words
	global guessed
	global game_state
	#Format response for processing
	# query = response.lower()
	# query.replace(" ", "_") # In case two-word choice is on board

	#Check if word is on board
		#Find index of word on board
	# If not redo prompt?

	#Get identity of the word
	word_identity = word_grid.get(response)
	#Mark as guessed (make negative) for AI processing
	word_grid.update({response:word_identity*-1})
	#Mark a word as guessed
	word_idx = word_list.index(response)
	guessed[word_idx] = 1

	# print("Word is: "+str(word_identity))
	if word_identity==BLUE_TEAM:
		blue_words-=1
		# print("You found a "+getTeamString(BLUE_TEAM)+" card!")
		print("You found a "+getTeamString(BLUE_TEAM)+" card! That's "+str(blue_words)+" cards left for the "+getTeamString(BLUE_TEAM)+"!")

		if blue_words==0: 
			print("The "+getTeamString(BLUE_TEAM)+" has no cards left, so they win! Congrats!")
			endGame()
	elif word_identity==RED_TEAM:
		red_words-=1
		print("You found a "+getTeamString(RED_TEAM)+" card! That's "+str(red_words)+" cards left for the "+getTeamString(RED_TEAM)+"!")
		if red_words==0: 
			print("The "+getTeamString(RED_TEAM)+" has no cards left, so they win! Congrats!")
			endGame()
	elif word_identity==CIVILIAN:
		print("You found a civilian card!")
	elif word_identity==ASSASIAN:
		winner_num = (current_team + 1) % 2
		winner = getTeamString(winner_num)
		print("Oh no!!! You chose the assasian word! That means the "+winner+" wins!")
		# game_state = GAME_RESET # TODO Figure out whether this should be GAME_END instead, probably not though
		endGame()


# Gets a prompt/clue from the spymaster, human or AI
def getPrompt():
	# Need to check current team
	#If human is the spy master and if it's their tur
	clue = "dummy clue"
	clue_num = 1

	if is_spy_master and current_team==human_team:
		pass
	#If the ai is the spy master
	else:
		pass

	return clue, clue_num

#Processes a hint given by the spy master (the player)
def processPrompt(response,number):
	#Format response for processing
	query = response.lower()
	# clue = "dummy clue"
	# clue_num = 1

	#Get sim_matrix

	#Get index of query in sim_matrix
	#Find corres. vector in sim_matrix
	#Argmax sorting
	#Iterate through results
		#If result is in the word_list, add to list of guesses until is length [number]
	#

	#Edge case = only 1 word left on board

	#Need to check similarities with assasin and opponent's words

	# return clue, clue_num

#Returns a team number as a team string because lazy
def getTeamString(team_num):
	if team_num == BLUE_TEAM:
		return "blue team"
	else:
		return "red team"	

# Call to end the game
def endGame():
	global game_state

	game_state=GAME_RESET # TODO Figure out whether this should be GAME_END instead, probably not though

	print("Final results: ")
	print("\t"+getTeamString(BLUE_TEAM)+": "+str(blue_words))
	print("\t"+getTeamString(RED_TEAM)+": "+str(red_words))
	# print("\t Civilian words: "+str(red_words))
	print("\t The assasian word was "+assasian_word)

	#Check for win/lose conditions

def gameLoop():
# def gameLoop(word_list,word_grid):
	# global game_state
	# print("WAH")
	# print(game_state)
	# game_state=GAME_IN_PROGRESS # TODO Figure out why this keeps getting read as a local variable
	while game_state==GAME_IN_PROGRESS:
		printWordGrid()
		# printWordGrid(word_list)

		# for i in range(0,len(word_list)):
		# 	word_test = word_list[i]
		# 	id_num = word_grid.get(word_test)
		# 	print("Word: "+word_test+", ID:  "+str(id_num))

		print("[Current turn: "+getTeamString(current_team)+"]\n")
		# clue, clue_num = getPrompt()
		# processPrompt(clue, clue_num)

		# guess = getGuess()
		# processGuess(guess)

		print("Your clue is: "clue+" "+str(clue_num))

		if is_spy_master==False:
			response = raw_input("What word would you like to guess?\n")
			response = response.strip()
			response = response.capitalize()
			# Prevent users from making typos or guessing words not on the board
			if word_list.count(response)==0:
				print("\""+response+"\" isn't on the board! Try again.")
			else: 
				# response = response.lower()
				processGuess(response)
		else:
			response = raw_input("What prompt would you like to give?\n")
			#Format prompt for rule-checking
			response = response.strip()
			temp = response
			# temp.replace("_", " ")
			# temp.replace("-", " ")
			# temp.replace(" ", "")
			# ^isalpha() takes care of most of these
			temp = temp.capitalize()
			#Rule-check
			if word_list.count(temp)==1 and guessed[word_list.index(temp)]==0:
				print("Hey, \""+response+"\"  is on the board already! You can't use that as a clue! Try a different one.")
			elif temp.count(" ")>0:
				print("You can only provide one word as a clue! Try a different one.")
			elif not temp.isalpha():
				print("Hey now, you can't put non-alphabet characters in your clue! Try a different one.")
			else: 
				number = raw_input("How many words are there?\n")
				if not number.isdigit():
					print("Hey, this isn't a number! Now you have to start over because user edge-cases are annoying to handle =(")
				else: 
					# response = response.lower()
					processPrompt(response,number)			
			# if word_list.count(temp)==1 && guessed(word_list.index(temp))==0:
			# 	print("Hey, that word is on the board! You can't use that as a clue! Try a different one.")
			# else: processPrompt(response,number)



def main():
	global game_state
	# print("Welcome to Codenames!\n")
	response = raw_input("Would you like to be spy master? [Yes/No]\n")
	response = response.capitalize()
	# TODO ask if there are human players for both teams
	# TODO ask which team the player wants to be on if only one team has human players

	if response == "Yes":
		is_spy_master = True
		print("You will be the spy master for your team\n")
	elif response == "No":
		is_spy_master = False
		print("You will be a regular agent for your team\n")
	else:
		is_spy_master = False
		print("Your response could not be read, you have been defaulted to not being spy master\n")

	team_req = raw_input("Which team do you want to be on? [Blue/Red]\n")
	team_req = team_req.capitalize()
	
	# TODO ask if there are human players for both teams
	# TODO ask which team the player wants to be on if only one team has human players
	if team_req == "Blue":
		human_team = BLUE_TEAM
		print("You will be on the blue team\n")
	elif team_req == "No":
		human_team = RED_TEAM
		print("You will be on the blue team\n")
	else:
		human_team = BLUE_TEAM
		print("Your response could not be read, but I like the color blue, so you will be on the blue team\n")

	# word_list, word_grid = createGame()
	createGame()

	game_state = GAME_IN_PROGRESS #TODO Should this be defined here?

	# printWordGrid()
	# game_state=GAME_IN_PROGRESS

	# print(game_state)
	# print("Go")
	# print(word_list)
	# print(word_grid)

	# gameLoop(word_list,word_grid)
	gameLoop()

	print("Bye =3 xx3")




if __name__ == "__main__":
	global game_state
	print("Welcome to Codenames!\n")
	while not game_state==GAME_END:
		main()

		response = raw_input("Would you like to play again?[Yes/No]")
		response = response.strip()
		response = response.capitalize()
		if response == "Yes":
			game_state=GAME_RESET
			print("Another game will be started then!")
		elif response == "No":
			game_state=GAME_END
			print("Thanks for playing! =D\n")

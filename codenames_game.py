### Created 04/17/2017 by Lauren Hsu and Elizabeth Yam
from __future__ import print_function
import numpy as np 
import random
import codenames_ai as ai
from sys import version_info as vi
import printcolor as col

py3 = False

DICTIONARY_FILE = "words.txt"
BLUE_TEAM = 0
RED_TEAM = 1
CIVILIAN = 2
ASSASIAN = 3

#For color-printing
MASTER_VIEW = 0
SPY_VIEW = 1
GUESSED = 4
NOT_GUESSED = 5
BLUE_CARD_COLOR = col.CBLUEBG2 #Blue
RED_CARD_COLOR = col.CREDBG #Red
CIV_CARD_COLOR = col.CGREENBG #Green
BOOM_CARD_COLOR = col.CBEIGEBG #Yellow
# GUESSED_COLOR = col.CBLACK #Black
GUESSED_COLOR = col.CVIOLETBG
NOT_GUESSED_COLOR = col.CBLACKBG
TEXT_COLOR = col.CGREY

#Game states
GAME_START = 0
GAME_RESET = 1
GAME_IN_PROGRESS = 2
GAME_END = 3

game_state = GAME_START
is_spy_master = False
human_team = BLUE_TEAM

blue_master_human = False
blue_spy_human = False
red_master_human = False
red_spy_human = False

#Placeholders for initializing 
blue_ai_master = 0
blue_ai_agent = 0
red_ai_master = 0
red_ai_agent = 0

current_team = BLUE_TEAM
red_words = 8
blue_words = 8
total_words = 25
word_grid = {}
word_list = []
guessed = [0]*total_words
assasian_word = ""


def createGame():
	global current_team
	global blue_words
	global red_words

	global blue_ai_master
	global blue_ai_agent
	global red_ai_master
	global red_ai_agent
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

	print("\n")

	#Create AIs if necessary, complete with loading messages
	if not blue_master_human: 
		print("Recruiting a spy master for the blue team...")
		blue_ai_master = ai.spyMaster(BLUE_TEAM)
	if not blue_spy_human: 
		print("Recruiting spy agents for the blue team...")
		blue_ai_agent = ai.spyAgent(BLUE_TEAM)
	if not red_master_human: 
		print("Recruiting a spy master for the red team...")
		red_ai_master = ai.spyMaster(RED_TEAM)
	if not red_spy_human: 
		print("Recruiting spy agents for the red team...")
		red_ai_agent = ai.spyAgent(RED_TEAM)
	
	print("\n")
	#Create word grid + assign words to teams
	createWordGrid()

def getIdColor(color_id):
	if abs(color_id)==BLUE_TEAM:
		return BLUE_CARD_COLOR
	elif abs(color_id)==RED_TEAM:
		return RED_CARD_COLOR
	elif abs(color_id)==CIVILIAN:
		return CIV_CARD_COLOR
	elif abs(color_id)==ASSASIAN:
		return BOOM_CARD_COLOR
	elif abs(color_id)==GUESSED:
		return GUESSED_COLOR
	elif abs(color_id)==NOT_GUESSED:
		return NOT_GUESSED_COLOR #TODO Choose a better color

def printWordGrid(game_view):
	# global word_list

	for x in range(0,5):
		# colorprint(text,color,bg=None,bold=False)
		print_text = []
		print_color = []
		for y in range(0,5):
			position = y+(x*5)
			#If word HAS NOT been guessed yet
			#TODO Colors
			# print(str(position))
			print_word = word_list[position]
			print_text.append(print_word)
			if game_view==SPY_VIEW:
				if guessed[position]==0:
					# print(print_word+str(guessed[position])+"\t\t", end="")
					print_color.append(getIdColor(NOT_GUESSED))
				else:
					word_id = word_grid.get(print_word)
					# col.colorprint(print_word+"\t\t",TEXT_COLOR,getIdColor(word_id))
					print_color.append(getIdColor(word_id))
			elif game_view==MASTER_VIEW:
				if guessed[position]==0:
					word_id = word_grid.get(print_word)
					# col.colorprint(print_word+"\t\t",TEXT_COLOR,getIdColor(word_id))
					print_color.append(getIdColor(word_id))
				else:
					word_id = word_grid.get(print_word)
					# col.colorprint(print_word+"\t\t",GUESSED_COLOR,getIdColor(word_id))
					print_color.append(getIdColor(GUESSED))

			# if guessed[position]==0:
			# 	# col.colorprint()
			# 	print(word_list[position]+str(guessed[position])+"\t\t", end="")
			# else:
			# 	print(word_list[position]+str(guessed[position])+"\t\t", end="")

		# print("\n")
		col.colorprint(print_text,print_color)
	col.endColor()

	print("KEY: Blue team = blue, Red team = red, Civilian = green, Assasian = yellow/beige/teal")
	print("Blue words left: "+str(blue_words))
	print("Red words left: "+str(red_words))
	print("\n")


# Populate the word grid
def getWords():
	global word_list
	#Assigned here incase of reset
	if py3:
		word_list.clear()
	else:
		del word_list[:]

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


#Create word grid with assigning words to teams
def createWordGrid():
	global word_grid
	global word_list
	global assasian_word

	#Assigned here incase of reset
	word_grid.clear()

	##Get random set of words in a dictionary
	#Populates word_list
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

	#Assign words a label
	for i in range(0,len(word_list)):
		word = word_list[i]
		assign_num = assign_order[i]
		# print("Word: "+word+", ID:  "+str(assign_num))
		word_grid.update({word:assign_num})	
		if assign_num==ASSASIAN: assasian_word = word


#Processes a guess made by an agent (the player) 
#[NOTE: assumes from previous procedures that response exists in word_list]
def processGuess(response,team_id):
	global word_grid
	# global word_list
	global blue_words
	global red_words
	global guessed
	global game_state

	endTurn = False
	#Format response for processing
	# query = response.lower()
	# query.replace(" ", "_") # In case two-word choice is on board

	#Check if word is on board
		#Find index of word on board
	# If not redo prompt?

	#Get identity of the word
	# print(response)
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

		#End turn if red team guessed a blue word
		if team_id==RED_TEAM:
			print("The red team guessed a blue word, so its turn has ended.")
			endTurn=True

		#End game if all of blue's words are gone
		if blue_words==0: 
			print("The "+getTeamString(BLUE_TEAM)+" has no cards left, so they win! Congrats!")
			endGame()
	elif word_identity==RED_TEAM:
		red_words-=1
		print("You found a "+getTeamString(RED_TEAM)+" card! That's "+str(red_words)+" cards left for the "+getTeamString(RED_TEAM)+"!")

		#End turn if blue team guessed a red word
		if team_id==BLUE_TEAM:
			print("The blue team guessed a red word, so its turn has ended.")
			endTurn=True
		
		#End game if all of red's words are gone
		if red_words==0: 
			print("The "+getTeamString(RED_TEAM)+" has no cards left, so they win! Congrats!")
			endGame()
	
	elif word_identity==CIVILIAN:
		print("You found a civilian card!")
		print("This isn't your team's card though, so your turn has now ended")
		endTurn=True
	
	elif word_identity==ASSASIAN:
		endTurn=True
		winner_num = (current_team + 1) % 2
		winner = getTeamString(winner_num)
		print("Oh no!!! You chose the assasian word! That means the "+winner+" wins!")
		# game_state = GAME_RESET # TODO Figure out whether this should be GAME_END instead, probably not though
		endGame()

	print("\n")

	return endTurn

def getHumanPrompt():
	clue = ""
	clue_num = 0
	
	clue_done = False
	num_done = False

	printWordGrid(MASTER_VIEW)
	
	while not clue_done:
		if py3:
			clue = input("Spy Master, what prompt would you like to give?\n")
		else:
			clue = raw_input("Spy Master, what prompt would you like to give?\n")
		clue = clue.strip().lower()
		
		temp = clue
		# temp = temp.capitalize()
		dict_check = True
		# **Only care if not a real word if the agents aren't human**
		if current_team==BLUE_TEAM and not blue_spy_human: 
			temp = temp.lower()
			exists = blue_ai_agent.bankword_to_idx.get(temp)
			if exists==None: dict_check= False
		elif current_team==RED_TEAM and not red_spy_human:
			temp = temp.lower()
			exists = red_ai_agent.bankword_to_idx.get(temp)
			if exists==None: dict_check= False
					
		clue = clue.capitalize()

		if word_list.count(clue)==1 and guessed[word_list.index(clue)]==0:
			print("Hey, \""+clue+"\"  is on the board already! You can't use that as a clue! Try a different one.")
		elif clue.count(" ") > 0:
			print("You can only provide one word as a clue! Try a different one.")
		elif not clue.isalpha():
			print("Hey now, you can't put non-alphabet characters in your clue! Try a different one.")
		elif not dict_check:
			print("\""+clue+"\" doesn't exist in the agents' vocabulary! Can you try a different one instead?")
		else:
			clue_done = True

		print("\n")
			
	while not num_done:
		if py3:
			clue_num = input("Spy Master, how many guesses should your agents make?\n")
		else:
			clue_num = raw_input("Spy Master, how many guesses should your agents make?\n")
		clue_num = clue_num.strip()

		if not clue_num.isdigit():
			print("Hey, this isn't a number! Try again!")
		else:
			num_done = True
			clue_num = int(clue_num)

		print("\n")
			
	return clue, clue_num


# Gets a prompt/clue from the spymaster, human or AI
def getPrompt():
	# Need to check current team
	#If human is the spy master and if it's their tur
	global blue_ai_master
	global red_ai_master

	print("[Current turn: "+getTeamString(current_team)+", SPY MASTER]\n")
	
	clue = ""
	clue_num = 0
	
	if current_team == BLUE_TEAM:
		# print("[Current Team: Blue Team]")

		# blue spy master stuff
		# print("It is Blue Spy Master's Turn")

		if not blue_master_human:
			print("The blue spy master is thinking...\n")
			return blue_ai_master.createClue(word_list,word_grid)
		else:
			return getHumanPrompt()
	else:
		# print("[Current Team: Blue Team]")
		
		# red spy master stuff
		# print("It is Red Spy Master's Turn")
		if not red_master_human:
			print("The red spy master is thinking...\n")
			return red_ai_master.createClue(word_list,word_grid)
		else:
			return getHumanPrompt()

	return clue, clue_num

#Returns a guess made by the players (human or AI) based off the clue
def takeGuess(clue,clue_num):
	#Guesses must be processed after each on is made
	guess = "dummy guess"
	num_guesses = clue_num

	print("[Current turn: "+getTeamString(current_team)+", AGENTS]\n")

	while num_guesses>0:		
		if (current_team==BLUE_TEAM and blue_spy_human) or (current_team==RED_TEAM and red_spy_human):
			printWordGrid(SPY_VIEW)
			# print("[Current turn: "+getTeamString(current_team)+", AGENTS]\n")
			print("Your clue is: "+clue+" "+str(num_guesses))
			valid_response=False
			while not valid_response:				
				
				response = ""
				if py3:
					response = input("Agents, what word would you like to guess? [Number of guesses left: "+str(num_guesses)+"]\n")
				else:
					response = raw_input("Agents, what word would you like to guess? [Number of guesses left: "+str(num_guesses)+"]\n")

				response = response.strip()
				response = response.capitalize()
				# Prevent users from making typos or guessing words not on the board
				if word_list.count(response)==0:
					print("\""+response+"\" isn't on the board! Try again.")
				else: 
					guess = response
					valid_response=True
					num_guesses-=1
		elif current_team==BLUE_TEAM and not blue_spy_human:
			print("The clue is: "+clue+" "+str(num_guesses)+"\n")
			print("The blue agents are thinking...\n")
			query = clue.capitalize()
			guess = blue_ai_agent.makeGuesses(word_list, guessed,query,clue_num)
			num_guesses-=1
		elif current_team==RED_TEAM and not red_spy_human:
			print("The clue is: "+clue+" "+str(num_guesses)+"\n")
			print("The red agents are thinking...\n")
			query = clue.capitalize()
			guess = red_ai_agent.makeGuesses(word_list, guessed,query,clue_num)
			num_guesses-=1
		else:
			print("This shouldn't be a thing for guessing")

		guess = guess.capitalize()
		print("The agents guessed: "+guess)
		result = processGuess(guess,current_team)
		
		# If endTurn==True, then end the turn
		if result: 
			num_guesses=0
		
		#Teach AI only if playing with humans, don't have learn off of selves

		#Have agents account for their guess being related (or not) to the clue based on correctness
		if current_team==BLUE_TEAM and not blue_spy_human and blue_master_human:
			query = clue.lower()
			#If the guess was wrong, the two are probably not related
			if result:
				print("Blue thinks that was bad")
				blue_ai_agent.addIrrelevantEntry(query,guess)
				blue_ai_agent.addIrrelevantEntry(guess,query)
			#If the guess was correct, the two are probably related
			else:
				print("Blue thinks that was good")
				blue_ai_agent.addRelevantEntry(query,guess)
				blue_ai_agent.addRelevantEntry(guess,query)

		if current_team==RED_TEAM and not red_spy_human and red_master_human:
			query = clue.lower()
			#If the guess was wrong, the two are probably not related
			if result:
				print("Red thinks that was bad")
				red_ai_agent.addIrrelevantEntry(query,guess)
				red_ai_agent.addIrrelevantEntry(guess,query)
			#If the guess was correct, the two are probably related
			else:
				print("Red thinks that was good")
				red_ai_agent.addRelevantEntry(query,guess)
				red_ai_agent.addRelevantEntry(guess,query)

		#TODO Teach AI master based off what it was trying to get people to guess and the clue it gave
		if current_team==BLUE_TEAM and not blue_master_human and blue_spy_human:
			query = clue.lower() 
			#Also get words that AI intended to be guessed, replaces guess in statement
			#If the guess was wrong, the two are probably thought to be related
			
			blue_ai_master.addRelevantEntry(query,guess)
			blue_ai_master.addRelevantEntry(guess,query)

			#TODO Add clue and top num_clue words from processing to irrelevant

		if current_team==RED_TEAM and not red_master_human and red_spy_human:
			query = clue.lower()
			#Also get words that AI intended to be guessed, replaces guess in statement
			#If the guess was wrong, the two are probably thought to be related
			
			red_ai_master.addRelevantEntry(query,guess)
			red_ai_master.addRelevantEntry(guess,query)

			#TODO Add clue and top num_clue words from processing to irrelevant


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
	print("\t"+getTeamString(BLUE_TEAM)+": "+str(blue_words)+" cards remaining")
	print("\t"+getTeamString(RED_TEAM)+": "+str(red_words)+" cards remaining")
	# print("\t Civilian words: "+str(red_words))
	print("\t The assasian word was "+assasian_word)

	print("\n")

	#Check for win/lose conditions

	#TODO
	#Have the AI save their Rocchios in case they were modified during the game

	# LEAVE THESE COMMENTS HERE
	if not blue_master_human:
		print("The blue spymaster is being dismissed...")
		blue_ai_master.saveRocchios()

	if not red_master_human:
		print("The red spymaster is being dismissed...")
		red_ai_master.saveRocchios()

	if not blue_spy_human:
		print("The blue agents are being dismissed...")
		blue_ai_agent.saveRocchios()

	if not red_spy_human:
		print("The red agents are being dismissed...")
		red_ai_agent.saveRocchios()
	

def gameLoop():
	global current_team
	# game_state=GAME_IN_PROGRESS # TODO Figure out why this keeps getting read as a local variable
	while game_state==GAME_IN_PROGRESS:
		# printWordGrid()
		# printWordGrid(word_list)

		# for i in range(0,len(word_list)):
		# 	word_test = word_list[i]
		# 	id_num = word_grid.get(word_test)
		# 	print("Word: "+word_test+", ID:  "+str(id_num))

		# print("[Current turn: "+getTeamString(current_team)+", SPY MASTER]\n")

		#Get clue from spy master
		clue, clue_num = getPrompt()
		
		#Give clue to spy agents + process it
		takeGuess(clue,clue_num)
		
		#Switch to next team
		current_team = (current_team+1)%2

		print("\n")



def main():
	global game_state
	global blue_master_human
	global blue_spy_human
	global red_master_human
	global red_spy_human


	response = ""
		
	#Check human spy master for blue team
	valid_response = False
	while not valid_response:
		if py3:
			response = input("Will there be a human spy master for the blue team? [(Y)es/(N)o]\n")
		else:
			response = raw_input("Will there be a human spy master for the blue team? [(Y)es/(N)o]\n")
		response = response.strip()
		response = response.capitalize()
		if response == "Yes" or response == "Y":
			blue_master_human = True
			print("Humans will be the spy master for the blue team\n")
			valid_response=True
		elif response == "No" or response == "N":
			blue_master_human = False
			print("An AI will be the spy master for the blue team\n")
			valid_response=True
		else:
			print("I'm sorry, I didn't understand that\n")

	#Check human spy agent(s) for blue team
	valid_response = False
	while not valid_response:
		if py3:
			response = input("Will there be human agents for the blue team? [(Y)es/(N)o]\n")
		else:
			response = raw_input("Will there be human agents for the blue team? [(Y)es/(N)o]\n")
		response = response.strip()
		response = response.capitalize()
		if response == "Yes" or response == "Y":
			blue_spy_human = True
			print("Human agents will be on the blue team\n")
			valid_response=True
		elif response == "No" or response == "N":
			blue_spy_human = False
			print("AI agents be on the blue team\n")
			valid_response=True
		else:
			print("I'm sorry, I didn't understand that\n")

	#Check human spy master for red team
	valid_response = False
	while not valid_response:
		if py3:
			response = input("Will there be a human spy master for the red team? [(Y)es/(N)o]\n")
		else:
			response = raw_input("Will there be a human spy master for the red team? [(Y)es/(N)o]\n")

		response = response.capitalize()
		if response == "Yes" or response == "Y":
			red_master_human = True
			print("Humans will be the spy master for the red team\n")
			valid_response=True
		elif response == "No" or response == "N":
			red_master_human = False
			print("An AI will be the spy master for the red team\n")
			valid_response=True
		else:
			print("I'm sorry, I didn't understand that\n")

	#Check human spy agent(s) for red team
	valid_response = False
	while not valid_response:
		if py3:
			team_req = input("Will there be human agents for the red team? [(Y)es/(N)o]\n")
		else:
			team_req = raw_input("Will there be human agents for the red team? [(Y)es/(N)o]\n")
		team_req = team_req.capitalize()
		if team_req == "Yes" or team_req == "Y":
			red_spy_human = True
			print("Human agents will be on the red team\n")
			valid_response=True
		elif team_req == "No" or team_req == "N":
			red_spy_human = False
			print("AI agents be on the red team\n")
			valid_response=True
		else:
			print("I'm sorry, I didn't understand that\n")

	#Create game elements
	createGame()
	game_state = GAME_IN_PROGRESS #TODO Should this be defined here?

	print("Here is the game board: \n")
	printWordGrid(SPY_VIEW)
	#Start the loop
	gameLoop()
	# print("Bye =3 xx3")




if __name__ == "__main__":
	global game_state
	global py3

	#Check if environment is Python3
	py3 = vi[0]>2

	print("Welcome to Codenames!\n")
	while not game_state==GAME_END:
		#Enter main loop
		main()

		#Perform "outro"
		valid_response = False
		while not valid_response:
			respone = ""
			if py3:
				response = input("Would you like to play again?[(Y)es/(N)o]\n")
			else: 
				response = raw_input("Would you like to play again?[(Y)es/(N)o]\n")
			response = response.strip()
			response = response.capitalize()
			if response == "Yes" or response == "Y":
				game_state=GAME_RESET
				valid_response=True
				print("Another game will be started then!\n")
			elif response == "No" or response == "N":
				game_state=GAME_END
				valid_response=True
				print("Thanks for playing! =D\n")
			else: print("Sorry, I didn't understand that. Try again?\n")

		print("\n")


# 
### Created 04/17/2017 by Lauren Hsu and Elizabeth Yam
from __future__ import print_function
import numpy as np 
import random
import codenames_ai as ai
from sys import version_info as vi

py3 = False

DICTIONARY_FILE = "words.txt"
BLUE_TEAM = 0
RED_TEAM = 1
CIVILIAN = 2
ASSASIAN = 3

#For color-printing
MASTER_VIEW = 0
SPY_VIEW = 1
BLUE_CARD_COLOR = col.CBLUEBG #Blue
RED_CARD_COLOR = col.CREDBG #Red
CIV_CARD_COLOR = col.CGREENBG #Green
BOOM_CARD_COLOR = col.CYELLOWBG #Yellow
GUESSED_COLOR = col.CBLACK #Black
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

#TODO Distinguish agent vs. spy master input/output and actions and logic processsing and everything
#TODO Finish game loop
#TODO COLORS


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

	#Create AIs if necessary, complete with loading messages
	if not blue_master_human: 
		print("Recruiting a spy master for blue team...")
		blue_ai_master = ai.spyMaster(BLUE_TEAM)
	if not blue_spy_human: 
		print("Recruiting spy agents for blue team...")
		blue_ai_agent = ai.spyAgent(BLUE_TEAM)
	if not red_master_human: 
		print("Recruiting a spy master for red team...")
		red_ai_master = ai.spyMaster(RED_TEAM)
	if not red_spy_human: 
		print("Recruiting spy agents for red team...")
		red_ai_agent = ai.spyAgent(RED_TEAM)
	
	#Create word grid + assign words to teams
	createWordGrid()

def getIdColor(color_id):
	if color_id==BLUE_TEAM:
		return BLUE_CARD_COLOR
	elif color_id==RED_TEAM:
		return RED_CARD_COLOR
	elif color_id==CIVILIAN:
		return CIV_CARD_COLOR
	elif color_id==ASSASIAN:
		return BOOM_CARD_COLOR
	# elif color_id==-1:
	# 	return GUESSED_COLOR #TODO Choose a better color

def printWordGrid(game_view):
	# global word_list

	for x in range(0,5):
		for y in range(0,5):
			position = y+(x*5)
			#If word HAS NOT been guessed yet
			#TODO Colors
			# print(str(position))
			print_word = word_list[position]
			if game_view==SPY_VIEW:
				if guessed[position]==0:
					print(print_word+str(guessed[position])+"\t\t", end="")
				else:
					word_id = word_grid.get(print_word)
					col.colorprint(print_word+"\t\t",TEXT_COLOR,getIdColor(word_id))
			elif game_view==MASTER_VIEW:
				if guessed[position]==0:
					word_id = word_grid.get(print_word)
					col.colorprint(print_word+"\t\t",TEXT_COLOR,getIdColor(word_id))
				else:
					word_id = word_grid.get(print_word)
					col.colorprint(print_word+"\t\t",GUESSED_COLOR,getIdColor(word_id))

			col.endColor()
			# if guessed[position]==0:
			# 	# col.colorprint()
			# 	print(word_list[position]+str(guessed[position])+"\t\t", end="")
			# else:
			# 	print(word_list[position]+str(guessed[position])+"\t\t", end="")

		print("\n")

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
			clue = input("What prompt would you like to give?\n")
		else:
			clue = raw_input("What prompt would you like to give?\n")
		clue = clue.strip().lower()
		
		temp = clue
		# temp = temp.capitalize()
		dict_check = True
		if current_team==BLUE_TEAM and not blue_spy_human: 
			temp = temp.lower()
			exists = blue_ai_agent.bankword_to_idx.get(temp)
			if exists==None: dict_check= False
		elif current_team==RED_TEAM and not red_spy_human:
			temp = temp.lower()
			exists = red_ai_agent.bankword_to_idx.get(temp)
			if exists==None: dict_check= False
					
		clue.capitalize()

		if word_list.count(clue)==1 and guessed[word_list.index(clue)]==0:
			print("Hey, \""+response+"\"  is on the board already! You can't use that as a clue! Try a different one.")
		elif clue.count(" ") > 0:
			print("You can only provide one word as a clue! Try a different one.")
		elif not clue.isalpha():
			print("Hey now, you can't put non-alphabet characters in your clue! Try a different one.")
		elif not dict_check:
			print("\""+temp+"\" doesn't exist in the agents' vocabulary! Can you try a different one instead?")
		else:
			clue_done = true
			
	while not num_done:
		if py3:
			clue_num = input("Spy Master, how many guesses should your agents make?\n")
		else:
			clue_num = raw_input("Spy Master, how many guesses should your agents make?\n")
		clue_num = clue_num.strip()

		if not clue_num.isdigit():
			print("Hey, this isn't a number! Try again!")
		else:
			num_done = true
			clue_num = int(clue_num)
			
	return clue, clue_num


# Gets a prompt/clue from the spymaster, human or AI
def getPrompt():
	clue = "dummy clue"
	clue_num = 1

	valid_response=False
	if (current_team==BLUE_TEAM and blue_master_human) or (current_team==RED_TEAM and red_master_human):
		printWordGrid()
		while not valid_response:
			response = ""
			if py3:
				response = input("What prompt would you like to give?\n")
			else:
				response = raw_input("What prompt would you like to give?\n")
			
			#Format prompt for rule-checking
			response = response.strip()
			temp = response
			# temp = temp.capitalize()
			dict_check = True
			if current_team==BLUE_TEAM and not blue_spy_human: 
				temp = temp.lower()
				exists = blue_ai_agent.bankword_to_idx.get(temp)
				if exists==None: dict_check= False
			elif current_team==RED_TEAM and not red_spy_human:
				temp = temp.lower()
				exists = red_ai_agent.bankword_to_idx.get(temp)
				if exists==None: dict_check= False

			temp = temp.capitalize()
				
			#Rule-check
			if word_list.count(temp)==1 and guessed[word_list.index(temp)]==0:
				print("Hey, \""+response+"\"  is on the board already! You can't use that as a clue! Try a different one.")
			elif temp.count(" ")>0:
				print("You can only provide one word as a clue! Try a different one.")
			elif not temp.isalpha():
				print("Hey now, you can't put non-alphabet characters in your clue! Try a different one.")
			elif not dict_check:
				print("\""+temp+"\" doesn't exist in the agents' vocabulary! Can you try a different one instead?")
			else: 
				number = 0
				while not valid_response:
					if py3:
						number = input("How many words are there?\n")
					else:
						number = raw_input("How many words are there?\n")
					number = number.strip()
					if not number.isdigit():
						# print("Hey, this isn't a number! Now you have to start over because user edge-cases are annoying to handle =(")
						print("Hey, this isn't a number! Try again.")
					else: 
						# response = response.lower()
						# processPrompt(response,number)	
						clue = temp
						clue_num = int(number)
						valid_response=True
	elif current_team==BLUE_TEAM and not blue_master_human:
		clue, clue_num = blue_ai_master.createClue(word_list, word_grid)
	elif current_team==RED_TEAM and not red_master_human:
		clue, clue_num = red_ai_master.createClue(word_list, word_grid)
	else:
		print("This shouldn't be a thing for prompting")

	return clue, clue_num

#Returns a guess made by the players (human or AI) based off the clue
def getGuess(clue,clue_num):
	#Guesses must be processed after each on is made
	guess = "dummy guess"
	num_guesses = clue_num

	while num_guesses>0:
		valid_response=False
		if (current_team==BLUE_TEAM and blue_spy_human) or (current_team==RED_TEAM and red_spy_human):
			printWordGrid(SPY_VIEW)
			print("[Current turn: "+getTeamString(current_team)+", AGENTS]\n")
			while not valid_response:				
				print("Your clue is: "+clue+" "+str(num_guesses))
				response = ""
				if py3:
					response = input("What word would you like to guess? [Number of guesses left:"+str(num_guesses)+"]\n")
				else:
					response = raw_input("What word would you like to guess? [Number of guesses left:"+str(num_guesses)+"]\n")

				response = response.strip()
				response = response.capitalize()
				# Prevent users from making typos or guessing words not on the board
				if word_list.count(response)==0:
					print("\""+response+"\" isn't on the board! Try again.")
				else: 
					# response = response.lower()
					# processGuess(response)
					guess = response
					valid_response=True
					num_guesses-=1
		elif current_team==BLUE_TEAM and not blue_spy_human:
			query = clue.capitalize()
			guess = blue_ai_agent.makeGuesses(word_list, guessed,query,clue_num)
			num_guesses-=1
		elif current_team==RED_TEAM and not red_spy_human:
			query = clue.capitalize()
			guess = red_ai_agent.makeGuesses(word_list, guessed,query,clue_num)
			num_guesses-=1
		else:
			print("This shouldn't be a thing for guessing")

		guess = guess.capitalize()
		print("The agents guessed: "+guess)
		result = processGuess(guess,current_team)
		# If endTurn==True
		if result: 
			num_guesses=0
		
		#Teach AI

		#Have agents account for their guess being related (or not) to the clue based on correctness
		if current_team==BLUE_TEAM and not blue_spy_human:
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

		if current_team==RED_TEAM and not red_spy_human:
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
		if current_team==BLUE_TEAM and not blue_master_human:
			pass
			# query = clue.lower() 
			# Also get words that AI intended to be guessed, replaces guess in statement
			# #If the guess was wrong, the two are probably not related
			# if result:
			# 	blue_ai_agent.addIrrelevantEntry(query,guess)
			# 	blue_ai_agent.addIrrelevantEntry(guess,query)
			# #If the guess was correct, the two are probably related
			# else:
			# 	blue_ai_agent.addRelevantEntry(query,guess)
			# 	blue_ai_agent.addRelevantEntry(guess,query)

		if current_team==RED_TEAM and not red_master_human:
			pass
			# query = clue.lower()
			# Also get words that AI intended to be guessed, replaces guess in statement
			# #If the guess was wrong, the two are probably not related
			# if result:
			# 	red_ai_agent.addIrrelevantEntry(query,guess)
			# 	red_ai_agent.addIrrelevantEntry(guess,query)
			# #If the guess was correct, the two are probably related
			# else:
			# 	red_ai_agent.addRelevantEntry(query,guess)
			# 	red_ai_agent.addRelevantEntry(guess,query)


	# if is_spy_master==False:
	# 		response = input("What word would you like to guess?\n")
	# 		response = response.strip()
	# 		response = response.capitalize()
	# 		# Prevent users from making typos or guessing words not on the board
	# 		if word_list.count(response)==0:
	# 			print("\""+response+"\" isn't on the board! Try again.")
	# 		else: 
	# 			# response = response.lower()
	# 			processGuess(response)
	
	# processGuess(guess)

	# valid_response=False
	# if (current_team==BLUE_TEAM and blue_spy_human) or (current_team==RED_TEAM and red_spy_human):
	# 	printWordGrid()
	# 	while not valid_response:
	# 		response = ""
	# 		if py3:
	# 			response = input("What word would you like to guess?\n")
	# 		else:
	# 			response = raw_input("What word would you like to guess?\n")

	# 		response = response.strip()
	# 		response = response.capitalize()
	# 		# Prevent users from making typos or guessing words not on the board
	# 		if word_list.count(response)==0:
	# 			print("\""+response+"\" isn't on the board! Try again.")
	# 		else: 
	# 			# response = response.lower()
	# 			# processGuess(response)
	# 			guess = response
	# 			valid_response=True
	# elif current_team==BLUE_TEAM and not blue_spy_human:
	# 	query = clue.lower()
	# 	guess = blue_ai_agent.makeGuesses(word_list, guessed,query,clue_num)
	# elif current_team==RED_TEAM and not red_spy_human:
	# 	query = clue.lower()
	# 	guess = red_ai_agent.makeGuesses(word_list, guessed,query,clue_num)
	# else:
	# 	print("This shouldn't be a thing for guessing")



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
	print("\t"+getTeamString(BLUE_TEAM)+": "+str(blue_words)+" cards remaining")
	print("\t"+getTeamString(RED_TEAM)+": "+str(red_words)+" cards remaining")
	# print("\t Civilian words: "+str(red_words))
	print("\t The assasian word was "+assasian_word)

	#Check for win/lose conditions

	#Have the AI save their Rocchios in case they were modified during the game

	# if not blue_master_human:
	# 	print("The blue spymaster is being dismissed...")
	# 	blue_ai_master.saveRocchios()

	# if not red_master_human:
	# 	print("The red spymaster is being dismissed...")
	# 	red_ai_master.saveRocchios()

	# if not blue_spy_human:
	# 	print("The blue agents are being dismissed...")
	# 	blue_ai_agent.saveRocchios()

	# if not red_spy_human:
	# 	print("The red agents are being dismissed...")
	# 	red_ai_agent.saveRocchios()
	

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

		print("[Current turn: "+getTeamString(current_team)+", MASTER]\n")

		clue, clue_num = getPrompt()
		# processPrompt(clue, clue_num)

		# print("[Current turn: "+getTeamString(current_team)+", AGENTS]\n")
		# print("Your clue is: "+clue+" "+str(clue_num))
		getGuess(clue,clue_num)
		# guess = getGuess(clue,clue_num)
		# processGuess(guess)

		

		# if is_spy_master==False:
		# 	response = input("What word would you like to guess?\n")
		# 	response = response.strip()
		# 	response = response.capitalize()
		# 	# Prevent users from making typos or guessing words not on the board
		# 	if word_list.count(response)==0:
		# 		print("\""+response+"\" isn't on the board! Try again.")
		# 	else: 
		# 		# response = response.lower()
		# 		processGuess(response)
		# else:
		# 	response = input("What prompt would you like to give?\n")
		# 	#Format prompt for rule-checking
		# 	response = response.strip()
		# 	temp = response
		# 	# temp.replace("_", " ")
		# 	# temp.replace("-", " ")
		# 	# temp.replace(" ", "")
		# 	# ^isalpha() takes care of most of these
		# 	temp = temp.capitalize()
		# 	#Rule-check
		# 	if word_list.count(temp)==1 and guessed[word_list.index(temp)]==0:
		# 		print("Hey, \""+response+"\"  is on the board already! You can't use that as a clue! Try a different one.")
		# 	elif temp.count(" ")>0:
		# 		print("You can only provide one word as a clue! Try a different one.")
		# 	elif not temp.isalpha():
		# 		print("Hey now, you can't put non-alphabet characters in your clue! Try a different one.")
		# 	else: 
		# 		number = input("How many words are there?\n")
		# 		if not number.isdigit():
		# 			print("Hey, this isn't a number! Now you have to start over because user edge-cases are annoying to handle =(")
		# 		else: 
		# 			# response = response.lower()
		# 			processPrompt(response,number)			
			# if word_list.count(temp)==1 && guessed(word_list.index(temp))==0:
			# 	print("Hey, that word is on the board! You can't use that as a clue! Try a different one.")
			# else: processPrompt(response,number)
		current_team = (current_team+1)%2



def main():
	global game_state
	global blue_master_human
	global blue_spy_human
	global red_master_human
	global red_spy_human
	
	# TODO ask if there are human players for both teams
	# TODO ask which team the player wants to be on if only one team has human players

	response = ""
		
	#Check human spy master for blue team
	valid_response = False
	while not valid_response:
		if py3:
			response = input("Will there be a human spy master for the blue team? [Yes/No]\n")
		else:
			response = raw_input("Will there be a human spy master for the blue team? [Yes/No]\n")
		response = response.strip()
		response = response.capitalize()
		if response == "Yes":
			blue_master_human = True
			print("Humans will be the spy master for the blue team\n")
			valid_response=True
		elif response == "No":
			blue_master_human = False
			print("An AI will be the spy master for the blue team\n")
			valid_response=True
		else:
			print("I'm sorry, I didn't understand that\n")

	#Check human spy agent(s) for blue team
	valid_response = False
	while not valid_response:
		if py3:
			response = input("Will there be human agents for the blue team? [Yes/No]\n")
		else:
			response = raw_input("Will there be human agents for the blue team? [Yes/No]\n")
		response = response.strip()
		response = response.capitalize()
		if response == "Yes":
			blue_spy_human = True
			print("Human agents will be on the blue team\n")
			valid_response=True
		elif response == "No":
			blue_spy_human = False
			print("AI agents be on the blue team\n")
			valid_response=True
		else:
			print("I'm sorry, I didn't understand that\n")

	#Check human spy master for red team
	valid_response = False
	while not valid_response:
		if py3:
			response = input("Will there be a human spy master for the red team? [Yes/No]\n")
		else:
			response = raw_input("Will there be a human spy master for the red team? [Yes/No]\n")

		response = response.capitalize()
		if response == "Yes":
			red_master_human = True
			print("Humans will be the spy master for the red team\n")
			valid_response=True
		elif response == "No":
			red_master_human = False
			print("An AI will be the spy master for the red team\n")
			valid_response=True
		else:
			print("I'm sorry, I didn't understand that\n")

	#Check human spy agent(s) for red team
	valid_response = False
	while not valid_response:
		if py3:
			team_req = input("Will there be human agents for the red team? [Yes/No]\n")
		else:
			team_req = raw_input("Will there be human agents for the red team? [Yes/No]\n")
		team_req = team_req.capitalize()
		if team_req == "Yes":
			red_spy_human = True
			print("Human agents will be on the red team\n")
			valid_response=True
		elif team_req == "No":
			red_spy_human = False
			print("AI agents be on the red team\n")
			valid_response=True
		else:
			print("I'm sorry, I didn't understand that\n")

	#Create game elements
	createGame()
	game_state = GAME_IN_PROGRESS #TODO Should this be defined here?
	#Start the loop
	gameLoop()
	print("Bye =3 xx3")




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
				response = input("Would you like to play again?[Yes/No]")
			else: 
				response = raw_input("Would you like to play again?[Yes/No]")
			response = response.strip()
			response = response.capitalize()
			if response == "Yes":
				game_state=GAME_RESET
				valid_response=True
				print("Another game will be started then!\n")
			elif response == "No":
				game_state=GAME_END
				valid_response=True
				print("Thanks for playing! =D\n")
			else: print("Sorry, I didn't understand that. Try again?\n")


# 
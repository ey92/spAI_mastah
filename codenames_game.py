### Created 04/17/2017 by Lauren Hsu and Elizabeth Yam
import numpy as np 

DICTIONARY_FILE = "test.txt"
BLUE_TEAM = 0
RED_TEAM = 1
CIVILIAN = 2
ASSASIAN = 3

GAME_START = 0
GAME_RESET = 1
GAME_IN_PROGRESS = 2
GAME_END = 3

game_state = GAME_START
is_spy_master = False
current_team = 0
red_words = 8
blue_words = 8
total_words = 25
word_grid = {}
word_list = []
guessed = [0]*total_words

#TODO Distinguish agent vs. spy master input/output and actions and logic processsing and everything
#TODO Finish game loop
#TODO COLORS


def createGame():
	##Decide if red or blue goes first
	coin_flip = random.randint(0,1)
	
	#Hard-coded incase of reset
	if coin_flip==BLUE_TEAM:
		blue_words = 9
		red_words = 8
	else:
		blue_words = 8
		red_words = 9
	
	#Create word grid + assign words to teams
	createWordGrid()

def printWordGrid():
	for x in range(0,5):
		for y in range(0,5):
			position = y+(x*5)
			#If word HAS NOT been guessed yet
			#TODO Colors
			if guessed[position]==0:
				print(word_list[position]+guessed[position]+"\t\t")
			else:
				print(word_list[position]+guessed[position]+"\t\t")
		print()



#Create word grid with assigning words to teams
def createWordGrid():
	##Get random set of words in a dictionary
	#Assigned here incase of reset
	word_grid = {} #GLOBAL
	word_list = [] #GLOBAL

	#TODO actually get words
	

	##Assign key as word w/ value as BLUE_TEAM, RED_TEAM, CIVILIAN, or ASSASIAN

	# blue_num = blue_words
	# red_num = red_words
	assasian_num = 1
	civilian_num = total_words-blue_words-red_words-assasian_num

	#Insert blue into assigning order
	assign_order = [BLUE_TEAM]*blue_words

	#Insert red in assigning order
	for i in range(0,blue_words):
		assign_num = random.randint(0,assign_order.length()-1)
		assign_order.insert(assign_num,RED_TEAM)

	#Insert civilian in assigning order
	for i in range(0,civilian_num):
		assign_num = random.randint(0,assign_order.length()-1)
		assign_order.insert(assign_num,CIVILIAN)

	#Insert assasian in assigning order
	assign_num = random.randint(0,assign_order.length()-1)
	assign_order.insert(assign_num,ASSASIAN)

	#Assign words a label
	for i in range(0,word_list.length()):
		word = word_list[i]
		assign_num = assign_order[i]
		word_grid.update({word:assign_num})
		
		# assign_num = random.randint(0,3)
		# word_grid.update({word:assign_num})
		# if assign_num==0:			
		# 	blue_num-=1
		# elif assign_num==1:
		# 	red_num-=1
		# elif assign_num==2:
		# 	civilian_num-=1
		# elif assign_num==3:
		# 	assasian_num-=1


#Processes a guess made by an agent
def processGuess(response):
	pass

#Processes a hint given by the spy master
def processPrompt(response,number):
	pass


def gameLoop():
	while game_state==GAME_IN_PROGRESS:
		printWordGrid()

		if is_spy_master==False:
			response = input("What word would you like to guess?\n")
			processGuess(response)
		else:
			response = input("What prompt would you like to give?\n")
			number = input("How many words are there?\n")
			processPrompt(response,number)




def main():
	print("Welcome to Codenames!\n")
	response = input("Would you like to be spy master? [Yes/No]\n")
	response.capitalize()

	if response == "Yes":
		is_spy_master = True
		print("You will be the spy master for your team\n")
	elif response == "No":
		print("You will be a regular agent for your team\n")
	else:
		print("Your response could not be read, you have been defaulted to not being spy master\n")

	createGame()

	gameLoop()

	print("Bye =3 xx3")



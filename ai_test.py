import codenames_game as gm 
import codenames_ai as ai
import random
import pickle

DICTIONARY_FILE = "words.txt"
word_list = []
word_grid = {}
assasian_word = ""
blue_words = 9
red_words = 8
civilian_num = 7
BLUE_TEAM = 0
RED_TEAM = 1
CIVILIAN = 2
ASSASIAN = 3
word_guessed = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
word_guessed2 = [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0]
total_words = 25

test_list=['pitch', 'canada', 'fork', 'model', 'cloak', 'pass', 'washer', 'sock', 'tap', 'track', 'sink', 'organ', 'watch', 'lap', 'state', 'crash', 'tail', 'parachute', 'kangaroo', 'green', 'pyramid', 'rock', 'school', 'head', 'check']
test_list2=['block', 'limousine', 'buck', 'berlin', 'life', 'compound', 'degree', 'cover', 'sound', 'cliff', 'australia', 'horseshoe', 'lock', 'arm', 'centaur', 'tower', 'green', 'mole', 'germany', 'scorpion', 'pool', 'ruler', 'film', 'duck', 'hospital']
test_list3=['face', 'smuggler', 'switch', 'field', 'tube', 'egypt', 'plot', 'cricket', 'tooth', 'alps', 'soul', 'bank', 'spy', 'fly', 'kid', 'pistol', 'eagle', 'glove', 'snowman', 'compound', 'bolt', 'diamond', 'king', 'cloak', 'ruler']

test_list4 = ['light', 'net', 'glove', 'moon', 'cell', 'spy', 'swing', 'spike', 'ship', 'greece', 'boom', 'maple', 'snowman', 'vet', 'america', 'iron', 'jack', 'dog', 'olive', 'battery', 'centaur', 'cricket', 'green', 'tablet', 'pupil']
test_grid4 = {'vet': 2, 'tablet': 2, 'light': 2, 'swing': 0, 'dog': 0, 'glove': 2, 'moon': 2, 'cell': 0, 'green': 1, 'boom': 3, 'iron': 1, 'spike': 1, 'net': 1, 'snowman': 1, 'spy': 1, 'cricket': 0, 'battery': 2, 'centaur': 1, 'jack': 0, 'greece': 1, 'olive': 2, 'ship': 0, 'america': 0, 'maple': 0, 'pupil': 0}

test_list5 = ['glove', 'back', 'bomb', 'yard', 'rock', 'screen', 'hawk', 'box', 'watch', 'missile', 'china', 'telescope', 'spine', 'ball', 'switch', 'antactica', 'soldier', 'stream', 'lemon', 'cook', 'spot', 'moon', 'engine', 'war', 'sink']
test_grid5 = {'box': 1, 'yard': 2, 'spine': 2, 'watch': 3, 'antactica': 2, 'glove': 2, 'moon': 2, 'soldier': 0, 'switch': 0, 'rock': 1, 'lemon': 0, 'war': 0, 'engine': 1, 'ball': 1, 'bomb': 1, 'telescope': 1, 'stream': 2, 'screen': 0, 'spot': 1, 'back': 2, 'missile': 1, 'china': 0, 'sink': 0, 'cook': 0, 'hawk': 0}

test_list6 = ['india', 'field', 'ground', 'life', 'mexico', 'deck', 'stick', 'canada', 'pan', 'bat', 'lap', 'bark', 'washington', 'cliff', 'organ', 'atlantis', 'heart', 'dwarf', 'angel', 'buck', 'space', 'grace', 'nail', 'germany', 'temple']
test_grid6 = {'canada': 0, 'buck': 2, 'bat': 1, 'organ': 2, 'space': 0, 'india': 1, 'field': 0, 'temple': 0, 'pan': 2, 'heart': 0, 'life': 0, 'atlantis': 0, 'dwarf': 1, 'angel': 1, 'mexico': 1, 'deck': 1, 'washington': 3, 'nail': 2, 'germany': 0, 'stick': 2, 'bark': 2, 'ground': 0, 'lap': 2, 'grace': 1, 'cliff': 1}

def getWords():
	# grid_words = []
	global word_list
	word_list.clear()

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

def createWordGrid():
	# global word_list
	global word_grid
	global word_list
	global assasian_word

	word_grid.clear()
	##Get random set of words in a dictionary
	#Assigned here incase of reset
	# word_grid = {} #GLOBAL
	# word_list = [] #GLOBAL, resets for every game

	#Populates word_list
	# word_list = getWords()	
	# getWords()

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


if __name__ == "__main__":
	test = ai.spyAgent(1)
	# makeGuesses(self,word_list, guessed,clue,num_words)

	print("Test list 1")
	print(test.makeGuesses(test_list,word_guessed,"apparel",25))
	print("\n")
	print("\n")

	print("Test list 2")
	print(test.makeGuesses(test_list2,word_guessed,"animal",25))
	print("\n")
	print("\n")

	print("Test list 3")
	print(test.makeGuesses(test_list3,word_guessed,"animal",25))
	print("\n")
	print("\n")

	# print("Test list 1")
	# print(test.makeGuesses(test_list,word_guessed2,"apparel",10))
	# print("\n")
	# print("\n")

	# print("Test list 2")
	# print(test.makeGuesses(test_list2,word_guessed2,"animal",10))
	# print("\n")
	# print("\n")

	# print("Test list 3")
	# print(test.makeGuesses(test_list3,word_guessed2,"animal",10))
	# print("\n")
	# print("\n")

	# word_guessed = []

	# counter
	# while len(word_guessed)<25:
	# 	word_guessed[]
	



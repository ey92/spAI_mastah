import codenames_game as gm 
import codenames_ai as ai
import random
import cPickle as pickle

DICTIONARY_FILE = "words.txt"
word_list = []
word_guessed = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
word_guessed2 = [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0]
total_words = 25

test_list=['pitch', 'canada', 'fork', 'model', 'cloak', 'pass', 'washer', 'sock', 'tap', 'track', 'sink', 'organ', 'watch', 'lap', 'state', 'crash', 'tail', 'parachute', 'kangaroo', 'green', 'pyramid', 'rock', 'school', 'head', 'check']
test_list2=['block', 'limousine', 'buck', 'berlin', 'life', 'compound', 'degree', 'cover', 'sound', 'cliff', 'australia', 'horseshoe', 'lock', 'arm', 'centaur', 'tower', 'green', 'mole', 'germany', 'scorpion', 'pool', 'ruler', 'film', 'duck', 'hospital']
test_list3=['face', 'smuggler', 'switch', 'field', 'tube', 'egypt', 'plot', 'cricket', 'tooth', 'alps', 'soul', 'bank', 'spy', 'fly', 'kid', 'pistol', 'eagle', 'glove', 'snowman', 'compound', 'bolt', 'diamond', 'king', 'cloak', 'ruler']

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
	



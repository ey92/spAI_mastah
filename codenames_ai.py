### Created 04/17/2017 by Lauren Hsu and Elizabeth Yam
import numpy as np 
import rocchio as ro

# CODENAMES_WORDLIST = "words_to_process.txt"
BANKWORDS_PICKLE = "knowledge/idx_to_lemma.pickle"
INVERTED_BANKWORDS_PICKLE = "knowledge/lemma_to_idx.pickle"
CODEWORDS_PICKLE = "knowledge/idx_to_codeword.pickle"
INVERTED_CODEWORDS_PICKLE = "knowledge/codeword_to_idx.pickle"

SIM_PICKLE_HEAD = "knowledge/sim_matrix"
RELEVANT_PICKLE = "knowledge/relevant.pickle"
IRRELEVANT_PICKLE = "knowledge/irrelevant.pickle"

class spyPlayer():
	def __init__(self, team_num):
    self.sim_matrix = self.generateSimMatrix()
    self.rel_pool = self.generateRelRocchio()
    self.irrel_pool = self.generateIrrelRocchio()
    self.team_num = team_num
    self.idx_to_bankword = self.generateBankWordMap()
    self.bankword_to_idx = self.generateInvertedBankWord()
		self.idx_to_codeword = self.generateCodeWordMap()
		self.codeword_to_idx = self.generateInvertedCodeWord()

    def generateSimMatrix():
    	"""Returns a numpy array mapping Codename words to other possible words"""
    	
    	#Should trim it such that only contains the words pertaining to the game
    	pass

    def generateRelRocchio():
    	rel_dict = {}
			with open(RELEVANT_PICKLE,'rb') as f:
        rel_dict = pickle.load(f)

     	return rel_dict

    def generateIrrelRocchio():
    	irrel_dict = {}
			with open(IRRELEVANT_PICKLE,'rb') as f:
        irrel_dict = pickle.load(f)

     	return irrel_dict

    def generateBankWordMap():
    	wordmap = []
			with open(BANKWORDS_PICKLE,'rb') as f:
        wordmap = pickle.load(f)

      return wordmap

    def generateInvertedBankWord():
    	wordmap = {}
			with open(INVERTED_BANKWORDS_PICKLE,'rb') as f:
        wordmap = pickle.load(f)

     	return wordmap

    def generateCodeWordMap():
			wordmap = []
			with open(CODEWORDS_PICKLE,'rb') as f:
        wordmap = pickle.load(f)

      return wordmap

		def generateInvertedCodeWord():
			wordmap = {}
			with open(INVERTED_CODEWORDS_PICKLE,'rb') as f:
        wordmap = pickle.load(f)

     	return wordmap


class spyMaster(spyPlayer):

	def interpretGameboard(word_grid):
		"""Returns a 4-tuple of the words REMAINING for the spy master's team, 
		   the opposing team, the civilians, and the assasin (represented by boom)
		   Note: Already guessed words are noted by a negative sign"""
    team_words = []
    opp_words = []
    civ_words = []
    boom_word = ""

    opp_num = (self.team_num+1)%2
    civ_num = 2
    boom_num = 3

		for word in word_grid.keys():
			word_id = word_grid.get(word)
			if word_id == self.team_num: team_words.append(word)
			elif word_id == opp_num: opp_words.append(word)
			elif word_id == civ_num: civ_words.append(word)
			elif word_id == boom_num: boom_word = word
			else: print("Why is there a "+word_id+" in the processing?!?!?")

		return team_words, opp_words, civ_words, boom_word


	# def getTeamWords(word_grid):
	# 	"""Returns a list of the words REMAINING for the spy master's team
	# 	   Note: Already guessed words are noted by a negative sign"""
	# 	team_words = []
	# 	for word in word_grid.keys():
	# 		if word_grid.get(word) == self.team_num: team_words.append(word)

	# 	return team_words
    	

 #    def getOppWords(word_grid):
 #    	"""Returns a list of the words REMAINING for the opposing team
	# 	   Note: Already guessed words are noted by a negative sign"""
 #    	opp_num = (self.team_num+1)%2
 #    	opp_words = []
	# 	for word in word_grid.keys():
	# 		if word_grid.get(word) == self.opp_num: opp_words.append(word)

	# 	return opp_words

	# def getCivWords(word_grid):
 #    	"""Returns a list of the words REMAINING civilian words
	# 	   Note: Already guessed words are noted by a negative sign"""
 #    	civ_num = 2
 #    	civ_words = []
	# 	for word in word_grid.keys():
	# 		if word_grid.get(word) == self.civ_num: civ_words.append(word)

	# 	return opp_words

	# def getBoomWord(word_grid):
 #    	"""Returns a list of the words REMAINING civilian words
	# 	   Note: Already guessed words are noted by a negative sign"""
 #    	boom_num = 3
 #    	boom_words = []
	# 	for word in word_grid.keys():
	# 		if word_grid.get(word) == self.boom_num: boom_words.append(word)

	# 	return boom_words

  def createClue(word_list, word_grid):
  	"""
  		game_board: dictionary containing the "identity of each word"
  	"""
  	clue = ""
  	clue_num = 1

  	team_words, opp_words, civ_words, boom_word = self.interpretGameboard(word_grid)
  	
  	return clue, clue_num


class spyAgent(spyPlayer):

	#Make a mapping of possible words to Codename words
	self.sim_matrix = np.transpose(self.sim_matrix) #TODO Check if this is the correct way to reference

	def getNonGuessed(word_list, guessed):
		"""Returns a list of the words that have not been guessed yet"""
		not_guessed = []
		for i in range(0,len(guessed)):
			if guessed[i]==0: not_guessed.append(word_list[i])
		
		return not_guessed

  # NOTE: returns a LIST of guesses, must be iterated through in order to process in main game
  def makeGuesses(word_list, guessed,clue,num_words):
  	guesses = []

  	word_choices = self.getNonGuessed(word_list, guessed)

  	# Get sim vector for the clue
  	clue_vec = self.idx_to_bankword

  	# Rocchio with sim vectors for synonyms of the clue

  	# Get argsort of resulting vector as ranking

  	# While len(guesses) < num_words
	  	#Iterate through ranking via counter
	  	#if idx_to_codeword[counter] is in word_list
	  		#Append result to guesses


  	return guesses



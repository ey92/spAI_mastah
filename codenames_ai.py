### Created 04/17/2017 by Lauren Hsu and Elizabeth Yam
import numpy as np 
import rocchio as ro
import pickle

#List of words in the English language
BANKWORDS_PICKLE = "knowledge/idx_to_lemma.pickle"
#Inverted index to access words in the English language
INVERTED_BANKWORDS_PICKLE = "knowledge/lemma_to_idx.pickle"
#List of words possible in Codenames
CODEWORDS_PICKLE = "knowledge/idx_to_codeword.pickle"
#Inverted index to access words possible in Codenames
INVERTED_CODEWORDS_PICKLE = "knowledge/codeword_to_idx.pickle"
#Similarity matrix mapping "Codename" words to "English" words
SIM_PICKLE_HEAD = "knowledge/sim_matrix"
#Dictionary mapping words to lists their related/unrelated words, used for Rocchio algorithm
RELEVANT_PICKLE = "knowledge/relevant_rocchio.pickle"
IRRELEVANT_PICKLE = "knowledge/irrelevant_rocchio.pickle"

#Constant weights for Rocchio
ALPHA_ROCC = 0.5
BETA_ROCC = 0.8
GAMMA_ROCC = 0.6

class spyPlayer():
	def __init__(self, team_num):
		self.team_num = team_num
		self.sim_matrix = self.generateSimMatrix()
		self.rel_pool = self.generateRelRocchio()
		self.irrel_pool = self.generateIrrelRocchio()
		self.idx_to_bankword = self.generateBankWordMap()
		self.bankword_to_idx = self.generateInvertedBankWord() 		# lemmas
		self.idx_to_codeword = self.generateCodeWordMap()
		self.codeword_to_idx = self.generateInvertedCodeWord()		# dict {"key = word", value = idx}

	def generateSimMatrix(self):
		"""Returns a numpy array mapping Codename words to other possible words"""
		sim_mat = np.empty([400,6459])
		with open(SIM_PICKLE_HEAD+str("1")+".pickle",'rb') as f:
			sim_mat = pickle.load(f)

		return sim_mat
		
		#Should trim it such that only contains the words pertaining to the game?
	def generateRelRocchio(self):
		rel_dict = {}
		with open(RELEVANT_PICKLE,'rb') as f:
			rel_dict = pickle.load(f)	

		return rel_dict

	def generateIrrelRocchio(self):
		irrel_dict = {}
		with open(IRRELEVANT_PICKLE,'rb') as f:
			irrel_dict = pickle.load(f)	

		return irrel_dict

	def generateBankWordMap(self):
		wordmap = []
		with open(BANKWORDS_PICKLE,'rb') as f:
			wordmap = pickle.load(f)	

		return wordmap

	def generateInvertedBankWord(self):
		wordmap = {}
		with open(INVERTED_BANKWORDS_PICKLE,'rb') as f:
			wordmap = pickle.load(f)
	
		return wordmap

	def generateCodeWordMap(self):
		wordmap = []
		with open(CODEWORDS_PICKLE,'rb') as f:
			wordmap = pickle.load(f)
	
		return wordmap

	def generateInvertedCodeWord(self):
		wordmap = {}
		with open(INVERTED_CODEWORDS_PICKLE,'rb') as f:
			wordmap = pickle.load(f)
	
		return wordmap

	def getRelevantEntry(self,word):
		return self.rel_pool.get(word,[])

	def getIrrelevantEntry(self,word):
		return self.irrel_pool.get(word,[])

	def addRelevantEntry(self,word,rel_entry):
		temp = self.getRelevantEntry(word)
		temp.append(rel_entry)
		self.rel_pool.update({word:temp})

	def addIrelevantEntry(self,word,irrel_entry):
		temp = self.getIrrelevantEntry(word)
		temp.append(irrel_entry)
		self.irrel_pool.update({word:temp})

	def saveRocchios(self):
		original_rel = self.generateRelRocchio()
		original_irrel = self.generateIrrelRocchio()

		#Update original relevant rocchio with only NEW entries made during the game 
		#Done this way to prevent lose of data from overwritting from multiple AI
		for entry in self.rel_pool.keys():
			original_list = original_rel.get(entry,[])
			new_list = self.getRelevantEntry(entry)
			for new_word in new_list:
				if original_list.count(new_word)==0: original_list.append(new_word)

			original_rel.update({entry:original_list})

		with open(RELEVANT_PICKLE,'wb') as f:
			pickle.dump(original_rel,f, protocol=2)


		#Update original irrelevant rocchio with only NEW entries made during the game 
		#Done this way to prevent lose of data from overwritting from multiple AI
		for entry in self.irrel_pool.keys():
			original_list = original_irrel.get(entry,[])
			new_list = self.getIrrelevantEntry(entry)
			for new_word in new_list:
				if original_list.count(new_word)==0: original_list.append(new_word)

			original_irrel.update({entry:original_list})

		with open(IRRELEVANT_PICKLE,'wb') as f:
			pickle.dump(original_irrel,f, protocol=2)


class spyMaster(spyPlayer):	

	def interpretGameboard(self,word_grid):
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
			# else: print("Why is there a "+str(word_id)+" in the processing?!?!?")

		return team_words, opp_words, civ_words, boom_word

	def createClue(self,word_list, word_grid):
		"""Creates a clue based off the state of the gameboard [word_grid]
			word_grid: dictionary containing the "identity of each word"
		"""
		clue = "ax"
		clue_num = 1

		team_words, opp_words, civ_words, boom_word = self.interpretGameboard(word_grid)

		#Find words most relevant to each other
		# self.sim_matrix
		# team_indexs = [self.codeword_to_idx.get(x) for x in team_words]
		# opp_indexs = [self.codeword_to_idx.get(x) for x in opp_words]
		# civ_indexs = [self.codeword_to_idx.get(x) for x in civ_words]
		# boom_index = [self.codeword_to_idx.get(x) for x in boom_word]

		# top_team_idxs = []
		# top_opp_idxs = []
		# top_civ_idxs = []
		# top_boom_idxs = self.codeword_to_idx[boom_index].argsort()[::-1][:]

		# ind_max = max(len(team_indexs),len(opp_indexs),len(civ_indexs),len(boom_index))
		
		# for i in ind_max:
		# 	if i < len(team_indexs):
		# 		idx = team_indexs[i]
		# 		top_team_idxs.append(self.codeword_to_idx[idx].argsort()[::-1][:])
		# 	if i < len(opp_indexs):
		# 		idx = opp_indexs[i]
		# 		top_opp_idxs.append(self.codeword_to_idx[idx].argsort()[::-1][:])
		# 	if i < len(civ_indexs):
		# 		idx = civ_indexs[i]
		# 		top_civ_idxs.append(self.codeword_to_idx[idx].argsort()[::-1][:])

		#Rocchio away the synonyms of the opp_words, civ_words, and boom_word
		
		return clue, clue_num


class spyAgent(spyPlayer):
	def __init__(self, team_num):
		spyPlayer.__init__(self,team_num)
		#Make a mapping of possible words to Codename words
		# print("Before")
		# print(self.sim_matrix)
		self.sim_matrix = np.transpose(self.sim_matrix) 
		# print("After")
		# print(self.sim_matrix)

	def getNonGuessed(self,word_list, guessed):
		"""Returns a list of the words that have not been guessed yet"""
		not_guessed = []
		for i in range(0,len(guessed)):
			if guessed[i]==0: not_guessed.append(word_list[i])
		
		return not_guessed

	# def computeRocchio(self,word_vec):
	def computeRocchio(self,word):
		rel_words = self.rel_pool.get(word,[])
		irrel_words = self.irrel_pool.get(word,[])
		
		#Get sim vector for word, mult. by alpha term
		sim_idx = self.bankword_to_idx.get(word)
		sim_vector = self.sim_matrix[sim_idx]
		sim_size = np.shape(sim_vector)
		# print(sim_size)
		
		#Define accumulators
		alpha_term = np.empty([sim_size[0],])
		beta_term = np.empty([sim_size[0],])
		gamma_term = np.empty([sim_size[0],])
		
		alpha_term = ALPHA_ROCC*sim_vector

		# print("Alpha")
		# print(alpha_term)
		# print(np.shape(alpha_term))		

		#For each relevant word
		for rel_word in rel_words:
			#Get sim vector of rel_word
			rel_idx = self.bankword_to_idx.get(rel_word)
			rel_vector = self.sim_matrix[rel_idx]
			beta_term+=rel_vector
		
		#Account for divide by zero
		b_frac = 0
		if len(rel_words)>0: b_frac = BETA_ROCC/len(rel_words)
		beta_term = b_frac*beta_term

		# print("Beta")
		# print(beta_term)
		# print(np.shape(beta_term))

		#For each irrelevant word
		for irrel_word in irrel_words:
			#Get sim vector of irrel_word
			irrel_idx = self.bankword_to_idx.get(irrel_word)
			irrel_vector = self.sim_matrix[irrel_idx]
			gamma_term+=irrel_vector
		#Account for divide by zero
		c_frac = 0
		if len(irrel_words)>0: c_frac = GAMMA_ROCC/len(irrel_words)
		gamma_term = c_frac*gamma_term

		# print("Gamma")
		# print(gamma_term)
		# print(np.shape(gamma_term))		

		#Calculate updated query
		mod_vec = alpha_term + beta_term - gamma_term

		#Lowest value allowed is 0
		for i in range(0,mod_vec.size):
			# print(mod_vec[i])
			# print(np.shape(mod_vec[i]))
			mod_vec[i] = max(0,mod_vec[i])

		return mod_vec

	# NOTE: returns a LIST of guesses, must be iterated through in order to process in main game
	def makeGuesses(self,word_list, guessed,clue,num_words):
		guesses = []

		# USE INSTEAD OF WORD_LIST
		word_choices = self.getNonGuessed(word_list, guessed)

		# Get sim vector for the clue
		clue_idx = self.bankword_to_idx.get(clue)
		clue_vec = self.sim_matrix[clue_idx]

		# Rocchio with sim vectors for synonyms and antonyms of the clue
		query = clue.lower()
		mod_clue_vec = self.computeRocchio(query)

		# Get argsort of resulting vector as ranking
		ranking = np.argsort(mod_clue_vec)
		# Change from ascending to descending order
		ranking = np.flip(ranking,0)

		#Get most similar words in word_grid
		# counter = 0
		# #Only get the number of words guessed
		# while len(guesses)<num_words:
		# 	code_check = ranking[counter]
		# 	codeword = self.idx_to_codeword[code_check] 
		# 	#Only append the most similar word if it's on the board
		# 	if word_choices.count(codeword) ==1: guesses.append(codeword)
		# 	counter+=1

		# return guesses

		# Get most similar word besides the query itself
		# code_check = ranking[1]
		# codeword = self.idx_to_codeword[code_check] 
		# codeword = codeword.capitalize()

		print("Clue for guessing is: "+clue)
		print(np.shape(ranking))

		counter = 0
		#Only get the number of words guessed
		while len(guesses)<1:
			print(word_choices)
			# print(counter)
			code_check = ranking[counter]
			print(code_check)
			codeword = self.idx_to_codeword[code_check] 
			# print(codeword)
			#Only append the most similar word if it's on the board
			codeword = codeword.capitalize()
			print(codeword)
			if word_choices.count(codeword) ==1: guesses.append(codeword)
			counter+=1

		return guesses[0]



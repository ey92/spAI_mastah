### Created 04/17/2017 by Lauren Hsu and Elizabeth Yam
import numpy as np 
import rocchio as ro
import pickle

# CODENAMES_WORDLIST = "words_to_process.txt"
BANKWORDS_PICKLE = "knowledge/idx_to_lemma.pickle"
INVERTED_BANKWORDS_PICKLE = "knowledge/lemma_to_idx.pickle"
CODEWORDS_PICKLE = "knowledge/idx_to_codeword.pickle"
INVERTED_CODEWORDS_PICKLE = "knowledge/codeword_to_idx.pickle"

SIM_PICKLE_HEAD = "knowledge/sim_matrix"
RELEVANT_PICKLE = "knowledge/relevant_rocchio.pickle"
IRRELEVANT_PICKLE = "knowledge/irrelevant_rocchio.pickle"

ALPHA_ROCC = 0.3
BETA_ROCC = 0.3
GAMMA_ROCC = 0.8

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
			# file = f.read()
			# # print(file)
			# sim_mat = pickle.loads(file)
			sim_mat = pickle.load(f)

		return sim_mat
		
		#Should trim it such that only contains the words pertaining to the game?
	def generateRelRocchio(self):
		rel_dict = {}
		with open(RELEVANT_PICKLE,'rb') as f:
			rel_dict = pickle.load(f)

		# rel_dict = pickle.loads(RELEVANT_PICKLE)

		return rel_dict

	def generateIrrelRocchio(self):
		irrel_dict = {}
		with open(IRRELEVANT_PICKLE,'rb') as f:
			irrel_dict = pickle.load(f)

		# irrel_dict = pickle.loads(IRRELEVANT_PICKLE)

		return irrel_dict

	def generateBankWordMap(self):
		wordmap = []
		with open(BANKWORDS_PICKLE,'rb') as f:
			wordmap = pickle.load(f)

		# wordmap = pickle.loads(BANKWORDS_PICKLE)

		return wordmap

	def generateInvertedBankWord(self):
		wordmap = {}
		with open(INVERTED_BANKWORDS_PICKLE,'rb') as f:
			wordmap = pickle.load(f)

		# wordmap = pickle.loads(INVERTED_BANKWORDS_PICKLE)

		return wordmap

	def generateCodeWordMap(self):
		wordmap = []
		with open(CODEWORDS_PICKLE,'rb') as f:
			wordmap = pickle.load(f)

		# wordmap = pickle.loads(CODEWORDS_PICKLE)

		return wordmap

	def generateInvertedCodeWord(self):
		wordmap = {}
		with open(INVERTED_CODEWORDS_PICKLE,'rb') as f:
			wordmap = pickle.load(f)

		# wordmap = pickle.loads(INVERTED_CODEWORDS_PICKLE)

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
			pickle.dump(original_rel,f)


		#Update original irrelevant rocchio with only NEW entries made during the game 
		#Done this way to prevent lose of data from overwritting from multiple AI
		for entry in self.irrel_pool.keys():
			original_list = original_irrel.get(entry,[])
			new_list = self.getIrrelevantEntry(entry)
			for new_word in new_list:
				if original_list.count(new_word)==0: original_list.append(new_word)

			original_irrel.update({entry:original_list})

		with open(IRRELEVANT_PICKLE,'wb') as f:
			pickle.dump(original_irrel,f)


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
			else: print("Why is there a "+word_id+" in the processing?!?!?")

		return team_words, opp_words, civ_words, boom_word

	def createClue(self,word_list, word_grid):
		"""Creates a clue based off the state of the gameboard [word_grid]
			word_grid: dictionary containing the "identity of each word"
		"""
		clue = ""
		clue_num = 1

		team_words, opp_words, civ_words, boom_word = self.interpretGameboard(word_grid)

		#Find words most relevant to each other
		self.sim_matrix
		team_indexs = [self.codeword_to_idx.get(x) for x in team_words]
		opp_indexs = [self.codeword_to_idx.get(x) for x in opp_words]
		civ_indexs = [self.codeword_to_idx.get(x) for x in civ_words]
		boom_index = [self.codeword_to_idx.get(x) for x in boom_word]

		top_team_idxs = []
		top_opp_idxs = []
		top_civ_idxs = []
		top_boom_idxs = self.codeword_to_idx[boom_index].argsort()[::-1][:]

		ind_max = max(len(team_indexs),len(opp_indexs),len(civ_indexs),len(boom_index))
		
		for i in ind_max:
			if i < len(team_indexs):
				idx = team_indexs[i]
				top_team_idxs.append(self.codeword_to_idx[idx].argsort()[::-1][:])
			if i < len(opp_indexs):
				idx = opp_indexs[i]
				top_opp_idxs.append(self.codeword_to_idx[idx].argsort()[::-1][:])
			if i < len(civ_indexs):
				idx = civ_indexs[i]
				top_civ_idxs.append(self.codeword_to_idx[idx].argsort()[::-1][:])

		#Rocchio away the synonyms of the opp_words, civ_words, and boom_word
		
		return clue, clue_num


class spyAgent(spyPlayer):
	def __init__(self, team_num):
		spyPlayer.__init__(self,team_num)
		#Make a mapping of possible words to Codename words
		self.sim_matrix = np.transpose(self.sim_matrix) #TODO Check if this is the correct way to reference

	def getNonGuessed(self,word_list, guessed):
		"""Returns a list of the words that have not been guessed yet"""
		not_guessed = []
		for i in range(0,len(guessed)):
			if guessed[i]==0: not_guessed.append(word_list[i])
		
		return not_guessed

	def computeRocchio(word):
		rel_words = self.rel_pool.get(word,[])
		irrel_words = self.irrel_pool.get(word,[])
		# mod_vec = np.empty([17000]) #TODO Replace
		# alpha_term = np.empty([17000]) #TODO Replace
		# beta_term = np.empty([17000]) #TODO Replace
		# gamma_term = np.empty([17000]) #TODO Replace
		
		#Get sim vector for word, mult. by alpha term
		# sim_vector = np.empty([17000]) #TODO Replace
		sim_idx = self.bankword_to_idx.get(word)
		sim_vector = self.sim_matrix[sim_idx]
		alpha_term = ALPHA_ROCC*sim_vector

		#For each relevant word
		for rel_word in rel_words:
			#Get sim vector of rel_word
			rel_idx = self.bankword_to_idx.get(rel_word)
			rel_vector = self.sim_matrix[rel_idx]
			beta_term+=rel_vector
		b_frac = BETA_ROCC/len(rel_words)
		beta_term = b_frac*beta_term

		#For each irrelevant word
		for irrel_word in irrel_words:
			#Get sim vector of irrel_word
			irrel_idx = self.bankword_to_idx.get(irrel_word)
			irrel_vector = self.sim_matrix[irrel_idx]
			gamma_term+=irrel_vector
		c_frac = GAMMA_ROCC/len(irrel_words)
		gamma_term = c_frac*gamma_term

		#Calculate updated query
		mod_vec = alpha_term + beta_term - gamma_term

		#Lowest value allowed is 0
		for i in range(0,mod_vec.size):
			mod_vec[i] = max(0,mod_vec[i])

		return mod_vec

	# NOTE: returns a LIST of guesses, must be iterated through in order to process in main game
	def makeGuesses(self,word_list, guessed,clue,num_words):
		guesses = []

		# USE INSTEAD OF WORD_LIST
		word_choices = self.getNonGuessed(word_list, guessed)

		# print(self.sim_matrix)

		# Get sim vector for the clue
		clue_idx = self.bankword_to_idx.get(clue)
		# print(clue_idx)
		clue_vec = self.sim_matrix[clue_idx]

		# Rocchio with sim vectors for synonyms and antonyms of the clue
		mod_clue_vec = computeRocchio(clue) #clue_vec # TODO Rocchio

		# print("Mod vector")
		# print(mod_clue_vec)

		# Get argsort of resulting vector as ranking
		ranking = np.argsort(mod_clue_vec)
		#Change from ascending to descending order
		ranking = np.flip(ranking,0)
		# print("Ranking")
		# print(ranking)

		counter = 0
		while len(guesses)<num_words:
			code_check = ranking[counter]
			# print(code_check)
			codeword = self.idx_to_codeword[code_check] 
			if word_choices.count(codeword) ==1: guesses.append(codeword)
			counter+=1

		# While len(guesses) < num_words
			#Iterate through ranking via counter
			#if idx_to_codeword[counter] is in word_list
				#Append result to guesses

		return guesses



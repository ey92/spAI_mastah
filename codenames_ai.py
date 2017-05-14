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
NUM_SIM_PICKLES = 12
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
		self.idx_to_bankword = self.generateBankWordMap()			# dict {key = idx, value = "word"}
		self.bankword_to_idx = self.generateInvertedBankWord() 		# dict {"key = word", value = idx}
		self.idx_to_codeword = self.generateCodeWordMap()
		self.codeword_to_idx = self.generateInvertedCodeWord()		# dict {"key = word", value = idx}

	def generateSimMatrix(self):
		"""Returns a numpy array mapping Codename words to other possible words"""
		sim_mat = np.empty([400,6459])
		for x in range(0,NUM_SIM_PICKLES):
			with open(SIM_PICKLE_HEAD+str(1)+".pickle",'rb') as f:
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

	def addIrrelevantEntry(self,word,irrel_entry):
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

		# print(type(word_grid))

		for word in word_grid.keys():
			word_id = word_grid.get(word)
			mod_word = word.lower()
			if word_id == self.team_num: team_words.append(mod_word)
			elif word_id == opp_num: opp_words.append(mod_word)
			elif word_id == civ_num: civ_words.append(mod_word)
			elif word_id == boom_num: boom_word = mod_word
			else: print("Why is there a "+str(word_id)+" in the processing?!?!?")

		return team_words, opp_words, civ_words, boom_word

	def createClue(self,word_list, word_grid):
		"""Creates a clue based off the state of the gameboard [word_grid]
		word_grid: dictionary containing the "identity of each word"""
		n = 200   # num similar words you care about
		clue = ""
		clue_num = 0

		team_words, opp_words, civ_words, boom_word = self.interpretGameboard(word_grid)

		#Find words most relevant to each other
		team_indexs = [self.codeword_to_idx.get(x) for x in team_words]
		opp_indexs = [self.codeword_to_idx.get(x) for x in opp_words]
		civ_indexs = [self.codeword_to_idx.get(x) for x in civ_words]
		boom_index = [self.codeword_to_idx.get(x) for x in boom_word]
		
#         print('team_indexs')
#         print(team_indexs)

		top_team_idxs = []
		top_opp_idxs = []
		top_civ_idxs = []
		sorted = self.sim_matrix[boom_index].argsort()[::-1][:]
		top_boom_idxs = sorted[:10]

		# ind_max = max(len(team_indexs),len(opp_indexs),len(civ_indexs),len(boom_index))
	
		# get top 5 similarity
		for i in range(9):
			if i < len(team_indexs):
				idx = team_indexs[i]
				sorted = self.sim_matrix[idx].argsort()[::-1][:]
				top_team_idxs.append(sorted[:n])
			if i < len(opp_indexs):
				idx = opp_indexs[i]
				sorted = self.sim_matrix[idx].argsort()[::-1][:]
				top_opp_idxs.append(sorted[:n])
			if i < len(civ_indexs):
				idx = civ_indexs[i]
				sorted = self.sim_matrix[idx].argsort()[::-1][:]
				top_civ_idxs.append(sorted[:n])

		counts = np.zeros([n,n])
#         team_similar = []
		
#         for i in range(8):
#             print(top_team_idxs[i])
#             team_similar.append([self.idx_to_bankword[x] for x in top_team_idxs[i]])
#             print(team_similar[i])
		
		# print("team")
		# print(team_words)
		# print("opp")
		# print(opp_words)
		# print("civ")
		# print(civ_words)
		# print("boom")
		# print(boom_word)

		for i in range(len(top_team_idxs)):
			if i < len(top_team_idxs):
				for j in range(n):
					if j < len(top_team_idxs[0]):
						try:
							top_team_idxs[i][j]
						
							for k in range(len(top_team_idxs)):
								if k < len(top_team_idxs):
									if top_team_idxs[i][j] in top_team_idxs[k]:
										counts[i][j]+=1
								if k < len(top_opp_idxs):
									if top_team_idxs[i][j] in top_opp_idxs[k]:
										counts[i][j]-=0.8
								if k < len(top_civ_idxs):
									if top_team_idxs[i][j] in top_civ_idxs[k]:
										 counts[i][j]-=0.3
						except:
							print(i,j,k)
							# print(top_team_idxs[i])
#                             print(top_team_idxs[k])
		# top indices for each word in team words
		cts_idx = [np.argmax(z) for z in counts]
		top_cts = [counts[i][cts_idx[i]] for i in range(len(cts_idx))]
		i = np.argmax(top_cts)
		j = cts_idx[i]

		ii = [team_indexs[i]][0]
		jj = [top_team_idxs[i][j]][0]

#         print(counts[i][j])
		clue = self.idx_to_bankword[jj]
		clue_num = np.floor(counts[i][j])
		
#         for i in range(n):
#             print(counts[i])

		#Rocchio away the synonyms of the opp_words, civ_words, and boom_word

		return clue, clue_num


class spyAgent(spyPlayer):
	def __init__(self, team_num):
		spyPlayer.__init__(self,team_num)
		#Make a mapping of possible words to Codename words
		self.sim_matrix = np.transpose(self.sim_matrix) 

	def getNonGuessed(self,word_list, guessed):
		"""Returns a list of the words that have not been guessed yet"""
		not_guessed = []
		for i in range(0,len(word_list)):
			if guessed[i]==0: not_guessed.append(word_list[i])
		
		return not_guessed

	# def computeRocchio(self,word_vec):
	def computeRocchio(self, word):
		rel_words = self.rel_pool.get(word,[])
		irrel_words = self.irrel_pool.get(word,[])
		
		#Get sim vector for word, mult. by alpha term
		sim_idx = self.bankword_to_idx.get(word)
		sim_vector = self.sim_matrix[sim_idx]
		sim_size = np.shape(sim_vector)
		
		#Define accumulators
		alpha_term = np.empty([sim_size[0],])
		beta_term = np.empty([sim_size[0],])
		gamma_term = np.empty([sim_size[0],])
		
		alpha_term = ALPHA_ROCC*sim_vector

		#For each relevant word
		for rel_word in rel_words:
			#Get sim vector of rel_word
			print(rel_word)
			rel_idx = self.bankword_to_idx.get(rel_word)
			print(str(rel_idx))
			rel_vector = self.sim_matrix[rel_idx]
			beta_term+=rel_vector		
		#Account for divide by zero
		b_frac = 0
		if len(rel_words)>0: b_frac = BETA_ROCC/len(rel_words)
		beta_term = b_frac*beta_term

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

		#Calculate updated query
		mod_vec = alpha_term + beta_term - gamma_term

		#Lowest value allowed is 0
		for i in range(0,mod_vec.size):
			mod_vec[i] = max(0,mod_vec[i])

		return mod_vec

	# NOTE: returns a LIST of guesses, must be iterated through in order to process in main game
	def makeGuesses(self, word_list, guessed, clue, num_words):
		guesses = []

		# USE INSTEAD OF WORD_LIST
		word_choices = self.getNonGuessed(word_list, guessed)

		# Get sim vector for the clue
		clue_idx = self.bankword_to_idx.get(clue)
		clue_vec = self.sim_matrix[clue_idx]

		print("Clue for guessing is: "+clue)
		# print(np.shape(ranking))

		# Rocchio with sim vectors for synonyms and antonyms of the clue
		query = clue.lower()		
		mod_clue_vec = self.computeRocchio(query)

		# Get argsort of resulting vector as ranking in descending order
		ranking = np.argsort(mod_clue_vec)
		# Change from ascending to descending order
		ranking = np.flip(ranking,0)		

		#Get most similar words in word_grid
		counter = 0

		#Only get the number of words guessed
		while len(guesses) < 1:
			word_idx = ranking[counter]
			codeword = self.idx_to_codeword[word_idx] 
			codeword = codeword.capitalize()
			#Only append the most similar word if it's on the board
			if word_choices.count(codeword) ==1: guesses.append(codeword)
			counter+=1

		return guesses[0]
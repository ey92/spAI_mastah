import numpy as np
import cPickle as pickle

RELEVANT_PICKLE = "relevant.pickle"
IRRELEVANT_PICKLE = "irrelevant.pickle"

relevant = {}
irrelevant = {}

ALPHA_ROCC = 0.3
BETA_ROCC = 0.3
GAMMA_ROCC = 0.8

def loadRocchio():
	with open(RELEVANT_PICKLE,"rb") as r_file:
		relevant = pickle.load(r_file)

	with open(IRRELEVANT_PICKLE,"rb") as ir_file:
		irrelevant = pickle.load(ir_file)


def saveRocchio():
	with open(RELEVANT_PICKLE,"wb") as r_file:
		pickle.dump(relevant, r_file)

	with open(IRRELEVANT_PICKLE,"wb") as ir_file:
		pickle.dump(irrelevant, ir_file)

def getRelevantEntry(word):
	return relevant.get(word,[])

def getIrrelevantEntry(word):
	return irrelevant.get(word,[])


def addRelevantEntry(word,rel_entry):
	temp = getRelevantEntry(word)
	temp.append(rel_entry)
	relevant.update({word:temp})

def addIrelevantEntry(word,irrel_entry):
	temp = getIrrelevantEntry(word)
	temp.append(irrel_entry)
	irrelevant.update({word:temp})


def computeRocchio(word):
	rel_words = relevant.get(word,[])
	irrel_words = irrelevant.get(word,[])
	mod_vec = np.empty([17000]) #TODO Replace
	alpha_term = np.empty([17000]) #TODO Replace
	beta_term = np.empty([17000]) #TODO Replace
	gamma_term = np.empty([17000]) #TODO Replace
	
	#Get sim vector for word, mult. by alpha term
	sim_vector = np.empty([17000]) #TODO Replace
	alpha_term = ALPHA_ROCC*sim_vector

	#For each relevant word
	for rel_word in rel_words:
		#Get sim vector of rel_word
		rel_vector = np.empty([17000]) #TODO Replace
		beta_term+=rel_vector
	b_frac = BETA_ROCC/len(rel_words)
	beta_term = b_frac*beta_term

	#For each irrelevant word
	for irrel_word in irrel_words:
		#Get sim vector of irrel_word
		irrel_vector = np.empty([17000]) #TODO Replace
		gamma_term+=irrel_vector
	c_frac = GAMMA_ROCC/len(irrel_words)
	gamma_term = c_frac*gamma_term

	#Calculate updated query
	mod_vec = alpha_term + beta_term - gamma_term

	#Lowest value allowed is 0
	for i in range(0,mod_vec.size):
		mod_vec[i] = max(0,mod_vec[i])

	return mod_vec

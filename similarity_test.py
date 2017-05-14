from nltk.corpus import wordnet as wn
import cPickle as pickle
import numpy as np

CODENAMES_WORDLIST = "words_to_process.txt"
relevant = {}
irrelevant = {}

# Dictionary for relevant & irrelevant terms for Rocchio
# When choosing an answer, should access Rocchio structures for both terms and append to both structures
# 

# Only allowed to give one word guesses, so only concerned with one-word entries
all_lemmas = [i for i in wn.all_lemma_names() if i.count("_")==0 and i.isalpha()]
all_lemmas = sorted(all_lemmas)
#all_lemmas is the indexing order for the corress. similarity matrix
num_lemmas = len(all_lemmas)

# Get Codenames words
file = open(CODENAMES_WORDLIST, "r")
words = file.read()
word_list = words.split("\n") #Contains an array of the words from Codenames
num_words = len(word_list)

similarity_matrix = np.empty([num_words,num_lemmas])

#Collect EVERYTHING
for i in range(0,num_words):
	#Compute similarity
	#Get synonyms for relevant
	#Get antonyms for irrelevant

	for j in range(0,num_lemmas):

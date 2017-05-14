
# coding: utf-8

# In[1]:

from nltk.corpus import wordnet as wn
import pickle
import numpy as np

CODENAMES_WORDLIST = "words_to_process.txt"
# relevant = {}
# irrelevant = {}

MATRIX_NUM = 0

# In[2]:

# Only allowed to give one word guesses, so only concerned with one-word entries
all_lemmas = [i for i in wn.all_lemma_names() if i.count("_")==0 and i.isalpha()]
all_lemmas = sorted(all_lemmas)
#all_lemmas is the indexing order for the corress. similarity matrix
num_lemmas = len(all_lemmas)


# # In[3]:

file = open(CODENAMES_WORDLIST, "r")
words = file.read()
word_list = words.split("\n") #Contains an array of the words from Codenames
word_list = sorted(word_list)
num_words = len(word_list)
# num_words = 400


# In[5]:

# print(len(all_lemmas))


# In[6]:

# similarity_matrix = np.empty([num_words,num_lemmas])

#Collect EVERYTHING

# Populate relevant and irrelevant dictionaries
#The following is taken from: 
# < https://pythonprogramming.net/wordnet-nltk-tutorial/ >
# for word in word_list:
#     synonyms = set() #Convert to arrays later
#     antonyms = set() #Convert to arrays later
#     for syn_list in wn.synsets(word):
#         for lemma in syn_list.lemmas():
# #             print(lemma)
#             #Get synonyms for relevant
#             synonym = lemma.name()
#             if synonym.count("_")==0 and not synonym==word : synonyms.add(synonym)
#             #Get antonyms for irrelevant
#             for ant in lemma.antonyms():
#                 antonym = ant.name()
#                 if antonym.count("_")==0: antonyms.add(antonym)
# #             if lemma.antonyms():
# #                 print(lemma.antonyms())
#                 #antonyms.add(lemma.antonyms()[0].name())
#     relevant.update({word:list(synonyms)})
#     irrelevant.update({word:list(antonyms)})

# # print(relevant)
# # print(irrelevant)



# # In[7]:

# with open('relevant_rocchio.pickle', 'wb') as f:
#     pickle.dump(relevant, f)

# with open('irrelevant_rocchio.pickle', 'wb') as f:
#     pickle.dump(irrelevant, f)


# In[8]:

# Just takes the highest similarity score, maybe something fancier later
def getSimilarityScore(word1,word2):
    synset1 = wn.synsets(word1)
    synset2 = wn.synsets(word2)
    accumulator = 0.0
    for i in synset1:
        for j in synset2:
            score = i.wup_similarity(j)
#             print(score)
            if score==None: score=0
            if accumulator<score: accumulator = score
                
#     print("Returned"+str(accumulator))
#     print()
    return accumulator

#Populate similarity matrix
# for i in range(0,num_words):
#     #Compute similarity
# #     similarity = 0.0
#     for j in range(0,num_lemmas):
# #     for j in range(0,10):
# #         synset1 = wn.synsets(words_list[i])
# #         synset2 = wn.synsets(all_lemmas[j])
#         sim_score = getSimilarityScore(word_list[i],all_lemmas[j])
#         similarity_matrix[i,j] = sim_score


# In[49]:

# print(similarity_matrix)
# print(similarity_matrix.shape)

# test = wn.synsets("program")
# test2 = wn.synsets("test")

# # test3 = wn.synset("ship.n.01")
# # print(test3)

# # print(test)
# # print(test2)

# for i in test:
#     for j in test2:
#         print(i.wup_similarity(j))
#     print()


# In[9]:

#77503 words total

sim_matrix1 = np.empty([num_words,6459])
sim_matrix2 = np.empty([num_words,6459])
sim_matrix3 = np.empty([num_words,6459])
sim_matrix4 = np.empty([num_words,6459])
sim_matrix5 = np.empty([num_words,6459])
sim_matrix6 = np.empty([num_words,6459])
sim_matrix7 = np.empty([num_words,6459])
sim_matrix8 = np.empty([num_words,6459])
sim_matrix9 = np.empty([num_words,6459])
sim_matrix10 = np.empty([num_words,6459])
sim_matrix11 = np.empty([num_words,6459])
sim_matrix12 = np.empty([num_words,6454])

def popMatrix(sim_matrix,lemma_set):
    for i in range(0,num_words):
        #Compute similarity
        # print("CODENAMES WORD: "+str(i))
        for j in range(0,len(lemma_set)):
            print("MATRIX NUMBER: "+str(MATRIX_NUM)+", CODENAMES WORD: "+str(i)+", BANK WORD: "+str(j))
            sim_score = getSimilarityScore(word_list[i],lemma_set[j])
            sim_matrix[i,j] = sim_score



# # In[ ]:

# with open('sim_matrix1.pickle', 'wb') as f:
#     popMatrix(sim_matrix1,all_lemmas[:6459])
#     pickle.dump(sim_matrix1, f)


# # In[ ]:

# with open('sim_matrix2.pickle', 'wb') as f:
#     popMatrix(sim_matrix2,all_lemmas[6459+1:12918])
#     pickle.dump(sim_matrix2, f)


# # In[ ]:

# with open('sim_matrix3.pickle', 'wb') as f:
#     popMatrix(sim_matrix3,all_lemmas[12918+1:19377])
#     pickle.dump(sim_matrix3, f)


# # In[ ]:

# with open('sim_matrix4.pickle', 'wb') as f:
#     popMatrix(sim_matrix4,all_lemmas[19377+1:25836])
#     pickle.dump(sim_matrix4, f)


# # In[ ]:

# with open('sim_matrix5.pickle', 'wb') as f:
#     popMatrix(sim_matrix5,all_lemmas[25836+1:32295])
#     pickle.dump(sim_matrix5, f)


# # In[ ]:

# with open('sim_matrix6.pickle', 'wb') as f:
#     popMatrix(sim_matrix6,all_lemmas[32295+1:38754])
#     pickle.dump(sim_matrix6, f)


# # In[ ]:

# with open('sim_matrix7.pickle', 'wb') as f:
#     popMatrix(sim_matrix7,all_lemmas[38754+1:45213])
#     pickle.dump(sim_matrix7, f)


# # In[ ]:

# with open('sim_matrix8.pickle', 'wb') as f:
#     popMatrix(sim_matrix8,all_lemmas[45213+1:51672])
#     pickle.dump(sim_matrix8, f)


# # In[ ]:

# with open('sim_matrix9.pickle', 'wb') as f:
#     popMatrix(sim_matrix9,all_lemmas[51672+1:58131])
#     pickle.dump(sim_matrix9, f)


# # In[ ]:

# with open('sim_matrix10.pickle', 'wb') as f:
#     popMatrix(sim_matrix10,all_lemmas[58131+1:64590])
#     pickle.dump(sim_matrix10, f)


# # In[ ]:

# with open('sim_matrix11.pickle', 'wb') as f:
#     popMatrix(sim_matrix11,all_lemmas[64590+1:71049])
#     pickle.dump(sim_matrix11, f)


# # In[ ]:

# with open('sim_matrix12.pickle', 'wb') as f:
#     popMatrix(sim_matrix12,all_lemmas[71049+1:])
#     pickle.dump(sim_matrix12, f)


# In[ ]:

#glove.6B.50d.txt
# file = open("glove.6B.50d.txt", "r")
# new_words = file.read()
# new_word_list = words.split("\n") #Contains an array of the words from Codenames
# new_word_list = sorted(word_list)
# new_num_words = len(word_list)


# In[ ]:


if __name__=="__main__":
    # with open('test2.pickle', 'wb') as f:
    #     print("This is a test")
    #     popMatrix(sim_matrix1,all_lemmas[:10])
    #     pickle.dump(sim_matrix1, f)
    
    # In[ ]:
    with open('sim_matrix1.pickle', 'wb') as f:
        MATRIX_NUM = 1
        print("This is sim_matrix1")
        popMatrix(sim_matrix1,all_lemmas[:6459])
        pickle.dump(sim_matrix1, f)

    # In[ ]:
    with open('sim_matrix2.pickle', 'wb') as f:
        MATRIX_NUM = 2
        print("This is sim_matrix2")
        popMatrix(sim_matrix2,all_lemmas[6459+1:12918])
        pickle.dump(sim_matrix2, f)

    # In[ ]:
    with open('sim_matrix3.pickle', 'wb') as f:
        MATRIX_NUM = 3
        print("This is sim_matrix3")
        popMatrix(sim_matrix3,all_lemmas[12918+1:19377])
        pickle.dump(sim_matrix3, f)

    # In[ ]:
    with open('sim_matrix4.pickle', 'wb') as f:
        MATRIX_NUM = 4
        print("This is sim_matrix4")
        popMatrix(sim_matrix4,all_lemmas[19377+1:25836])
        pickle.dump(sim_matrix4, f)

    # In[ ]:
    with open('sim_matrix5.pickle', 'wb') as f:
        MATRIX_NUM = 5
        print("This is sim_matrix5")
        popMatrix(sim_matrix5,all_lemmas[25836+1:32295])
        pickle.dump(sim_matrix5, f)

    # In[ ]:
    with open('sim_matrix6.pickle', 'wb') as f:
        MATRIX_NUM = 6
        print("This is sim_matrix6")
        popMatrix(sim_matrix6,all_lemmas[32295+1:38754])
        pickle.dump(sim_matrix6, f)

    # In[ ]:
    with open('sim_matrix7.pickle', 'wb') as f:
        MATRIX_NUM = 7
        print("This is sim_matrix7")
        popMatrix(sim_matrix7,all_lemmas[38754+1:45213])
        pickle.dump(sim_matrix7, f)

    # In[ ]:
    with open('sim_matrix8.pickle', 'wb') as f:
        MATRIX_NUM = 8
        print("This is sim_matrix8")
        popMatrix(sim_matrix8,all_lemmas[45213+1:51672])
        pickle.dump(sim_matrix8, f)

    # In[ ]:
    with open('sim_matrix9.pickle', 'wb') as f:
        MATRIX_NUM = 9
        print("This is sim_matrix9")
        popMatrix(sim_matrix9,all_lemmas[51672+1:58131])
        pickle.dump(sim_matrix9, f)

    # In[ ]:
    with open('sim_matrix10.pickle', 'wb') as f:
        MATRIX_NUM = 10
        print("This is sim_matrix10")
        popMatrix(sim_matrix10,all_lemmas[58131+1:64590])
        pickle.dump(sim_matrix10, f)

    # In[ ]:
    with open('sim_matrix11.pickle', 'wb') as f:
        MATRIX_NUM = 11
        print("This is sim_matrix11")
        popMatrix(sim_matrix11,all_lemmas[64590+1:71049])
        pickle.dump(sim_matrix11, f)

    # In[ ]:
    with open('sim_matrix12.pickle', 'wb') as f:
        MATRIX_NUM = 12
        print("This is sim_matrix12")
        popMatrix(sim_matrix12,all_lemmas[71049+1:])
        pickle.dump(sim_matrix12, f)

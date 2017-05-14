def getHumanPrompt():
    clue = ""
    clue_num = 0
    
    clue_done = false
    num_done = false
    
    while not clue_done:
        if py3:
            clue = input("What prompt would you like to give?\n")
        else:
            clue = raw_input("What prompt would you like to give?\n")
        clue = clue.strip().lower()
        
        temp = clue
        # temp = temp.capitalize()
        dict_check = True
        if current_team==BLUE_TEAM and not blue_spy_human: 
            temp = temp.lower()
            exists = blue_ai_agent.bankword_to_idx.get(temp)
            if exists==None: dict_check= False
        elif current_team==RED_TEAM and not red_spy_human:
            temp = temp.lower()
            exists = red_ai_agent.bankword_to_idx.get(temp)
            if exists==None: dict_check= False
                    
        clue.capitalize()

        if word_list.count(clue)==1 and guessed[word_list.index(clue)]==0:
            print("Hey, \""+response+"\"  is on the board already! You can't use that as a clue! Try a different one.")
        elif clue.count(" ") > 0:
            print("You can only provide one word as a clue! Try a different one.")
        elif not clue.isalpha():
            print("Hey now, you can't put non-alphabet characters in your clue! Try a different one.")
        elif not dict_check:
            print("\""+temp+"\" doesn't exist in the agents' vocabulary! Can you try a different one instead?")
        else:
            clue_done = true
            
    while not num_done:
        if py3:
            clue_num = input("Spy Master, how many guesses should your agents make?\n")
        else:
            clue_num = raw_input("Spy Master, how many guesses should your agents make?\n")
        clue_num = clue_num.strip()

        if not clue_num.isdigit():
            print("Hey, this isn't a number! Try again!")
        else:
            num_done = true
            clue_num = int(clue_num)
            
    return clue, clue_num

# Gets a prompt/clue from the spymaster, human or AI
def getPrompt():
    # Need to check current team
    #If human is the spy master and if it's their tur
    global blue_ai_master
    global red_ai_master
    
    clue = ""
    clue_num = 0
    
    if current_team == BLUE_TEAM:
        print("[Current Team: Blue Team]")

        # blue spy master stuff
        print("It is Blue Spy Master's Turn")

        if not blue_master_human:
            return blue_ai_master.createClue(word_list,word_grid)
        else:
            return getHumanPrompt()
    else:
        print("[Current Team: Blue Team]")
        
        # red spy master stuff
        print("It is Red Spy Master's Turn")
        if not red_master_human:
            return red_ai_master.createClue(word_list,word_grid)
        else:
            return getHumanPrompt()

    return clue, clue_num

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
                            num = top_team_idxs[i][j]
                        except:
                            num = top_team_idxs[0][i][j]

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
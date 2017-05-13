### Created 04/17/2017 by Lauren Hsu and Elizabeth Yam
import numpy as np 
import rocchio as ro

SIM_PICKLE_HEAD = "sim_matrix"
RELEVANT_PICKLE = "relevant.pickle"
IRRELEVANT_PICKLE = "irrelevant.pickle"

class spyPlayer():
	def __init__(self):
        # self.frequency = frequency
        # Sound.__init__(self, buffer=self.build_samples())
        # self.set_volume(volume) 
        self.sim_matrix = generateSimMatrix()
        self.rel_pool = generateRelRocchio()
        self.irrel_pool = generateIrrelRocchio()

    def generateSimMatrix():
    	pass

    def generateRelRocchio():
    	pass

    def generateIrrelRocchio():
    	pass

class spyMaster(spyPlayer):

    def createClue():
    	pass


class spyAgent(spyPlayer):

    def makeGuess():
    	pass



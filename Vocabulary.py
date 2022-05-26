"""_summary_
    Vocab handler
"""
import random
class TestVocabulary:
    # look into context managers/reading from .txt
    def __init__(self, vocab_path=None):
        # these should be in txt files
        self.vocab_0 = ['rainbow', 'fish','england','america','fire','missle']
        self.vocab_1 = ['rainbow', 'fish','england','america','fire','missle',
                            'truck','car', 'frog', 'russia', 'war', 'mole','spy',
                            'victory','book','note','choir','movie','fox','zoo',
                            'carrot','potato','giraffe','guitar','piano','door',
                            'stone','pit','arm','dreadful','hook','pirate','young',
                            'attic','arctic','roman','greek','pyramid','gladiator',
                            'punch','chew','gold','wrench','hammer','silver','iron',
                            'bear','eagle','shirt','ship','dragon','island','pen',
                            'pencil','sketch','paper','tree','wax','moon','sun','wolf',
                            'ice','ocean','mountain','hill','desert','ice cream','fountain',
                            'crash','cup','pin','mass','train','hollywood','horse','dog',
                            'play','note','key']
        
        random.shuffle(self.vocab_1)
    
    def choose_random(self):
        return self.vocab_1.pop()
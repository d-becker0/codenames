"""_summary_
player classes for human and ai players
"""
from nltk.corpus import wordnet as wn
from abc import abstractmethod
import random
from Board import Board

def get_meronyms(wordnet_word):
    return wordnet_word.part_meronyms()
def get_holonyms(wordnet_word):
    return wordnet_word.part_holonyms()
def get_hyponyms(wordnet_word):
    return wordnet_word.hyponyms()
def get_hypernyms(wordnet_word):
    return wordnet_word.hypernyms()  
def get_entailments(wordnet_word):
    return wordnet_word.entailments()

def search_wordnet(wordnet_word):
    meronyms = get_meronyms(wordnet_word)
    holonyms = get_holonyms(wordnet_word)
    hypernyms = get_hypernyms(wordnet_word)
    hyponyms = get_hyponyms(wordnet_word)
    entailments = get_entailments(wordnet_word)  
    return {
            'meronyms': meronyms,
            'holonyms':holonyms,
            'hypernyms':hypernyms,
            'hyponyms':hyponyms,
            'entailments':entailments
            }

# icky and doesn't always work
# good enough for quickly testing a gui at least
def find_single_clue(start_word):
    connections = search_wordnet(wn.synsets(start_word)[0])
    
    if not connections:
        return (False,0)
    
    for relation, connection in connections.items():
        for word in connection:
            if start_word not in word.lemma_names():
                lemmas=word.lemma_names()
                if lemmas:
                    return (word.lemma_names()[0],1) # (clue word, 1 word associated on board)
                
    return (False,0)

class NonHumanPlayer:
    def __init__(self,team,search_depth=1):
        self.team = team
        self.codes = {}
        self.search_depth = search_depth
    
    # @abstractmethod
    # def give_code(self):
    #     pass
    
    # @abstractmethod
    # def guess_word(self, code):
    #     pass

class WordnetPlayer(NonHumanPlayer):
    def __init__(self, team,search_depth=1,search=find_single_clue):#,select=select_max_matched):
        self.words_in_play = []
        self.word_team_lookup = {}
        self.team = team
        self.codes = {}
        self.search_depth = search_depth
        self.search=search
        #self.select=select
    
    def give_code(self):
        word = self.get_team_word()
        #possible_codes_and_words = self.search(word)
        code, num_associated = self.search(word)#possible_codes_and_words)
        self.codes[word] = code
        # num_associated = len(associated_words)
        return (code, num_associated) # yield with a tuple might give 1 value at a time... check this
        
    def update(self, board):
        self.words_in_play = board.words_in_play
        self.word_team_lookup = board.word_team_lookup
        
    def check_intersections_wordlists(self, wl1, wl2):
        intersections = set(wl1).intersection(set(wl2))
        if intersections:
            return intersections 
        else:
            return False
        
    def get_team_word(self):
        for word in self.words_in_play:
            if self.word_team_lookup[word] == self.team and word not in self.codes:
                return word
        
class HumanPlayer:
    def __init__(self, team):
        self.team = team
        
    def make_guess(self):
        guess = input('What is your guess?')
        return guess
      
    def give_code(self):
        code = input('What is your clue?')
        num_words = input('How many words on the board is it associated with?')
        return code, num_words
    
    def get_team(self):
        return self.team
    
    def update(self, board):
        pass
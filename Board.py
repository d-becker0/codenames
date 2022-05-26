"""_summary_
    A class method to handle the board and board states
"""
import random
from keywords import *

class Board:
    def __init__(self, x_size, y_size, team_counts):
        self.x_size = x_size
        self.y_size = y_size
        
        self.words_on_board = []
        self.words_in_play = []
        self.word_lookup = {} # specify location on board lookup in refactor
        self.word_team_lookup = {}
        self.team_counts = team_counts
        
        self.subscribers = []
        
        # TODO: there is better way to do this
        self.teams_to_pop = []
        for team, count in team_counts.items():
            self.teams_to_pop.extend([team for i in range(count)])
            
        random.shuffle(self.teams_to_pop)
        
    # observer pattern
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)
    def notify_subscribers(self):
        for subscriber in self.subscribers:
            subscriber.update(self)
            
    def make_board(self, vocabulary):
        for i in range(self.y_size):
            row = []
            for ii in range(self.x_size):
                
                word = vocabulary.choose_random()
                team = self.get_random_team()
                
                row.append({WORD_KEY:word, TEAM_KEY: team, REVEALED_KEY:False})
                self.word_team_lookup[word] = team
                self.words_in_play.append(word)
                self.word_lookup[word] = (i,ii)
            self.words_on_board.append(row)
            
    def get_random_team(self):
        return self.teams_to_pop.pop()
    
    def handle_valid_word_selection(self, guess):
        self.remove_guess_from_in_play(guess)
        self.update_revealed(guess)
        
    def remove_guess_from_in_play(self, guess):
        self.words_in_play.remove(guess)
        
    def update_revealed(self, guess):
        i,j = self.word_lookup[guess]
        self.words_on_board[i][j][REVEALED_KEY]=True
            
    def is_guess_in_play(self,guess):
        if guess in self.words_in_play:
            return True
        return False 
        
    def get_word_team(self, word):
        i, j = self.word_lookup[word]
        return self.words_on_board[i][j][TEAM_KEY]
    
    def get_position_team(self, i, j):
        return self.words_on_board[i][j][TEAM_KEY]
    
    def get_team_counts(self):
        return self.team_counts
    
    def get_words_on_board(self):
        return self.words_on_board
    
    def update_team_counts(self, team):
        self.team_counts[team] = self.team_counts[team]-1
        
    def yield_all_word_cards(self):
        for i,row in enumerate(self.words_on_board):
            for j, word_info in enumerate(row):
                yield (i,j, word_info)
    

    
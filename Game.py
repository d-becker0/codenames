""" Game class which defines game loop board drawing and game logic, while allowing for inheritance and hopefully future flexibility
    TODO: find out if this is too much of a "god class", i guess I feel like the inheritance might be nice, but theres def others ways to organize
    I gues I kinda like my other classes only interacting through a main method/class, but maybe thats bad in a growing project (my rough understanding of microservices
    would say not to do this) probably doesn't matter for a small project like this either way though...
"""

import pygame
from pygame.locals import * # fix me
from abc import abstractmethod

UNREVEALED_COLOR = (150,150,150)
INNOCENT_COLOR = (220,220,220)
ASSASSIN_COLOR = (10,10,10)
BLUE_COLOR = (60,60,230)
RED_COLOR = (230,60,60)
BACKGROUND_COLOR = (255,255,255)

INNOCENT_IDENTIFIER = 'innocent'
ASSASSIN_IDENTIFIER = 'assassin'
RED_IDENTIFIER = 'red'
BLUE_IDENTIFIER = 'blue'

X_MARGIN = 20
Y_MARGIN = 20
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

CARD_WIDTH = 150
CARD_HEIGHT = 100
CARD_SPACING = 20


class Abstract_Game:

    def __init__(self, board, code_giver, code_guesser, current_team):
        self.board = board
        self.code_giver = code_giver
        self.code_guesser = code_guesser
        self.current_team = current_team
        
        self.board.subscribe(self.code_giver)
        self.board.subscribe(self.code_guesser)
        
        self.turn = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        #self.screen.set_caption('Codenames')
    
    def draw_board(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        for i,j, word_card in self.board.yield_all_word_cards():
            card_color = self.find_card_color(word_card)
            x,y = self.find_left_top_coords_from_position(i,j)
            pygame.draw.rect(self.screen, card_color, (x,y, CARD_WIDTH, CARD_HEIGHT))
            
        pygame.display.update()
    
    def find_card_color(self, word_card):
        card_color = UNREVEALED_COLOR
        if word_card["revealed"]:
            if word_card["team"] == "red":
                card_color = RED_COLOR
            elif word_card["team"] == "blue":
                card_color = BLUE_COLOR
            elif word_card["team"] == "assassin":
                card_color = ASSASSIN_COLOR
            elif word_card["team"] == "innocent":
                card_color = INNOCENT_COLOR
        return card_color
    
    # https://inventwithpython.com/pygame/chapter3.html
    def find_left_top_coords_from_position(self,i,j):
    # Convert board coordinates to pixel coordinates
        left = i * (CARD_WIDTH + CARD_SPACING) + X_MARGIN
        top = j * (CARD_HEIGHT + CARD_SPACING) + Y_MARGIN
        return (left, top)
    
    # https://inventwithpython.com/pygame/chapter3.html
    def get_card_at_coords(self,x,y):
        for i in range(self.board.x_size):
            for j in range(self.board.y_size):
                left, top = self.find_left_top_coords_from_position(i, j)
                rect = pygame.Rect(left, top, CARD_WIDTH, CARD_HEIGHT) # this seems very inefficient
                if rect.collidepoint(x, y):
                    return (i,j)
        return False
    
    
    def wait_for_input(self):
        valid_card_board_pos=False
        while not valid_card_board_pos:
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
            # elif event.type == MOUSEMOTION:
            #     mousex, mousey = event.pos
                if event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    valid_card_board_pos = self.get_card_at_coords(x,y)

        return valid_card_board_pos

        
    def handle_mouse_selection(self):
        pass
    
    def next_turn(self):
        self.turn+=1
        if self.current_team == 'red':
            self.current_team = 'blue'
        else:
            self.current_team = 'red'
    
    def does_turn_continue(self, team):
        if team == self.current_team:
            return True
        else:
            return False
    
    # TODO: make less round-a-bout --- yes, god I hate the way I did this
    def does_game_continue(self):
        for team, count in self.board.team_counts.items():
          if count == 0:
              if team != 'innocent':
                  return False
        return True
    
    @abstractmethod
    def code_giving_section(self):
        pass

    @abstractmethod
    def guessing_section(self):
        pass
    
    def run(self, with_display=True, with_updates=True):
        self.board.notify_subscribers()
        game_in_progress = True
        while(game_in_progress):
            
            self.draw_board()
            code, num_words = self.code_giving_section()
            print(code+ ":",num_words)
            turn_continues = True
            while(turn_continues):
        
                guess = self.guessing_section()
        
                self.board.handle_valid_word_selection(guess)
                team = self.board.get_word_team(guess)
    
                self.board.update_team_counts(team)
                self.board.notify_subscribers()
                
                self.draw_board()
    
                turn_continues = self.does_turn_continue(team)
                game_in_progress = self.does_game_continue()
                
            self.next_turn()
        
        # find winner, record game states? record turns

class Game(Abstract_Game):
    def guessing_section(self):
        guess_i,guess_j = self.wait_for_input()
        guess=self.board.words_on_board[guess_i][guess_j]['word']
        return guess
    
    def code_giving_section(self):
        code, num_words = self.code_giver.give_code()
        return code, num_words
        
        
class HumanInTheLoopGame(Abstract_Game):
    def guessing_section(self):
        guess = self.check_input()
        return guess
    
    def code_giving_section(self):
        code, num_words = self.code_giver.give_code()
        return code, num_words
import pygame
from abc import abstractmethod

from keywords import * # lazy to avoid rewrite

# how do you do this better?
pygame.init()
word_font = pygame.font.SysFont("monospace", 15)

class DisplayController:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        #self.screen.set_caption('Codenames')
        self.buttons=[]
        self.button_to_update=None
        self.board=''
    
    def update(self,board):
        self.board=board
    
    def update_button_color(self,team):
        color = self.get_card_color_from_team(team)
        self.button_to_update.set_color(color)
        self.button_to_update=None
    
    def initialize_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        for i,j, word_card in self.board.yield_all_word_cards():
            color = self.get_card_color(word_card)
            text = word_card[WORD_KEY]
            x,y = self.get_pixel_coords_from_card_pos(i,j)
            button = Button(color,x,y,CARD_HEIGHT,CARD_WIDTH,text,i,j)
            self.buttons.append(button)
            button.draw(self.screen)
        pygame.display.update()
    
    def draw_screen(self):
        self.screen.fill(BACKGROUND_COLOR)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()
        
    def get_card_color(self, word_card):
        card_color = UNREVEALED_COLOR
        if word_card[REVEALED_KEY]:
            card_color = self.get_card_color_from_team(word_card[TEAM_KEY])
        return card_color

    def get_card_color_from_team(self,team):
        if team == RED_TEAM_KEY:
            card_color = RED_COLOR
        elif team == BLUE_TEAM_KEY:
            card_color = BLUE_COLOR
        elif team == ASSASSIN_TEAM_KEY:
            card_color = ASSASSIN_COLOR
        elif team == INNOCENT_TEAM_KEY:
            card_color = INNOCENT_COLOR
        return card_color
    
    def get_pixel_coords_from_card_pos(self,i,j):
        left = i * (CARD_WIDTH + CARD_SPACING) + X_MARGIN
        top = j * (CARD_HEIGHT + CARD_SPACING) + Y_MARGIN
        return (left, top)
        
    def valid_click(self,x,y):
        for button in self.buttons:
            if button.collidepoint(x,y):
                return button
        return False
    
    #way this is coded right now, locks me into only selecting word cards on board
    def wait_for_input(self):
        clicked_button=False
        while not clicked_button:
            for event in pygame.event.get(): # event handling loop
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
            # elif event.type == MOUSEMOTION:
            #     mousex, mousey = event.pos
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    clicked_button=self.valid_click(x,y)
        self.button_to_update=clicked_button
        return clicked_button.ij
    
class Button:
    def __init__(self,color,x,y,width,height,text,i=-1,j=-1):
        self.color=color
        self.height=height
        self.width=width
        self.text=text
        self.x=x
        self.y=y
        if i>=0 and j>=0: # position in relation to board can't be negative
            self.ij=(i,j)
        
        #self.surface=pygame.Rect((x,y),(width,height))#pygame.Surface((width,height))
        self.label=word_font.render(self.text, 1, (255,255,255))
        
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        screen.blit(self.label, (self.x + (self.width/2  - self.label.get_width()/2), 
                                 self.y + (self.height/2 - self.label.get_height()/2)))
    
    def collidepoint(self,x,y):
        # self.x,self.y represents top left of rect
        if self.x<=x<=self.x+self.width and self.y<=y<=self.y+self.height:
            return True
        return False
    
    def on_click(self):
        return self.ij
    
    def set_color(self,color):
        self.color=color
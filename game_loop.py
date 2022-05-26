from Board import Board
from Player import HumanPlayer,WordnetPlayer
from Vocabulary import TestVocabulary
from DisplayController import DisplayController
from keywords import *

x_size = 5
y_size = 5
team_counts = {RED_TEAM_KEY:8,BLUE_TEAM_KEY:8,INNOCENT_TEAM_KEY:8,ASSASSIN_TEAM_KEY:1}
board = Board(x_size, y_size, team_counts)
display = DisplayController()

vocabulary = TestVocabulary()
board.make_board(vocabulary)

code_giver = WordnetPlayer(team = RED_TEAM_KEY)
code_guesser = HumanPlayer(team = RED_TEAM_KEY)
        
board.subscribe(code_giver) 
board.subscribe(code_guesser)
board.subscribe(display)
    
def code_giving_section():
    code, num_words = code_giver.give_code()
    return code, num_words

def next_turn(turn,current_team):
    turn+=1
    if current_team == RED_TEAM_KEY:
        current_team = BLUE_TEAM_KEY
    else:
        current_team = RED_TEAM_KEY
    return turn,current_team
    
def does_turn_continue(team,current_team):
    if team == current_team:
        return True
    else:
        return False
    
def does_game_continue():
    if board.team_counts[RED_TEAM_KEY] and board.team_counts[BLUE_TEAM_KEY] and board.team_counts[ASSASSIN_TEAM_KEY]:
        return True
    return False
    
def run():
    turn = 0
    current_team = RED_TEAM_KEY
    board.notify_subscribers()
    display.initialize_screen()
    game_in_progress = True
    while(game_in_progress):
        
        display.draw_screen()
        code, num_words = code_giving_section()
        print(code+ ":",num_words)
        turn_continues = True
        while(turn_continues):
        
            guess_i,guess_j = display.wait_for_input()
            guess=board.words_on_board[guess_i][guess_j][WORD_KEY]
            board.handle_valid_word_selection(guess)
            team=board.get_word_team(guess)
            display.update_button_color(team)
            
            board.update_team_counts(team)
            board.notify_subscribers()
            
            display.draw_screen()
            turn_continues = does_turn_continue(team,current_team)
            game_in_progress = does_game_continue()
                
            turn,current_team = next_turn(turn,current_team)
        
        # find winner, record game states? record turns

if __name__ == '__main__':
    run()
    #print('Finished in ' + str(turn+1) + ' turns.')
    print('Remaing team counts were ' + str(board.get_team_counts()))


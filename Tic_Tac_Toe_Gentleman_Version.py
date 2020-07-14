from copy import deepcopy
from random import randint

#This function prints the game board in a readable format.
def print_board(board):
    print("|-------------|")
    print("| Tic Tac Toe |")
    print("|-------------|")
    print("|             |")
    print("|    " + board[0][0] + " " + board[0][1] + " " + board[0][2] + "    |")
    print("|    " + board[1][0] + " " + board[1][1] + " " + board[1][2] + "    |")
    print("|    " + board[2][0] + " " + board[2][1] + " " + board[2][2] + "    |")
    print("|             |")
    print("|-------------|")
    print()

# This is the starting game board
game_board1 = [['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']]

# This is the replay game board
game_board2 = [['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']]

# This function picks a space in the board
# 'move' refers to the number of the space that is being selected and 'turn' refers to the symbol of the player making the move.
def select_space(board, move, turn):
    if move not in range(1,10):
        return False
    row = int((move-1)/3)
    col = (move-1)%3
    if board[row][col] != "X" and board[row][col] != "O":
        board[row][col] = turn
        return True
    else:
        return False

# This function returns a list of the moves that are still available on the board.
def available_moves(board):
    moves = []
    for row in board:
        for col in row:
            if col != "X" and col != "O":
                moves.append(int(col))
    return moves

# This function checks whether any player has won the game.
def has_won(board, player):
    for row in board:
        if row.count(player) == 3:
            return True
    for i in range(3):
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

# This function checks whether the game is over.
def game_is_over(board):
  if has_won(board, 'X') or has_won(board, 'O') or len(available_moves(board))== 0:
    return True
  else:
    return False

# This function evaluates the board and is created to be used in the minimax function.
# It helps the algorithm 'play' all possible moves and all possible follow-up moves to the end and attach values to the possible outcomes.
# As the algorithm goes through all possible available moves it constantly evaluates whether an outcome value is better than a previous one and if so adjusts the best move.
# Depending on whether the player who's move it is is maximizing or minimizing the definition of best value differs.
def evaluate_board(board):
  if has_won(board, 'X'):
    return 1
  elif has_won(board, 'O'):
    return -1
  else:
    return 0

# This function is the core of the algorithm.
# Given the correct inputs it is able to evaluate the game board and chose the next best move at all times.
def minimax(input_board, is_maximizing):
  # Base case - the game is over, so we return the value of the board
  if game_is_over(input_board):
    return [evaluate_board(input_board), '']
  best_move = ''
  # Because the maximizing player tries to maximise the best value we start at -Inf
  if is_maximizing == True:
    best_value = -float("Inf")
    symbol = "X"
  # Following the same logic we start at +Inf for the minimising player
  else:
    best_value = float("Inf")
    symbol = "O"
  # Loop through every available move and evaluate hypothetical outcomes. Adjust the best value and best move accordingly.
  for move in available_moves(input_board):
    new_board = deepcopy(input_board)
    select_space(new_board, move, symbol)
    hypothetical_value = minimax(new_board, not is_maximizing)[0]
    if is_maximizing == True and hypothetical_value > best_value:
      best_value = hypothetical_value
      best_move = move
    if is_maximizing == False and hypothetical_value < best_value:
      best_value = hypothetical_value
      best_move = move
  return [best_value, best_move]

# This function places the algorithm's move and prints it out.
def ai_move(input_board):
    prev_open = 0
    for i in available_moves(input_board):
        prev_open += i
    # If the AI makes the first move it may as well select a random space for it's move.
    # Because of the way the algorithm works it won't lose anyway.
    # And the randint() function is a lot faster than the minimax() function.
    if(len(available_moves(input_board)) == 9):
        select_space(input_board, randint(1, 9), ai_symbol)
    else:
        select_space(input_board, minimax(input_board, maxi)[1], ai_symbol)
    post_open = 0
    for i in available_moves(input_board):
        post_open += i
    move = prev_open - post_open
    print()
    if (move == 0):
        print(
            'Your \'' + player_symbol + '\' has been placed. There are no more moves left. The game ends in a tie.')
        print_board(input_board)
    elif (len(available_moves(input_board)) == 8):
        print('The AI placed its \'' + ai_symbol + '\' at position ' + str(move) + '.')
    else:
        print(
        'Your \'' + player_symbol + '\' has been placed. The AI placed its \'' + ai_symbol + '\' at position ' + str(
            move) + '.')
    print_board(input_board)

# This is the replay function, which let's the player play again.
def play_again(input_board):
    print()
    print('Cool. Let\'s start the game.')
    # This calculates where the AI has placed it's move.
    ai_move(input_board)
    # Only accept valid input as the first move.
    while True:
        first_move = input('Where would you like to place your first \'' + player_symbol + '\' ?: ')
        if int(first_move) in range(1, 10):
            break
        print('Sorry mate, your choice was invalid. Please try again.')
    # Place first move.
    select_space(input_board, int(first_move), player_symbol)
    # Next AI move.
    ai_move(input_board)
    # Loop through the next rounds of the game.
    for i in range(4):
        while True:
            next_move = input('Where would you like to place your next \'' + player_symbol + '\' ?: ')
            if int(next_move) in available_moves(input_board):
                break
            print('Sorry mate, your choice was invalid. Please try again.')
        # Next AI move.
        select_space(input_board, int(next_move), player_symbol)
        prev_open = 0
        for i in available_moves(input_board):
            prev_open += i
        select_space(input_board, minimax(input_board, maxi)[1], ai_symbol)
        post_open = 0
        for i in available_moves(input_board):
            post_open += i
        move = prev_open - post_open
        print()
        if (move == 0):
            print(
                'Your \'' + player_symbol + '\' has been placed. There are no more moves left. The game ends in a tie.')
            print_board(input_board)
        print(
            'Your \'' + player_symbol + '\' has been placed. The AI placed its \'' + ai_symbol + '\' at position ' + str(
                move) + '.')
        print_board(input_board)
        # Check whether the AI has won.
        if game_is_over(input_board) and has_won(input_board, ai_symbol):
            print('The AI has beaten you. The game is over.')
            break
        # If AI hasn't won, check whether the game ends in a tie.
        elif game_is_over(input_board):
            print('There are no more moves left. The game ends in a tie.')
            break

# This is the game play function that takes the player through the entire game.
def play(input_board):
    # Place first move.
    select_space(input_board, int(first_move), player_symbol)
    # Place first AI move.
    ai_move(input_board)
    # Loop through the next rounds of the game.
    # After this point the game follows the same structure as the replay with the exception of the replay option once the game comes to an end.
    for i in range(4):
        while True:
            next_move = input('Where would you like to place your next \'' + player_symbol + '\' ?: ')
            if int(next_move) in available_moves(input_board):
                break
            print('Sorry mate, your choice was invalid. Please try again.')
        select_space(input_board, int(next_move), player_symbol)
        prev_open = 0
        for i in available_moves(input_board):
            prev_open += i
        select_space(input_board, minimax(input_board, maxi)[1], ai_symbol)
        post_open = 0
        for i in available_moves(input_board):
            post_open += i
        move = prev_open - post_open
        print()
        if (move == 0):
            print(
                'Your \'' + player_symbol + '\' has been placed. There are no more moves left. The game ends in a tie.')
            print_board(input_board)
            print('Would you like to try again? Maybe this time letting the AI go first?')
            while True:
                replay = input('Enter \'Yes\' or \'No\' indicating whether you would like to try again or not: ')
                if replay in ['Yes', 'No']:
                    break
                print('Sorry mate, your choice was invalid. Please try again.')
            if replay == 'Yes':
                play_again(game_board2)
                break
            elif replay == 'No':
                print()
                print('Ok then, see you next time.')
            break
        print(
            'Your \'' + player_symbol + '\' has been placed. The AI placed its \'' + ai_symbol + '\' at position ' + str(
                move) + '.')
        print_board(input_board)
        if game_is_over(input_board) and has_won(input_board, ai_symbol):
            print('The AI has beaten you. The game is over.')



# This is the start of the game.
# It only occurs once so there's no point in defining a function.
print('Welcome to a round of Tic Tac Toe against Jonas\' AI.')
print('Below you see what the game board looks like.')
print('The numbers represent the different spots where a symbol can be placed.')
print('If you want to place your symbol in a certain spot within the board, just select the number that corresponds to that spot in the game board.')
print()
print_board(game_board1)
print('First things first. Please select the symbol you would like to use throughout the game.')

# Only accept valid input as the player symbol.
while True:
        player_symbol = input(
            'Enter either \'X\' or \'O\' (capital o, not zero), depending on which symbol you want and then hit the ENTER key: ')
        if player_symbol in ['X', 'O']:
            break
        print('Sorry mate, your choice was invalid. Please try again.')

# Set the AI's symbol and whether it is maximising or minimising.
if (player_symbol == 'X'):
    ai_symbol = 'O'
    maxi = False
else:
    ai_symbol = 'X'
    maxi = True
print()
print('Awesome! Your symbol is: \'' + player_symbol + '\' and the AI\'s symbol is: \'' + ai_symbol + '\'.')
print()

# Only accept valid input regarding who gets to go first.
print('Next you get to decide who goes first. Would you like to go first or let the AI go first?')
while True:
        starter = input(
            'Enter \'Me\' if you would like to go first and \'AI\' if you would like to let the AI go first and then hit the ENTER key: ')
        if starter in ['Me', 'AI']:
            break
        print('Sorry mate, your choice was invalid. Please try again.')
print()
# Play with the player starting.
if starter == 'Me':
    print('Cool. Let\'s start the game.')
    # Only accept valid input regarding the first move.
    while True:
        first_move = input('Where would you like to place your first \'' + player_symbol + '\' ?: ')
        if int(first_move) in range(1,10):
            break
        print('Sorry mate, your choice was invalid. Please try again.')
    play(game_board1)
# In case the player lets the AI go first.
else:
    print('That is very noble of you but Jonas has trained this AI to be a gentleman.')
    print('As a true gentleman, the AI follows the principle of "Ladies first".')
    while True:
        first_move = input('In line with that principle you get to go first. Where would you like to place your first \'' + player_symbol + '\' ?: ')
        if int(first_move) in range(1,10):
            break
        print('Sorry mate, your choice was invalid. Please try again.')
    play(game_board1)




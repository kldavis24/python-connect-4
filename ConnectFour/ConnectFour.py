import random

# Initializing the width and height for the game board
width = 7
height = 6


def main():
    # Creating the game host object
    host = GameHost()

    print("Connect Four!")

    # Initializing a Player v Player, or Player v Computer match
    mode = host.pick_mode()

    # If the player picks PvP
    while mode == '1':
        # The host will pick who is X and who is O
        player_side1, player_side2 = host.pick_sides()
        turn = pick_turn()

        game_board = new_board()

        # Play through the game type, decide the winner, and display who won
        game = Game(game_board, player_side1, player_side2)
        winner = game.player_vs_player(turn)
        display_winner(game_board, winner)

        # Ask the user if they'd like to play again
        if not host.play_again():
            break

    # If the player picks PvC
    while mode == '2':
        # The host picks who is X and who is O
        player_side, computer_side = host.pick_sides()
        turn = pick_turn()

        # Displaying which player will go first and printing a blank board
        print('\n' + turn + ' will go first.')
        game_board = new_board()

        # Play through the game type, decide the winner, and display who won
        game = Game(game_board, player_side, computer_side)
        winner = game.player_vs_computer(turn)
        display_winner(game_board, winner)

        # Ask the user if they'd like to play again
        if not host.play_again():
            break


# ****************************************** CLASSES AND METHODS ******************************************

class GameHost:
    def __init__(self):
        self.turn = ''
        self.side = ''
        self.choice = ''
        self.mode = 0

    # The user picks which mode to play in
    def pick_mode(self):
        while self.mode != '1' or self.mode != '2':
            print('Choose the game mode:')
            print('(1) Player vs. Player')
            print('(2) Player vs. Computer')
            mode = input()

            if mode == '1':
                print('\nPlayer vs. Player mode selected!\n')
                return mode
            elif mode == '2':
                print('\nPlayer vs. Computer mode selected!\n')
                return mode
            else:
                print('\nPlease select either 1 or 2!\n')

    # A method for the user to choose a marker
    def pick_sides(self):
        while self.side.lower() != 'x' or self.side.lower() != 'o':
            print('Do you want to be X or O?')
            side = input()

            # The returned tuple's values are [user side, computer side]
            if side.lower() == 'x':
                print('\nPlayer 1 = X')
                print('Player 2 = O')
                return ['X', 'O']
            elif side.lower() == 'o':
                print('\nPlayer 1 = O')
                print('Player 2 = X')
                return ['O', 'X']
            elif side.lower() != 'x' or side.lower() != 'o':
                print('Please select X or O!')

    # This will ask the user to play again after a winner or a tie is found
    def play_again(self):
        while self.choice != 'yes' or self.choice != 'no':
            print('Do you want to play again? (yes or no)')
            choice = input().lower()

            if choice == 'yes':
                return True
            elif choice == 'no':
                print('Thanks for playing!')
                return False
            else:
                print('Please enter yes or no!')


class Game:
    def __init__(self, game_board, player_side1, player_side2):
        self.game_board = game_board
        self.player_side1 = player_side1
        self.player_side2 = player_side2

    def player_vs_computer(self, turn):
        while True:
            if turn == 'Player 1':
                player_turn(self.game_board, self.player_side1)

                # If player 1 has 4-in-a-row, they win - if not it is player 2's turn
                if check_for_winner(self.game_board, self.player_side1):
                    winner = 'Player 1'
                    break
                turn = 'Player 2'
            else:
                computer_turn(self.game_board, self.player_side2)

                # If the computer has 4-in-a-row, they win - if not it is player 1's turn
                if check_for_winner(self.game_board, self.player_side2):
                    winner = 'Player 2'
                    break
                turn = 'Player 1'

            # If the board is full with no winners, the game is a tie
            if check_board(self.game_board):
                winner = 'Tie'
                break
        return winner

    def player_vs_player(self, turn):
        while True:
            if turn == 'Player 1':
                player_turn(self.game_board, self.player_side1)

                # If player 1 has 4-in-a-row, they win - if not it's player 2's turn
                if check_for_winner(self.game_board, self.player_side1):
                    winner = turn
                    break
                turn = 'Player 2'
            else:
                player_turn(self.game_board, self.player_side2)

                # If player 2 has 4-in-a-row, they win - if not it's player 1's turn
                if check_for_winner(self.game_board, self.player_side2):
                    winner = turn
                    break
                turn = 'Player 1'

                # If the board is full with no winners, the game is a tie
                if check_board(self.game_board):
                    winner = 'Tie'
                    break
        return winner


# Print the winner of the game
def display_winner(game_board, winner):
    print_board(game_board)
    print('Winner is: %s' % winner)


# Mark the player's chosen move
def computer_turn(game_board, side):
    # Print the board, get a random number (1-7) and display the move
    print_board(game_board)
    move = get_computer_move(game_board)
    make_move(game_board, side, move)


# Mark the computer's random move
def player_turn(game_board, side):
    # Print the board, ask for player 1's move, and display the move
    print_board(game_board)
    move = get_player_move(game_board)
    make_move(game_board, side, move)


# Printing out a blank board
def print_board(board):
    print("\n\tConnect Four")

    for x in range(1, width + 1):
        print('  %s ' % x, end='')

    print('\n-----' + ('----' * (width - 1)))

    for y in range(height):
        print('|', end='')

        for x in range(width):
            print(' %s |' % board[x][y], end='')
        print('\n-----' + ('----' * (width - 1)))


# Quickly recall the board
def new_board():
    board = []

    for x in range(width):
        board.append([' '] * height)
    return board


# After the move is chosen, the player's mark will be left on the board
def make_move(board, player, column):
    for y in range(height - 1, -1, -1):
        if board[column][y] == ' ':
            board[column][y] = player
            return


# Check to see if the board is full with no winners
def check_board(board):
    for x in range(width):
        for y in range(height):
            if board[x][y] == ' ':
                return False
    return True


# Check for a winner after every move
def check_for_winner(board, tile):
    # Checking for a horizontal winner
    for y in range(height):
        for x in range(width - 3):
            if board[x][y] == tile \
                    and board[x + 1][y] == tile \
                    and board[x + 2][y] == tile \
                    and board[x + 3][y] == tile:
                return True

    # Checking for a vertical winner
    for x in range(width):
        for y in range(height - 3):
            if board[x][y] == tile \
                    and board[x][y + 1] == tile \
                    and board[x][y + 2] == tile \
                    and board[x][y + 3] == tile:
                return True

    # Checking for a upward diagonal winner
    for x in range(width - 3):
        for y in range(3, height):
            if board[x][y] == tile \
                    and board[x + 1][y - 1] == tile \
                    and board[x + 2][y - 2] == tile \
                    and board[x + 3][y - 3] == tile:
                return True

    # Checking for a downward diagonal winner
    for x in range(width - 3):
        for y in range(height - 3):
            if board[x][y] == tile \
                    and board[x + 1][y + 1] == tile \
                    and board[x + 2][y + 2] == tile \
                    and board[x + 3][y + 3] == tile:
                return True
    return False


# Decides if the move is allowed
def is_valid_move(board, move):
    if move < 0 or move >= width:
        return False

    if board[move][0] != ' ':
        return False

    return True


# Randomly choose which player goes first
def pick_turn():
    if random.randint(0, 1) == 0:
        print('\nPlayer 2 will go first.')
        return 'Player 2'
    else:
        print('\nPlayer 1 will go first.')
        return 'Player 1'


# Prompts the user to enter a position on the board to move on
def get_player_move(board):
    while True:
        print('\nPick a column to make your move!')
        move = input()

        if not move.isdigit():
            continue
        move = int(move) - 1

        if is_valid_move(board, move):
            return move
        else:
            print('Invalid move!')


# The computer will pick a random, valid place to play on the board
def get_computer_move(board):
    while True:
        move = random.randint(0, 8)
        move = int(move) - 1

        if is_valid_move(board, move):
            return move


# Calling the main function
main()

import random
import copy
import sys
import os

# Initializing the width and height for the game board
width = 7
height = 6


def main():
    # Creating objects of the classes to play the game
    host = GameHost()
    judge = Judge()
    player1 = Player()
    player2 = Player()
    board = Board()
    panel = Panel()

    print("Connect Four!")

    # Initializing a player v player, or player v computer match
    mode = host.pick_mode()

    # If the player picks PvP
    while mode == '1':
        # The host will pick who is X and who is O
        player_side1, player_side2 = host.pick_sides()
        turn = host.pick_turn()
        # The host will display who goes first and print a blank board
        print('\n' + turn + ' will go first.')
        game_board = board.new_board()

        while True:
            if turn == 'Player 1':  # If it is player 1's turn
                # Print the board, ask for his move, and display his move
                board.print_board(game_board)
                move = panel.get_player_move(game_board)
                player1.make_move(game_board, player_side1, move)
                # If player 1 has 4-in-a-row he wins, if not it's player 2's turn
                if judge.check_for_winner(game_board, player_side1):
                    winner = 'Player 1'
                    break
                turn = 'Player 2'
            else:  # If it is player 2's turn
                # Print the  board ask for this move, and display his move
                board.print_board(game_board)
                move = panel.get_player_move(game_board)
                player2.make_move(game_board, player_side2, move)
                # If player 2 has 4-in-a-row he wins, if not it's player 1's turn
                if judge.check_for_winner(game_board, player_side2):
                    winner = 'Player 2'
                    break
                turn = 'Player 1'

                # If the board is full with no winners, the game is a tie
                if judge.check_board(game_board):
                    winner = 'Tie'
                    break

        # Print the winner of the game and ask the user to play again
        board.print_board(game_board)
        print('Winner is: %s' % winner)
        if not host.play_again():
            break

    # If the player picks PvC
    while mode == '2':
        # The host picks who is X and who is O
        player_side, computer_side = host.pick_sides()
        turn = host.pick_turn()
        # Displaying which player will go first and printing a blank board
        print('\n' + turn + ' will go first.')
        game_board = board.new_board()

        while True:
            if turn == 'Player 1':  # If it is player 1's turn
                # Print the board, ask for his move, and display his move
                board.print_board(game_board)
                move = panel.get_player_move(game_board)
                player1.make_move(game_board, player_side, move)
                # If player 1 has 4-in-a-row he wins, if not it is player 2's turn
                if judge.check_for_winner(game_board, player_side):
                    winner = 'Player 1'
                    break
                turn = 'Player 2'
            else:  # If it is the computer's turn
                # Print the board, get a random number (1-7) and display his ove
                board.print_board(game_board)
                move = panel.get_computer_move(game_board)
                player2.make_move(game_board, computer_side, move)
                # If the computer has 4-in-a-row he wins, if not it is player 1's turn
                if judge.check_for_winner(game_board, computer_side):
                    winner = 'Player 2'
                    break
                turn = 'Player 1'

            # If the board is full with no winners, the game is a tie
            if judge.check_board(game_board):
                winner = 'Tie'
                break

        # Print the winner of the game and ask the user to play again
        board.print_board(game_board)
        print('Winner is: %s' % winner)
        if not host.play_again():
            break


# ****************************************** CLASSES ******************************************

class Board:
    # The method for printing out a blank board
    def print_board(self, board):
        print()
        print(' ', end='')
        print("       Connect Four")
        for x in range(1, width + 1):
            print(' %s  ' % x, end='')
        print()

        print('-----' + ('----' * (width - 1)))

        for y in range(height):
            print('|', end='')
            for x in range(width):
                print(' %s |' % board[x][y], end='')
            print()
            print('-----' + ('----' * (width - 1)))

    # A short method to quickly recall the board
    def new_board(self):
        board = []
        for x in range(width):
            board.append([' '] * height)
        return board


class Player:
    # After the move is chosen, the player's mark will be left on the board
    def make_move(self, board, player, column):
        for y in range(height - 1, -1, -1):
            if board[column][y] == ' ':
                board[column][y] = player
                return


class Judge:
    # The game is a tie if the board is full with no winners
    def check_board(self, board):
        for x in range(width):
            for y in range(height):
                if board[x][y] == ' ':
                    return False
        return True

    # The judge decides if the move is allowed
    def is_valid_move(self, board, move):
        if move < 0 or move >= (width):
            return False

        if board[move][0] != ' ':
            return False

        return True

    # The judge will check for a winner after every move
    def check_for_winner(self, board, tile):
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


class GameHost:
    # The user picks which mode to play in
    def pick_mode(self, choice=0):
        self.mode = choice
        mode = ''
        while mode != '1' or mode != '2':
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
    def pick_sides(self, tile=''):
        self.side = tile
        side = ''
        while side != 'X' or side != 'x' or side != 'O' or side != 'o':
            print('Do you want to be X or O?')
            side = input()

            # The returned tuple's values are [user side, computer side]
            if side == 'X' or side == 'x':
                print('\nPlayer 1 = X')
                print('Player 2 = O')
                return ['X', 'O']
            elif side == 'O' or side == 'o':
                print('\nPlayer 1 = O')
                print('Player 2 = X')
                return ['O', 'X']
            elif side != 'X' or side != 'x' or side != 'O' or side != 'o':
                print('Please select X or O!')

    # Randomly choose which player goes first
    def pick_turn(self):
        if random.randint(0, 1) == 0:
            return 'Player 2'
        else:
            return 'Player 1'

    # Display which player will go first
    def display_turn(self, pick=''):
        self.turn = pick
        turn = self.pick_turn()
        print('\n%s will go first.\n' % turn)

    # This will ask the user to play again after a winner or a tie is found
    def play_again(self):
        choice = ''
        while choice != 'yes' or choice != 'no':
            print('Do you want to play again? (yes or no)')
            choice = input().lower()

            if choice == 'yes':
                return True
            elif choice == 'no':
                print('Thanks for playing!')
                return False
            else:
                print('Please enter yes or no!')

    # Decides if the move is allowed
    def is_valid_move(self, board, move):
        if move < 0 or move >= width:
            return False

        if board[move][0] != ' ':
            return False

        return True


class Panel(GameHost):
    # Prompts the user to enter a position on the board to move on
    def get_player_move(self, board):
        while True:
            print('\nPick a column to make your move!')
            move = input()
            if not move.isdigit():
                continue
            move = int(move) - 1
            if self.is_valid_move(board, move):
                return move
            else:
                print('Invalid move!')

    # The computer will pick a random place to play on the board
    def get_computer_move(self, board):
        while True:
            move = random.randint(0, 8)
            move = int(move) - 1
            if self.is_valid_move(board, move):
                return move


# Calling the main function
main()

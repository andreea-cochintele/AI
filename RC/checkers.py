# Cochintele Andreea
# Grupa 231
# Proiect 2 / Laboratorul 9
# PB_6-- Dame / Checkers


from copy import deepcopy
import time
import math


class Node:
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        #self.value = value
        self.move = move
        #self.parent = parent

    def get_children(self, maximizing_player, mandatory_jumping, computer_color, player_color):
        # Generate and returns the children of the current state
        current_state = deepcopy(self.board)
        children_states = []
        if maximizing_player is True:
            # For the computer we always have the maximizing_player True
            available_moves = Checkers.find_available_moves(current_state, mandatory_jumping, computer_color,
                                                            player_color)
            big_letter = computer_color.upper()
            queen_row = 7
        else:
            # Generate the children for the player
            available_moves = Checkers.find_player_available_moves(current_state, mandatory_jumping, player_color,
                                                                   computer_color)
            big_letter = player_color.upper()
            queen_row = 0
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            Checkers.make_a_move(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
            children_states.append(Node(state, [old_i, old_j, new_i, new_j]))
        return children_states

    def get_children2(self, maximizing_player, computer_color, player_color, m, n):
        # Generate and returns the children of the current state
        current_state = deepcopy(self.board)
        children_states = []
        if maximizing_player is True:
            # For the computer we always have the maximizing_player True
            available_moves = Checkers.another_computer_move_available(current_state, player_color, computer_color, m, n)
            big_letter = computer_color.upper()
            queen_row = 7
        else:
            # Generate the children for the player
            available_moves = Checkers.another_move_available(current_state,  player_color,
                                                                   computer_color, m, n)
            big_letter = player_color.upper()
            queen_row = 0
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            Checkers.make_a_move(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
            children_states.append(Node(state, [old_i, old_j, new_i, new_j]))
        return children_states

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_board(self):
        return self.board

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent


class Checkers:
    def __init__(self):
        self.matrix = [[], [], [], [], [], [], [], []]
        self.current_turn = True
        self.computer_pieces = 12
        self.player_pieces = 12
        self.available_moves = []
        self.mandatory_jumping = False
        self.depth = 4
        self.algorithm = 1
        self.player_color = ''
        self.computer_color = ''
        self.player_moves = 0
        self.computer_moves = 0
        self.t = 0
        self.cjump = 0
        self.pjump = 0
    def set_cjump(self, x):
        self.cjump = x

    def set_pjump(self, x):
        self.pjump = x

    def beginning(self):
        for row in self.matrix:
            for i in range(8):
                row.append("---")
        self.position_computer()
        self.position_player()

    def position_computer(self):
        # Place the pieces for the computer
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = (self.computer_color + str(i) + str(j))

    def position_player(self):
        # Place the pieces for the player
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = (self.player_color + str(i) + str(j))

    def print_matrix(self):
        # The function for printing the table
        i = 0
        print()
        for row in self.matrix:
            print(i, end="  |")
            i += 1
            for elem in row:
                print(elem, end=" ")
            print()
        print()
        for j in range(8):
            if j == 0:
                j = "     0"
            print(j, end="   ")
        print("\n")

    # Player's move
    def get_player_input(self):
        t1 = time.time()
        # Generate all available moves for player
        available_moves = Checkers.find_player_available_moves(self.matrix, self.mandatory_jumping, self.player_color,
                                                               self.computer_color)
        # Verify if we have available moves

        if len(available_moves) == 0:
            if self.computer_pieces > self.player_pieces:
                print("You have no moves left, and you have fewer pieces than the computer.YOU LOSE!")
                print("Computer have " + str(12 - self.computer_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()
            else:
                print("You have no available moves.\nGAME ENDED!")
                print("You have " + str(12 - self.player_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()
        self.player_pieces = 0
        self.computer_pieces = 0
        while True:
            # If we press enter or s we end the game
            coord1 = input("Which piece[i,j]: ")
            if coord1 == "":
                print("Game ended!")
                print("Computer have " + str(12 - self.computer_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()
            elif coord1 == "s":
                print("You surrendered.\n")
                print("Computer have " + str(12 - self.computer_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()
            coord2 = input("Where to[i,j]:")
            if coord2 == "":
                print("Game ended!")
                print("Computer have " + str(12 - self.computer_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()
            elif coord2 == "s":
                print("You surrendered.\n")
                print("Computer have " + str(12 - self.computer_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()
            old = coord1.split(",")
            new = coord2.split(",")

            # Verify if our input is correct
            if len(old) != 2 or len(new) != 2:
                print("Ilegal input")
            else:
                old_i = old[0]
                old_j = old[1]
                new_i = new[0]
                new_j = new[1]
                if not old_i.isdigit() or not old_j.isdigit() or not new_i.isdigit() or not new_j.isdigit():
                    print("Ilegal input")
                else:
                    # If the input is correct, verify if that is an available move
                    move = [int(old_i), int(old_j), int(new_i), int(new_j)]
                    if move not in available_moves:
                        print("Ilegal move!")
                    else:
                        # Making the move and calculating the remaining pieces
                        t2 = time.time()
                        diff = t2 - t1
                        print("You moved (" + str(move[0]) + "," + str(move[1]) + ") to (" + str(move[2]) + "," + str(
                            move[3]) + ").")
                        print("It took you " + str(diff) + " seconds.")
                        Checkers.make_a_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j),
                                             self.player_color.upper(), 0)
                        for m in range(8):
                            for n in range(8):
                                if self.matrix[m][n][0] == self.computer_color or self.matrix[m][n][
                                    0] == self.computer_color.upper():
                                    self.computer_pieces += 1
                                elif self.matrix[m][n][0] == self.player_color or self.matrix[m][n][
                                    0] == self.player_color.upper():
                                    self.player_pieces += 1
                        available_moves = Checkers.another_move_available(self.matrix, self.player_color, self.computer_color, int(new_i), int(new_j))
                        if len(available_moves) == 0:
                            break
                        else:
                            if self.mandatory_jumping is True:
                                if self.pjump == 1:
                                    print("You have another available jump with the same piece.")
                                    continue
                                else:
                                    break
                            else:
                                break

    @staticmethod
    def find_available_moves(board, mandatory_jumping, computer_color, player_color):
        # Find the available moves for the computer for every pieces
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                if board[m][n][0] == computer_color:
                    # Down and Right move
                    if Checkers.check_moves(board, m, n, m + 1, n + 1, player_color):
                        available_moves.append([m, n, m + 1, n + 1])
                    # Down and Left move
                    if Checkers.check_moves(board, m, n, m + 1, n - 1, player_color):
                        available_moves.append([m, n, m + 1, n - 1])
                    # Down and Left jump
                    if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2, computer_color, player_color):
                        available_jumps.append([m, n, m + 2, n - 2])
                    # Down and Right jump
                    if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2, computer_color, player_color):
                        available_jumps.append([m, n, m + 2, n + 2])
                elif board[m][n][0] == computer_color.upper():
                    # Down and Right move
                    if Checkers.check_moves(board, m, n, m + 1, n + 1, player_color):
                        available_moves.append([m, n, m + 1, n + 1])
                    # Down and Left move
                    if Checkers.check_moves(board, m, n, m + 1, n - 1, player_color):
                        available_moves.append([m, n, m + 1, n - 1])
                    # Up and Left move
                    if Checkers.check_moves(board, m, n, m - 1, n - 1, player_color):
                        available_moves.append([m, n, m - 1, n - 1])
                    # Up and Right move
                    if Checkers.check_moves(board, m, n, m - 1, n + 1, player_color):
                        available_moves.append([m, n, m - 1, n + 1])
                    # Down and Left jump
                    if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2, computer_color, player_color):
                        available_jumps.append([m, n, m + 2, n - 2])
                    # Up and Left jump
                    if Checkers.check_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2, computer_color, player_color):
                        available_jumps.append([m, n, m - 2, n - 2])
                    # Up and Right jump
                    if Checkers.check_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2, computer_color, player_color):
                        available_jumps.append([m, n, m - 2, n + 2])
                    # Down and Right jump
                    if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2, computer_color, player_color):
                        available_jumps.append([m, n, m + 2, n + 2])
        # If we choose that jumping in mandatory, if we have can jump we should jump so the algorithm return as legal move just the jumps
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                Checkers.set_cjump(checkers, 1)
                return available_jumps

    @staticmethod
    def check_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j, computer_color, player_color):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[via_i][via_j] == "---":
            return False
        if board[via_i][via_j][0] == computer_color.upper() or board[via_i][via_j][0] == computer_color:
            return False
        if board[new_i][new_j] != "---":
            return False
        if board[old_i][old_j] == "---":
            return False
        if board[old_i][old_j][0] == player_color or board[old_i][old_j][0] == player_color.upper():
            return False
        return True

    @staticmethod
    def check_moves(board, old_i, old_j, new_i, new_j, player_color):

        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[old_i][old_j] == "---":
            return False
        if board[new_i][new_j] != "---":
            return False
        if board[old_i][old_j][0] == player_color or board[old_i][old_j][0] == player_color.upper():
            return False
        if board[new_i][new_j] == "---":
            return True

    @staticmethod
    def calculate_score(board, computer_color, player_color):
        result = 0
        mine = 0
        opp = 0
        for i in range(8):
            for j in range(8):
                if board[i][j][0] == computer_color or board[i][j][0] == computer_color.upper():
                    # Calculate the number of pieces of the computer
                    mine += 1

                    # Result +5 for normal pieces
                    if board[i][j][0] == computer_color:
                        result += 5
                    # Result +10 if it's a king
                    if board[i][j][0] == computer_color.upper():
                        result += 10
                    # Result +7 if it's on a margin
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        result += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7:
                        continue

                    # Decrement the result with 3 points if it the player can take the man
                    if (board[i + 1][j - 1][0] == player_color or board[i + 1][j - 1][0] == player_color.upper()) and \
                            board[i - 1][j + 1] == "---":
                        result -= 3
                    if (board[i + 1][j + 1][0] == player_color or board[i + 1][j + 1] == player_color.upper()) and \
                            board[i - 1][j - 1] == "---":
                        result -= 3
                    if board[i - 1][j - 1][0] == player_color.upper() and board[i + 1][j + 1] == "---":
                        result -= 3
                    if board[i - 1][j + 1][0] == player_color.upper() and board[i + 1][j - 1] == "---":
                        result -= 3

                    # Increment with 6 if we can take the man
                    if i + 2 > 7 or i - 2 < 0:
                        continue
                    if (board[i + 1][j - 1][0] == player_color.upper() or board[i + 1][j - 1][0] == player_color) and \
                            board[i + 2][j - 2] == "---":
                        result += 6

                    if i + 2 > 7 or j + 2 > 7:
                        continue
                    if (board[i + 1][j + 1][0] == player_color.upper() or board[i + 1][j + 1][0] == player_color) and \
                            board[i + 2][j + 2] == "---":
                        result += 6

                elif board[i][j][0] == player_color or board[i][j][0] == player_color.upper():
                    # Calculate the number of pieces of the player
                    opp += 1

        return result + (mine - opp) * 1000

    @staticmethod
    def find_player_available_moves(board, mandatory_jumping, player_color, computer_color):
        # Find all the available moves for every pieces
        available_moves = []
        available_jumps = []
        for m in range(8):
            for n in range(8):
                # Verify if the piece is normal or king
                if board[m][n][0] == player_color:
                    # Up and Left move
                    if Checkers.check_player_moves(board, m, n, m - 1, n - 1, computer_color):
                        available_moves.append([m, n, m - 1, n - 1])
                    # Up and Right move
                    if Checkers.check_player_moves(board, m, n, m - 1, n + 1, computer_color):
                        available_moves.append([m, n, m - 1, n + 1])
                    # Up and Left jump
                    if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2, player_color,
                                                   computer_color):
                        available_jumps.append([m, n, m - 2, n - 2])
                    # Up and Right jump
                    if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2, player_color,
                                                   computer_color):
                        available_jumps.append([m, n, m - 2, n + 2])
                elif board[m][n][0] == player_color.upper():
                    # Up and Left move
                    if Checkers.check_player_moves(board, m, n, m - 1, n - 1, computer_color):
                        available_moves.append([m, n, m - 1, n - 1])
                    # Up and Right move
                    if Checkers.check_player_moves(board, m, n, m - 1, n + 1, computer_color):
                        available_moves.append([m, n, m - 1, n + 1])
                    # Up and Left jump
                    if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2, player_color,
                                                   computer_color):
                        available_jumps.append([m, n, m - 2, n - 2])
                    # Up and Right jump
                    if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2, player_color,
                                                   computer_color):
                        available_jumps.append([m, n, m - 2, n + 2])
                    # Down and Left move
                    if Checkers.check_player_moves(board, m, n, m + 1, n - 1, computer_color):
                        available_moves.append([m, n, m + 1, n - 1])
                    # Down and Left jump
                    if Checkers.check_player_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2, player_color,
                                                   computer_color):
                        available_jumps.append([m, n, m + 2, n - 2])
                    # Down and Right move
                    if Checkers.check_player_moves(board, m, n, m + 1, n + 1, computer_color):
                        available_moves.append([m, n, m + 1, n + 1])
                    # Down and Right jump
                    if Checkers.check_player_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2, player_color,
                                                   computer_color):
                        available_jumps.append([m, n, m + 2, n + 2])

        # If we choose that jumping in mandatory, if we have can jump we should jump so the algorithm return as legal move just the jumps
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                Checkers.set_pjump(checkers, 1)
                return available_jumps


    @staticmethod
    def check_player_moves(board, old_i, old_j, new_i, new_j, computer_color):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[old_i][old_j] == "---":
            return False
        if board[new_i][new_j] != "---":
            return False
        if board[old_i][old_j][0] == computer_color or board[old_i][old_j][0] == computer_color.upper():
            return False
        if board[new_i][new_j] == "---":
            return True

    @staticmethod
    def check_player_jumps(board, old_i, old_j, via_i, via_j, new_i, new_j, player_color, computer_color):
        if new_i > 7 or new_i < 0:
            return False
        if new_j > 7 or new_j < 0:
            return False
        if board[via_i][via_j] == "---":
            return False
        if board[via_i][via_j][0] == player_color.upper() or board[via_i][via_j][0] == player_color:
            return False
        if board[new_i][new_j] != "---":
            return False
        if board[old_i][old_j] == "---":
            return False
        if board[old_i][old_j][0] == computer_color or board[old_i][old_j][0] == computer_color.upper():
            return False
        return True

    def evaluate_states(self):
        # t1 is the starting time
        t1 = time.time()
        current_state = Node(deepcopy(self.matrix))

        # Generates all the children from the current state
        first_computer_moves = current_state.get_children(True, self.mandatory_jumping, self.computer_color,
                                                          self.player_color)
        # If we don't have childrens, we don't have any available move
        if len(first_computer_moves) == 0:
            if self.player_pieces > self.computer_pieces:
                print("Computer has no available moves left, and you have more pieces left.\nYOU WIN!")
                print("You have " + str(12 - self.player_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()
            else:
                print("Computer has no available moves left.\nGAME ENDED!")
                print("You have " + str(12 - self.player_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()

        # If we have moves we can apply the chosen algorithm
        while True:
            dictionary = {}
            for i in range(len(first_computer_moves)):
                child = first_computer_moves[i]
                if self.algorithm == '1':
                    # Minimax
                    value = Checkers.minimax(child.get_board(), self.depth, False, self.mandatory_jumping,
                                             self.computer_color, self.player_color)
                else:
                    # Alpha-Beta Pruning
                    value = Checkers.alphabeta(child.get_board(), self.depth, -math.inf, math.inf, False,
                                               self.mandatory_jumping, self.computer_color, self.player_color)
                dictionary[value] = child

            if len(dictionary.keys()) == 0:
                print("Computer has cornered itself.\nYOU WIN!")
                print("You have " + str(12 - self.player_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()

            # Replace with the new board and print it
            new_board = dictionary[max(dictionary)].get_board()
            move = dictionary[max(dictionary)].move
            self.matrix = new_board
            t2 = time.time()
            diff = t2 - t1
            print("Computer has moved (" + str(move[0]) + "," + str(move[1]) + ") to (" + str(move[2]) + "," + str(
                move[3]) + ").")
            print("It took him " + str(diff) + " seconds.")

            first_computer_moves = current_state.get_children2(self.matrix, self.player_color,
                                                                            self.computer_color, move[2], move[3])
            if len(first_computer_moves) == 0:
                break
            else:
                if self.mandatory_jumping is True and self.cjump == 1:
                    print("The computer have another jump available.")
                    continue
                else:
                    break

    @staticmethod
    def alphabeta(board, depth, alpha, beta, maximizing_player, mandatory_jumping, computer_color, player_color):
        if depth == 0:
            # Calculate the score
            return Checkers.calculate_score(board, computer_color, player_color)
        current_state = Node(deepcopy(board))

        if maximizing_player is True:
            # For the max player
            max_eval = -math.inf
            for child in current_state.get_children(True, mandatory_jumping, computer_color, player_color):
                # Calculate the score for the current son
                ev = Checkers.alphabeta(child.get_board(), depth - 1, alpha, beta, False, mandatory_jumping,
                                        computer_color, player_color)
                # Modifying alpha and the max evaluation
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                # If the new alpha is greater than beta, we can prune
                if beta <= alpha:
                    break
            # We update the father score
            current_state.set_value(max_eval)
            return max_eval
        else:
            # For the min player
            min_eval = math.inf
            for child in current_state.get_children(False, mandatory_jumping, computer_color, player_color):
                # Calculate the score for the current son
                ev = Checkers.alphabeta(child.get_board(), depth - 1, alpha, beta, True, mandatory_jumping,
                                        computer_color, player_color)
                # Modifying alpha and the min evaluation
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                # If the new alpha is greater than beta, we can prune
                if beta <= alpha:
                    break
            # We update the father score
            current_state.set_value(min_eval)
            return min_eval

    @staticmethod
    def minimax(board, depth, maximizing_player, mandatory_jumping, computer_color, player_color):
        if depth == 0:
            # Calculate the score
            return Checkers.calculate_score(board, computer_color, player_color)
        current_state = Node(deepcopy(board))

        if maximizing_player is True:
            # If it's the max player, we choose the son with the max score
            max_eval = -math.inf
            for child in current_state.get_children(True, mandatory_jumping, computer_color, player_color):
                # Calculate the score for the current son
                ev = Checkers.minimax(child.get_board(), depth - 1, False, mandatory_jumping, computer_color,
                                      player_color)
                max_eval = max(max_eval, ev)
            current_state.set_value(max_eval)
            return max_eval
        else:
            # If it's the min player, we choose the son with the min score
            min_eval = -math.inf
            for child in current_state.get_children(True, mandatory_jumping, computer_color, player_color):
                # Calculate the score for the current son
                ev = Checkers.minimax(child.get_board(), depth - 1, False, mandatory_jumping, computer_color,
                                      player_color)
                min_eval = min(min_eval, ev)
            current_state.set_value(min_eval)
            return min_eval

    @staticmethod
    def make_a_move(board, old_i, old_j, new_i, new_j, big_letter, queen_row):
        # This function move the pieces and verify if it need to be transform in a king
        letter = board[old_i][old_j][0]
        i_difference = old_i - new_i
        j_difference = old_j - new_j
        if i_difference == -2 and j_difference == 2:
            board[old_i + 1][old_j - 1] = "---"

        elif i_difference == 2 and j_difference == 2:
            board[old_i - 1][old_j - 1] = "---"

        elif i_difference == 2 and j_difference == -2:
            board[old_i - 1][old_j + 1] = "---"

        elif i_difference == -2 and j_difference == -2:
            board[old_i + 1][old_j + 1] = "---"

        if new_i == queen_row:
            letter = big_letter
        board[old_i][old_j] = "---"
        board[new_i][new_j] = str(letter) + str(new_i) + str(new_j)

    @staticmethod
    def another_move_available(board, player_color, computer_color, m, n):
        # Find if there is any available jump we need to do
        available_jumps = []
        if board[m][n][0] == player_color:
            # Up and Left jump
            if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2, player_color,
                                           computer_color):
                available_jumps.append([m, n, m - 2, n - 2])
            # Up and Right jump
            if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2, player_color,
                                           computer_color):
                available_jumps.append([m, n, m - 2, n + 2])
        elif board[m][n][0] == player_color.upper():
            # Up and Left jump
            if Checkers.check_player_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2, player_color,
                                           computer_color):
                available_jumps.append([m, n, m - 2, n - 2])
            # Up and Right jump
            if Checkers.check_player_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2, player_color,
                                           computer_color):
                available_jumps.append([m, n, m - 2, n + 2])
            # Down and Left jump
            if Checkers.check_player_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2, player_color,
                                           computer_color):
                available_jumps.append([m, n, m + 2, n - 2])
            # Down and Right jump
            if Checkers.check_player_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2, player_color,
                                           computer_color):
                available_jumps.append([m, n, m + 2, n + 2])
        return available_jumps

    @staticmethod
    def another_computer_move_available(board, player_color, computer_color, m, n):
        # Find if there is any available jump the computer need to do
        available_jumps = []
        if board[m][n][0] == computer_color:
            # Down Left
            if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2, computer_color, player_color):
                available_jumps.append([m, n, m + 2, n - 2])
            # Down Right
            if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2, computer_color, player_color):
                available_jumps.append([m, n, m + 2, n + 2])
        elif board[m][n][0] == computer_color.upper():
            # Down Left
            if Checkers.check_jumps(board, m, n, m + 1, n - 1, m + 2, n - 2, computer_color, player_color):
                available_jumps.append([m, n, m + 2, n - 2])
            # Up Left
            if Checkers.check_jumps(board, m, n, m - 1, n - 1, m - 2, n - 2, computer_color, player_color):
                available_jumps.append([m, n, m - 2, n - 2])
            # Up Right
            if Checkers.check_jumps(board, m, n, m - 1, n + 1, m - 2, n + 2, computer_color, player_color):
                available_jumps.append([m, n, m - 2, n + 2])
            # Down Right
            if Checkers.check_jumps(board, m, n, m + 1, n + 1, m + 2, n + 2, computer_color, player_color):
                available_jumps.append([m, n, m + 2, n + 2])
        return available_jumps

    def play(self):
        self.t = time.time()
        print("##### WELCOME TO CHECKERS ####")
        print("\nRules:")
        print("1.You enter the coordinates in the form i,j.")
        print("2.You can quit the game at any time by pressing enter.")
        print("3.You can surrender at any time by pressing 's'.")
        print("Enjoy! :) ")
        while True:
            answer = input("\nIs jumping mandatory?[Y/n]: ")
            if answer == "Y":
                self.mandatory_jumping = True
                break
            elif answer == "n":
                self.mandatory_jumping = False
                break
            else:
                print("Invalid option!")

        while True:
            answer = input("Choose the algorithm you want to use: [1/2]\n1.Minimax\n2.Alpha-Beta Pruning")
            if answer in ['1', '2']:
                self.algorithm = answer
                break
            else:
                print("Invalid option!")

        while True:
            answer = input("\nDificulty[1/2/3]:")
            if answer in ['1', '2', '3']:
                if answer == '1':
                    self.depth = 2
                    break
                elif answer == '2':
                    self.depth = 4
                    break
                elif answer == '3':
                    self.depth = 6
                    break
            else:
                print("Invalid option!")

        while True:
            answer = input("\nWhite or Black?[w/b]")
            if answer in ['w']:
                self.player_color = str("w")
                self.computer_color = str("b")
                # Generate the initial state
                self.beginning()
                break
            elif answer in ['b']:
                self.player_color = str("b")
                self.computer_color = str("w")
                # Generate the initial state
                self.beginning()
                break
            else:
                print("Invalid option!")

        # I used as score the pieces left
        while True:
            self.print_matrix()
            if self.current_turn is True:
                print("\nPlayer's turn.")
                self.player_moves = self.player_moves + 1
                self.pjump = 0
                self.get_player_input()
            else:
                print("Computer's turn.")
                print("Thinking...")
                self.cjump = 0
                self.computer_moves = self.computer_moves + 1
                self.evaluate_states()
            if self.player_pieces == 0:
                self.print_matrix()
                print("You have no pieces left.\nYOU LOSE!\n")
                print("Computer has " + str(self.computer_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()
            elif self.computer_pieces == 0:
                self.print_matrix()
                print("Computer has no pieces left.\nYOU WIN!")
                print("You have " + str(self.player_pieces) + " points.")
                tf = time.time()
                diff = tf - self.t
                print("Game time: " + str(diff) + " seconds.")
                print("Computer moves: " + str(self.computer_moves))
                print("Player moves: " + str(self.player_moves))
                exit()
            elif self.computer_pieces - self.player_pieces == 7:
                wish = input("You have 7 pieces fewer than your opponent.Do you want to surrender?[yes/no]")
                if wish == "" or wish == "yes":
                    print("You surrended.\n")
                    print("Computer has " + str(self.computer_pieces) + " points.")
                    tf = time.time()
                    diff = tf - self.t
                    print("Game time: " + str(diff) + " seconds.")
                    print("Computer moves: " + str(self.computer_moves))
                    print("Player moves: " + str(self.player_moves))
                    exit()
            self.current_turn = not self.current_turn


if __name__ == '__main__':
    checkers = Checkers()
    checkers.play()

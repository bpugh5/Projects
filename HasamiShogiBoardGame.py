# Author: Blake Pugh
# Date:11/19/2021
# Description: This code simulates a Hasami Shogi board game with movable pieces and features player turns that are
# kept track of with movement checks and capture/win detection. Good luck!

class HasamiShogiGame:
    """
    This class is created to represent the running aspects of the Hasami Shogi game as a whole.
    It includes methods to return the current game state (winner), active player (turn), captured pieces (per player),
    ability to move pieces properly, giving the numerical value for a letter row, giving the player on a particular
    square, and returning the board to be accessible elsewhere.
    """

    def __init__(self):
        """
        This init method creates the board along with the starting player turn (Black), number of pieces captured,
        as well as the winner of the game.
        """
        self._board = ShogiBoard()
        self._player_board = self._board.get_board()
        self._player_turn = "BLACK"
        self._player_red_captured = 0
        self._player_black_captured = 0
        self._game_winner = "UNFINISHED"

    def get_game_state(self):
        """
        This method determines whether the game is won or unfinished by returning the game winner which is altered
        in the make_move function.
        """
        return self._game_winner

    def get_active_player(self):
        """
        This method determines which player's turn it currently is by returning the player turn which is altered
        in the make_move function.
        """
        return self._player_turn

    def get_num_captured_pieces(self, color):
        """
        This method determines how many of a player's pieces have been captured by the color provided when called.
        This is also altered in the make_move function when a piece or pieces are captured.
        """
        if color == "BLACK":
            return self._player_black_captured
        elif color == "RED":
            return self._player_red_captured

    def make_move(self, start, end):
        """
        This method moves a piece from a starting position to the ending position. It checks for any collisions along
        the way, as well as potential capturing opportunities where it lands. Players cannot move when it is
        not their turn, nor when the game is over.
        """
        if self.get_game_state() == "BLACK_WON" or self.get_game_state() == "RED_WON":
            return False

        # Initializes start and end variables
        start_row = self.get_row(start[0])
        start_column = int(start[1])
        square_to_move_from = self._player_board[start_row][start_column]

        end_row = self.get_row(end[0])
        end_column = int(end[1])

        # Checks every index between moves for collisions or overlaps
        if start[0] == end[0]:  # Horizontal movement check
            if end[1] > start[1]:
                for i in range(int(start[1]), int(end[1])):
                    if [end_row, i] != [start_row, start_column]:
                        if self._player_board[end_row][i] == "B" or self._player_board[end_row][i] == "R":
                            return False

            elif start[1] > end[1]:
                for i in range(int(end[1]), int(start[1])):
                    if [end_row, i] != [start_row, start_column]:
                        if self._player_board[end_row][i] == "B" or self._player_board[end_row][i] == "R":
                            return False

        elif start[1] == end[1]:  # Vertical movement check
            if end[0] > start[0]:
                for i in range(start_row, end_row):
                    if [i, end_column] != [start_row, start_column]:
                        if self._player_board[i][end_column] == "B" or self._player_board[i][end_column] == "R":
                            return False

            elif start[0] > end[0]:
                for i in range(end_row, start_row):
                    if [i, end_column] != [start_row, start_column]:
                        if self._player_board[i][end_column] == "B" or self._player_board[i][end_column] == "R":
                            return False

        else:
            return False

        # Player Black's turn
        if self.get_active_player() == "BLACK":
            if square_to_move_from == "B":  # Checks to make sure proper piece is being moved
                self._board.set_board(end_row, end_column, self._player_board[start_row][start_column])
                self._board.set_board(start_row, start_column, ".")  # Moves piece visually

                # Makes sure index won't go off list
                if end_row > 1:
                    if self._player_board[end_row - 1][end_column] == "R":  # capturing upwards
                        row_number = end_row - 1
                        capturable_pieces = []
                        is_capturable = False

                        while self._player_board[row_number][end_column] == "R":
                            if self._player_board[row_number - 1][end_column] == ".":
                                is_capturable = False
                                break

                            if self._player_board[row_number - 1][end_column] == "B":
                                is_capturable = True

                            capturable_pieces.append([row_number, end_column])
                            row_number -= 1

                        if is_capturable is True:
                            for piece in capturable_pieces:
                                self._board.set_board(piece[0], end_column, ".")
                                self._player_red_captured += 1

                if end_row < 9:
                    if self._player_board[end_row + 1][end_column] == "R":  # capturing downwards
                        row_number = end_row + 1
                        capturable_pieces = []
                        is_capturable = False

                        while self._player_board[row_number][end_column] == "R":
                            if self._player_board[row_number + 1][end_column] == ".":
                                is_capturable = False
                                break

                            if self._player_board[row_number + 1][end_column] == "B":
                                is_capturable = True

                            capturable_pieces.append([row_number, end_column])
                            row_number += 1

                        if is_capturable is True:
                            for piece in capturable_pieces:
                                self._board.set_board(piece[0], end_column, ".")
                                self._player_red_captured += 1

                if end_column > 1:
                    if self._player_board[end_row][end_column - 1] == "R":  # capturing left
                        column_number = end_column - 1
                        capturable_pieces = []
                        is_capturable = False

                        while self._player_board[end_row][column_number] == "R":
                            if self._player_board[end_row][column_number - 1] == ".":
                                is_capturable = False
                                break

                            if self._player_board[end_row][column_number - 1] == "B":
                                is_capturable = True

                            capturable_pieces.append([end_row, column_number])
                            column_number -= 1

                        if is_capturable is True:
                            for piece in capturable_pieces:
                                self._board.set_board(end_row, piece[1], ".")
                                self._player_red_captured += 1

                if end_column < 9:
                    if self._player_board[end_row][end_column + 1] == "R":  # capturing right
                        column_number = end_column + 1
                        capturable_pieces = []
                        is_capturable = False

                        while self._player_board[end_row][column_number] == "R":
                            if self._player_board[end_row][column_number + 1] == ".":
                                is_capturable = False
                                break

                            if self._player_board[end_row][column_number + 1] == "B":
                                is_capturable = True

                            capturable_pieces.append([end_row, column_number])
                            column_number += 1

                        if is_capturable is True:
                            for piece in capturable_pieces:
                                self._board.set_board(end_row, piece[1], ".")
                                self._player_red_captured += 1

                # Corner capture checks
                if [end_row, end_column] == [1, 2] and self._player_board[2][1] == "B" \
                        and self._player_board[1][1] == "R" \
                        or [end_row, end_column] == [2, 1] and self._player_board[1][2] == "B" \
                        and self._player_board[1][1] == "R":

                    self._board.set_board(1, 1, ".")
                    self._player_red_captured += 1

                elif [end_row, end_column] == [9, 2] and self._player_board[8][1] == "B" \
                        and self._player_board[9][1] == "R" \
                        or [end_row, end_column] == [8, 1] and self._player_board[9][2] == "B" \
                        and self._player_board[9][1] == "R":
                    self._board.set_board(9, 1, ".")
                    self._player_red_captured += 1

                elif [end_row, end_column] == [1, 8] and self._player_board[2][9] == "B" \
                        and self._player_board[1][9] == "R" \
                        or [end_row, end_column] == [2, 9] and self._player_board[1][8] == "B" \
                        and self._player_board[1][9] == "R":
                    self._board.set_board(1, 9, ".")
                    self._player_red_captured += 1

                elif [end_row, end_column] == [8, 9] and self._player_board[9][8] == "B" \
                        and self._player_board[9][9] == "R" \
                        or [end_row, end_column] == [9, 8] and self._player_board[8][9] == "B" \
                        and self._player_board[9][9] == "R":
                    self._board.set_board(9, 9, ".")
                    self._player_red_captured += 1
            else:
                return False

            self._player_turn = "RED"
            if self._player_red_captured >= 8:
                self._game_winner = "BLACK_WON"
                self._player_turn = None
            return True

        if self.get_active_player() == "RED":
            if square_to_move_from == "R":
                self._board.set_board(end_row, end_column, self._player_board[start_row][start_column])
                self._board.set_board(start_row, start_column, ".")

                if end_row > 1:
                    if self._player_board[end_row - 1][end_column] == "B":  # up
                        row_number = end_row - 1
                        capturable_pieces = []
                        is_capturable = False

                        while self._player_board[row_number][end_column] == "B":
                            if self._player_board[row_number - 1][end_column] == ".":
                                is_capturable = False
                                break

                            if self._player_board[row_number - 1][end_column] == "R":
                                is_capturable = True

                            capturable_pieces.append([row_number, end_column])
                            row_number -= 1

                        if is_capturable is True:
                            for piece in capturable_pieces:
                                self._player_board[piece[0]][end_column] = "."
                                self._player_black_captured += 1

                if end_row < 9:
                    if self._player_board[end_row + 1][end_column]:  # down
                        row_number = end_row + 1
                        capturable_pieces = []
                        is_capturable = False
                        while self._player_board[row_number][end_column] == "B":
                            if self._player_board[row_number + 1][end_column] == ".":
                                is_capturable = False
                                break
                            if self._player_board[row_number + 1][end_column] == "R":
                                is_capturable = True
                            capturable_pieces.append([row_number, end_column])
                            row_number += 1
                        if is_capturable is True:
                            for piece in capturable_pieces:
                                self._player_board[piece[0]][end_column] = "."
                                self._player_black_captured += 1

                if end_column > 1:
                    if self._player_board[end_row][end_column - 1]:  # left
                        column_number = end_column - 1
                        capturable_pieces = []
                        is_capturable = False
                        while self._player_board[end_row][column_number] == "B":
                            if self._player_board[end_row][column_number - 1] == ".":
                                is_capturable = False
                                break
                            if self._player_board[end_row][column_number - 1] == "R":
                                is_capturable = True
                            capturable_pieces.append([end_row, column_number])
                            column_number -= 1
                        if is_capturable is True:
                            for piece in capturable_pieces:
                                self._player_board[end_row][piece[1]] = "."
                                self._player_black_captured += 1

                if end_column < 9:
                    if self._player_board[end_row][end_column + 1]:  # right
                        column_number = end_column + 1
                        capturable_pieces = []
                        is_capturable = False
                        while self._player_board[end_row][column_number] == "B":
                            if self._player_board[end_row][column_number + 1] == ".":
                                is_capturable = False
                                break
                            if self._player_board[end_row][column_number + 1] == "R":
                                is_capturable = True
                            capturable_pieces.append([end_row, column_number])
                            column_number += 1
                        if is_capturable is True:
                            for piece in capturable_pieces:
                                self._player_board[end_row][piece[1]] = "."
                                self._player_black_captured += 1

                # Corner capture checks
                if [end_row, end_column] == [1, 2] and self._player_board[2][1] == "R" \
                        and self._player_board[1][1] == "B" \
                        or [end_row, end_column] == [2, 1] and self._player_board[1][2] == "R" \
                        and self._player_board[1][1] == "B":

                    self._board.set_board(1, 1, ".")
                    self._player_black_captured += 1

                elif [end_row, end_column] == [9, 2] and self._player_board[8][1] == "R" \
                        and self._player_board[9][1] == "B" \
                        or [end_row, end_column] == [8, 1] and self._player_board[9][2] == "R" \
                        and self._player_board[9][1] == "B":
                    self._board.set_board(9, 1, ".")
                    self._player_black_captured += 1

                elif [end_row, end_column] == [1, 8] and self._player_board[2][9] == "R" \
                        and self._player_board[1][9] == "B" \
                        or [end_row, end_column] == [2, 9] and self._player_board[1][8] == "R" \
                        and self._player_board[1][9] == "B":
                    self._board.set_board(1, 9, ".")
                    self._player_black_captured += 1

                elif [end_row, end_column] == [8, 9] and self._player_board[9][8] == "R" \
                        and self._player_board[9][9] == "B" \
                        or [end_row, end_column] == [9, 8] and self._player_board[8][9] == "R" \
                        and self._player_board[9][9] == "B":
                    self._board.set_board(9, 9, ".")
                    self._player_black_captured += 1
            else:
                return False

            self._player_turn = "BLACK"
            if self._player_black_captured >= 8:
                self._game_winner = "RED_WON"
                self._player_turn = None
            return True

    def get_row(self, char):
        """
        This method determines the numerical match to a particular row's letter for iteration.
        """
        if char == "a":
            return 1
        if char == "b":
            return 2
        if char == "c":
            return 3
        if char == "d":
            return 4
        if char == "e":
            return 5
        if char == "f":
            return 6
        if char == "g":
            return 7
        if char == "h":
            return 8
        if char == "i":
            return 9

    def get_square_occupant(self, square):

        """
        This method returns the player occupying a particular square that is provided in the SQUARE
        parameter (if there is one) otherwise it will return none
        """
        if self._player_board[self.get_row(square[0])][int(square[1])] == 'B':
            return "BLACK"
        elif self._player_board[self.get_row(square[0])][int(square[1])] == 'R':
            return "RED"
        else:
            return "NONE"


class ShogiBoard:
    def __init__(self):
        """
        This init method will hard code the board into a list of lists so that the starting positions of
        both players can be set every time the game resets
        """
        self._begin_board = [
            [" ", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            ["a", "R", "R", "R", "R", "R", "R", "R", "R", "R"],
            ["b", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["c", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["d", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["e", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["f", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["g", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["h", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["i", "B", "B", "B", "B", "B", "B", "B", "B", "B"]]

    def set_board(self, row, col, set_value):
        """
        This set method changes a specific index given by the parameters ROW and COL which are the
        indices passed to find where they want to change and what they want to set it to (passed
        by the SET_VALUE parameter)
        """
        self._begin_board[row][col] = set_value

    def build_board(self):
        """
        This method is simply for printing purposes and proper formatting, returns each list in the list of lists
        with spaces in between to make a perfect board.
        """

        board_string = ""
        for i in range(len(self._begin_board)):
            for o in range(len(self._begin_board[i])):
                board_string += (self._begin_board[i][o])
            board_string += "\n"
        print(board_string)

    def get_board(self):
        """
        This get method is meant to return the beginning board for initialization of the game once
        it first starts, used by the init method of the HasamiShogiGame class.
        """
        return self._begin_board

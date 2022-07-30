import copy

from gui import Chess_gui

class Position:
    initial_board = (
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    )
    figure = {
        " ": " ",
        "r": "♜",
        "n": "♞",
        "b": "♝",
        "q": "♛",
        "k": "♚",
        "p": "♟",
        "R": "♖",
        "N": "♘",
        "B": "♗",
        "Q": "♕",
        "K": "♔",
        "P": "♙",
    }

    def __init__(
        self,
        board=initial_board,
        white_to_move=True,
        en_passant=None,
        castling_rights=["both", "both"],
    ):
        self.board = board
        self.white_to_move = white_to_move
        self.en_passant = en_passant
        self.castling_rights = castling_rights

    def at(self, coords):
        return self.board[coords[0]][coords[1]]

    def move(self, move): #move: (old_row, old_col, new_row, new_col)
        self.en_passant = (
            move[1]
            if (
                self.at(move).lower() == "p"
                and move[0] == (6 if self.white_to_move else 1)
                and move[2] == (4 if self.white_to_move else 3)
            )
            else None
        )
        if self.at(move).lower() == "p":
            f = -1 if self.white_to_move else 1  # pawn's forward direction

            if move[1] != move[3] and self.at((move[2], move[3])) == " ":
                # en passant capture
                self.board[move[2] - f][move[3]] = " "
            if move[2] in (0, 7):
                self.board[move[2]][move[3]] = move[4]
                self.board[move[0]][move[1]] = " "
                self.white_to_move = not self.white_to_move
                return

        kings_rank = 7 if self.white_to_move else 0
        if self.at(move).lower() == "k":
            self.castling_rights[0 if self.white_to_move else 1] = "none"
            if abs(move[3] - move[1]) > 1:  # Castling
                self.castling_rights[0 if self.white_to_move else 1] = None
                self.board[kings_rank][0 if move[3] - move[1] < 0 else 7] = " "
                self.board[kings_rank][3 if move[3] - move[1] < 0 else 5] = (
                    "R" if self.white_to_move else "r"
                )
        if self.at(move).lower() == "r":
            if move[0] == kings_rank:
                if move[1] == 0:
                    self.castling_rights[0 if self.white_to_move else 1] = (
                        "kingside"
                        if self.castling_rights[0 if self.white_to_move else 1]
                        == "both"
                        else "none"
                    )
                if move[1] == 7:
                    self.castling_rights[0 if self.white_to_move else 1] = (
                        "queenside"
                        if self.castling_rights[0 if self.white_to_move else 1]
                        == "both"
                        else "none"
                    )
        self.board[move[2]][move[3]] = self.board[move[0]][move[1]]
        self.board[move[0]][move[1]] = " "
        self.white_to_move = not self.white_to_move

    def attacks(self):
        moves = []
        e_p = self.en_passant
        white_to_move = self.white_to_move
        f = -1 if self.white_to_move else 1  # Pawn's forward direction
        if e_p is not None:
            attacker_rank = 3 if white_to_move else 4 
            attacker = "P" if white_to_move else "p"
            if e_p > 0 and self.board[attacker_rank][e_p - 1] == attacker:
                moves.append((attacker_rank, e_p - 1, attacker_rank + f, e_p))
            if e_p < 7 and self.board[attacker_rank][e_p + 1] == attacker:
                moves.append((attacker_rank, e_p + 1, attacker_rank + f, e_p))

        for i, rank in enumerate(self.board):
            for j, square in enumerate(rank):
                if square != " " and square.isupper() == white_to_move:
                    if square.lower() == "p":  # Pawn moves
                        if self.board[i + f][j] == " ":  # single push
                            if i + f in (0, 7):  # Promotion
                                for piece in ["r", "n", "b", "q"]:
                                    p = piece.upper() if white_to_move else piece
                                    moves.append((i, j, i + f, j, p))
                            else:
                                moves.append((i, j, i + f, j))
                            if i == (6 if white_to_move else 1):  # double push
                                if self.board[i + 2 * f][j] == " ":
                                    moves.append((i, j, i + 2 * f, j))
                        if j > 0:  # capture to the left
                            target = self.board[i + f][j - 1]
                            if target != " " and target.islower() == white_to_move:
                                if i + f in (0, 7):  # Promotion
                                    for piece in ["r", "n", "b", "q"]:
                                        p = piece.upper() if white_to_move else piece
                                        moves.append((i, j, i + f, j - 1, p))
                                else:
                                    moves.append((i, j, i + f, j - 1))
                        if j < 7:  # capture to the right
                            target = self.board[i + f][j + 1]
                            if target != " " and target.islower() == white_to_move:
                                if i + f in (0, 7):  # Promotion
                                    for piece in ["r", "n", "b", "q"]:
                                        p = piece.upper() if white_to_move else piece
                                        moves.append((i, j, i + f, j + 1, p))
                                else:
                                    moves.append((i, j, i + f, j + 1))
                    if square.lower() == "n":  # Knight moves
                        # fmt: off
                        jumps = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
                        # fmt: on
                        for jump in jumps:
                            if 0 <= i + jump[0] < 8 and 0 <= j + jump[1] < 8:
                                target = self.board[i + jump[0]][j + jump[1]]
                                if target == " " or target.islower() == white_to_move:
                                    moves.append((i, j, i + jump[0], j + jump[1]))
                    if square.lower() == "b":  # Bishop moves
                        moves.extend(self.straight_moves(i, j, True))
                    if square.lower() == "r":  # Rook moves
                        moves.extend(self.straight_moves(i, j))
                    if square.lower() == "q":  # Queen moves
                        moves.extend(self.straight_moves(i, j, True))
                        moves.extend(self.straight_moves(i, j))
                    if square.lower() == "k":  # King moves
                        moves.extend(self.king_moves(i, j))

        return moves


    def moves(self):
        return [m for m in self.attacks() if not self.suicidal(m)]


    def straight_moves(self, i, j, bishop=False):
        s_moves = []
        directions = (
            ((-1, -1), (-1, 1), (1, -1), (1, 1))
            if bishop
            else ((-1, 0), (0, -1), (0, 1), (1, 0))
        )
        for d in directions:
            curr_i = i 
            curr_j = j
            while (
                0 <= (curr_i := curr_i + d[0]) < 8
                and 0 <= (curr_j := curr_j + d[1]) < 8
            ):
                if self.board[curr_i][curr_j] == " ":
                    s_moves.append((i, j, curr_i, curr_j))
                elif self.board[curr_i][curr_j].islower() == self.white_to_move:
                    s_moves.append((i, j, curr_i, curr_j))
                    break
                else:
                    break
        return s_moves


    def king_moves(self, i, j):
        king_moves = []
        directions = (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        )
        for d in directions:
            if 0 <= i + d[0] < 8 and 0 <= j + d[1] < 8:
                if (
                    self.board[i + d[0]][j + d[1]] == " "
                    or self.board[i + d[0]][j + d[1]].islower() == self.white_to_move
                ):
                    king_moves.append((i, j, i + d[0], j + d[1]))
        side = 0 if self.white_to_move else 1
        if self.castling_rights[side] in ["both", "queenside"] and self.can_castle(
            "queenside"
        ):
            king_moves.append((i, j, 7 if self.white_to_move else 0, 2))
        if self.castling_rights[side] in ["both", "kingside"] and self.can_castle(
            "kingside"
        ):
            king_moves.append((i, j, 7 if self.white_to_move else 0, 6))

        return king_moves


    def can_castle(self, side):
        kings_rank = 7 if self.white_to_move else 0
        # There can't be pieces between king and rook
        for j in range(*((1, 4) if side == "queenside" else (5, 7))):
            if self.board[kings_rank][j] != " ":
                return False
        # No square between can be attacked
        # We create hypothetical boards with the king moved and look for checks
        for j in range(*((1, 4) if side == "queenside" else (5, 7))):
            hyp = copy.deepcopy(self)
            hyp.move((kings_rank, 4, kings_rank, j))
            if hyp.king_attacked():
                return False
        return True


    def in_check(self):
        tmp = copy.deepcopy(self)
        tmp.white_to_move = not tmp.white_to_move
        return tmp.king_attacked()


    def king_attacked(self):
        for m in self.attacks():
            if self.board[m[2]][m[3]].lower() == "k":
                return True
        return False


    def suicidal(self, move):
        tmp = copy.deepcopy(self)
        tmp.move(move)
        return tmp.king_attacked()


    def print(self, color=False, unicode=False, clear=False):
        COLOR1 = "\33[46m"
        COLOR2 = "\33[44m"
        RESET = "\33[m"
        if clear:
            print("\33[2J\33[H")
        print("  ", end="")
        for j in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            print(j, end=" ")
        print()
        for i, rank in enumerate(self.board):
            print(8 - i, end=" ")
            for j, square in enumerate(rank):
                if color:
                    print(COLOR2 if (i + j) % 2 else COLOR1, end="")
                print(self.figure[square] if unicode else square, "", end="")
            print(RESET, 8 - i)
        print("  ", end="")
        for j in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            print(j, end=" ")


def quasismith_to_index(x):
    a = list(x)
    return (8 - int(a[1]), letter_to_idx[a[0]], 8 - int(a[3]), letter_to_idx[a[2]])


def index_to_quasismith(x):
    return "".join(
        (idx_to_letter[x[1]], str(8 - x[0]), idx_to_letter[x[3]], str(8 - x[2]))
    )


def index_to_algebraic(moves, move):
    dest_file = idx_to_letter[move[3]]
    dest_rank = str(8 - move[2])
    dest = "".join((dest_file, dest_rank))
    ambiguous = [
        m
        for m in moves
        if m[0:4] != move[0:4]  # ignore promotions
        and m[2] == move[2]
        and m[3] == move[3]
        and position.at(m) == position.at(move)
    ]
    piece = "" if position.at(move).lower() == "p" else position.at(move).upper()
    promotion = "" if len(move) == 4 else move[4].upper()
    if not ambiguous:
        return "".join((piece, dest, promotion))
    else:
        file_ambiguous = [m for m in ambiguous if m[1] == move[1]]
        if not file_ambiguous:
            return "".join((piece, idx_to_letter[move[1]], dest, promotion))
        else:
            rank_ambiguous = [m for m in ambiguous if m[0] == move[0]]
            if not rank_ambiguous:
                return "".join((piece, str(8 - move[0]), dest, promotion))
            else:
                return "".join(
                    (piece, str(8 - move[0]), idx_to_letter[move[1]], dest, promotion)
                )


def index_to_quasismith(x):
    return "".join(
        (idx_to_letter[x[1]], str(8 - x[0]), idx_to_letter[x[3]], str(8 - x[2]))
    )


letter_to_idx = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
idx_to_letter = dict((v, k) for k, v in letter_to_idx.items())

position = Position()
gui = Chess_gui(position.board)

while True:
    position.print(color=True, unicode=True, clear=True)
    moves = position.moves()
    if moves:
        print("\nAvailable moves: \n", end=" ")
        notation_to_move = dict([(index_to_algebraic(moves, x), x) for x in moves])
        for x in notation_to_move:
            print(x, end=" ")
    else:
        if position.in_check():
            print("Checkmate")
        else:
            print("Stalemate")
        exit()
    print("\nWhite to move:" if position.white_to_move else "\nBlack to move:", end=" ")
    while True:
        player_input = gui.get_input(position.board)
        if player_input == (-1,-1,-1,-1):
            exit(0)
        if player_input in moves:
            
            position.move(player_input)
            gui.refresh_board(position.board)
            break
        print("your move was", player_input)
        print("Illegal move, try again. Legal moves: ",moves)
        
    print()

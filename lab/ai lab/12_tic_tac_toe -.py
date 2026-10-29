
import math

WIN_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8),      # rows
             (0, 3, 6), (1, 4, 7), (2, 5, 8),      # columns
             (0, 4, 8), (2, 4, 6)]                 # diagonals
HUMAN, COMPUTER = "X", "O"


def print_board(board):
    print()
    for i in range(0, 9, 3):
        print(" " + " | ".join(board[i:i + 3]))
        if i < 6:
            print("---+---+---")
    print()


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return " " not in board


def minimax(board, is_computer_turn, alpha, beta):
    """Return score: +1 computer wins, -1 human wins, 0 draw."""
    w = winner(board)
    if w == COMPUTER:
        return 1
    if w == HUMAN:
        return -1
    if is_full(board):
        return 0

    if is_computer_turn:                         # maximiser
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = COMPUTER
                best = max(best, minimax(board, False, alpha, beta))
                board[i] = " "
                alpha = max(alpha, best)
                if beta <= alpha:                # prune
                    break
        return best
    else:                                        # minimiser
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = HUMAN
                best = min(best, minimax(board, True, alpha, beta))
                board[i] = " "
                beta = min(beta, best)
                if beta <= alpha:                # prune
                    break
        return best


def best_move(board):
    best_score, move = -math.inf, None
    for i in range(9):
        if board[i] == " ":
            board[i] = COMPUTER
            score = minimax(board, False, -math.inf, math.inf)
            board[i] = " "
            if score > best_score:
                best_score, move = score, i
    return move


def human_move(board):
    while True:
        try:
            choice = int(input("Your move (1-9): "))
        except ValueError:
            print("Please type a number between 1 and 9.")
            continue
        if not 1 <= choice <= 9:
            print("Number must be between 1 and 9.")
        elif board[choice - 1] != " ":
            print("That square is already taken.")
        else:
            return choice - 1


def play():
    board = [" "] * 9
    first = input("Do you want to play first? (y/n): ").strip().lower()
    human_turn = first.startswith("y")
    print(f"\nYou are {HUMAN}, the computer is {COMPUTER}.")
    print_board(board)

    while True:
        if human_turn:
            board[human_move(board)] = HUMAN
        else:
            move = best_move(board)
            board[move] = COMPUTER
            print(f"Computer plays at position {move + 1}")
        print_board(board)

        w = winner(board)
        if w:
            print("Congratulations, you win!" if w == HUMAN else "Computer wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break
        human_turn = not human_turn


if __name__ == "__main__":
    print("TIC TAC TOE - HUMAN vs COMPUTER (Minimax with Alpha-Beta pruning)")
    while True:
        play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if not again.startswith("y"):
            print("Thank you for playing!")
            break

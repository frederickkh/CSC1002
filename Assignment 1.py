import random

# Creates a global dictionary to store user custom key for moves 
# {"LEFT": None, "RIGHT": None, "UP": None, "DOWN": None}
moves = {key: None for key in ["LEFT", "RIGHT", "UP", "DOWN"]}
# Initiate a global list for the answer board
answer_board = []


def prompt_assign_keys():
    # Asks user for custom keys for moves and assigns them to the moves dictionary.
    #
    # return: None

    # Repeat until the user input is valid
    while True:
        try:
            keys = input("Enter four letters used for left, right, up, and down move > ")
            
            keys = keys.lower()  # Lowercase the whole string to make case-insensitive
            keys = keys.strip()  # Remove leading and trailing whitespaces

            length = len(keys)
            keys_list = []

            # Extract keys from keys string into keys_list.
            i = 0
            while i < length:
                if keys[i].isspace():
                    i += 1
                    continue
                j = i + 1
                if i == length-1 and not keys[i].isspace():
                    key = keys[i]
                    keys_list.append(key)
                else:
                    while j < length:
                        if keys[j].isspace():
                            key = keys[i:j]
                            keys_list.append(key)
                            break
                        elif j == length - 1:
                            key = keys[i:]
                            keys_list.append(key)
                            break
                        j += 1
                i = j + 1
            
            # Validate the keys inside keys_list.
            # They are valid if:
            # 1. There are exactly 4 keys.
            # 2. Each key is a single alphabet letter.
            # 3. Each key is different from one another.
            valid = True
            length = len(keys_list)
            if length != 4:
                valid = False  # Input is invalid if there are more than 4 keys
            else:
                for key in keys_list:
                    if not key.isalpha() or len(key) != 1:
                        valid = False  # Input is invalid if a key is not an alphabet or is not a single character
                        break
                # Check for duplicates; input is invalid if there are any duplicates.
                for i in range(length):
                    for j in range(i+1, length):
                        if keys_list[i] == keys_list[j]:
                            valid = False
                            break
                    if not valid:
                        break
        except Exception:
            # Warn user if the input produces any kind of error and ask again.
            print("Invalid input. Please enter only four different letters each separated by a space.")
        else:
            # If the input is valid, break out of the loop. Otherwise, warn and ask again.
            if valid:
                break
            else:
                print("Invalid input. Please enter only four different letters each separated by a space.")
                continue
    
    # Assign each letter to corresponding move.
    index = 0
    for key in ["LEFT", "RIGHT", "UP", "DOWN"]:
        moves[key] = keys_list[index]
        index += 1


def prompt_dim_or_end():
    # Asks user input for the choice of board dimension or quit game and returns the choice.
    #
    # return: string containing the choice, either "1", "2", or "q"

    # Repeat until user input is valid
    while True:
        try:
            choice = input('Enter "1" for 8-puzzle, "2" for 15-puzzle, or "q" to end the game > ')
            choice = choice.lower()  # Lowercase the string input to be case-insensitive
            choice = choice.strip()  # Remove leading and trailing whitespaces
            if choice not in ("1", "2", "q"):
                # Warn user if the input is other than "1", "2", or "q" and ask again.
                print('Invalid input. Please enter either "1", "2", or "q" only.')
                continue
        except Exception:
            # Warn user if the input produces any kind of error and ask again.
            print('Invalid input. Please enter either "1", "2", or "q" only.')
        else:
            break

    return choice


def get_blank_pos(p_board):
    # Returns the position of the blank tile.
    #
    # param p_board (list): the game board  
    # return: (y, x) tuple where the blank tile is in the y-th row and x-th column

    dim = len(p_board)
    # Go through each element and find the element containing 0 which is the blank tile.
    for y in range(dim):
        for x in range(dim):
            if p_board[y][x] == 0:
                return (y, x)


def is_valid_move(p_board, p_move):
    # Checks whether the move given is a valid move in the given board.
    #
    # param p_board (list): the game board
    # param p_move (str): the move to be checked
    # return: Boolean (True if the move is valid, False if the move is invalid)

    blank_y, blank_x = get_blank_pos(p_board)  # Get the index position of the blank tile
    if p_move == moves["LEFT"] and blank_x == len(p_board[0]) - 1:
        return False  # Left move is not available if the blank tile is at the right-most column
    elif p_move == moves["RIGHT"] and blank_x == 0:
        return False  # Right move is not available if the blank tile is at the left-most column
    elif p_move == moves["UP"] and blank_y == len(p_board) - 1:
        return False  # Up move is not available if the blank tile is at the bottom-most row
    elif p_move == moves["DOWN"] and blank_y == 0:
        return False  # Down move is not available if the blank tile is at the top-most row
    else:
        return True


def valid_moves_prompt(p_board):
    # Generates the prompt for the user input for the next move.
    #
    # param p_board (list): the game board
    # return: string containing the prompt, e.g. "Enter your move (left-a, right-d, up-w, down-s) > "

    # Create a string of the choices of possible moves.
    prompt = "Enter your move ("
    num = 0
    if is_valid_move(p_board, moves["LEFT"]):
        prompt += f"left-{moves['LEFT']}"
        num += 1
    if is_valid_move(p_board, moves["RIGHT"]):
        if num > 0:
            prompt += ", "  # Add comma in between if there are more than one possible moves
        prompt += f"right-{moves['RIGHT']}"
        num += 1
    if is_valid_move(p_board, moves["UP"]):
        if num > 0:
            prompt += ", "
        prompt += f"up-{moves['UP']}"
        num += 1
    if is_valid_move(p_board, moves["DOWN"]):
        if num > 0:
            prompt += ", "
        prompt += f"down-{moves['DOWN']}"
        num += 1
    prompt += ") > "

    return prompt


def prompt_moves(p_board):
    # Asks user input for the next move.
    #
    # param p_board (list): the game board
    # return: string containing the letter corresponding to a move

    prompt = valid_moves_prompt(p_board)  # Get the prompt containing valid moves for current board
    keys = []

    # Get a list of keys of valid moves.
    for move in moves.values():
        if is_valid_move(p_board, move):
            keys.append(move)

    # Repeat until user input is valid.
    while True:
        try:
            move = input(prompt)  # Asks user for a move
            move = move.lower()  # Lowercase the string input to be case-insensitive
            move = move.strip()  # Remove leading and trailing whitespaces
            if move not in keys:
                # Warn user if the move is not among the choices of valid moves and ask again.
                print("Invalid input. The move is not available. Please enter again.")
                continue
        except Exception:
            # Warn user if the input produces any kind of error and ask again.
            print("Invalid input. Please enter again.")
        else:
            break
    
    return move


def get_initial_board(p_dim):
    # Generates the answer board, i.e. all elements are in the correct place
    #
    # param p_dim (int): the side dimension of the board, e.g. p_dim = 3 corresponds to a 3x3 board
    # return: a list which is the answer board, e.g. [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    # Initiate the board and counter
    board = []
    counter = 1

    # Make the board which is a list consisting of p_dim amount of row lists.
    for i in range(p_dim):
        # Make a list for each row, consisting of p_dim amount of consecutive numbers.
        row = []
        for j in range(p_dim):
            if i == (p_dim - 1) and j == (p_dim - 1):
                row.append(0)  # The very last element (bottom-right-most) will be 0
            else:
                row.append(counter)
            counter += 1  
        board.append(row)
    
    return board


def get_new_puzzle(p_dim):
    # Generates a new random game board.
    #
    # param p_dim (int): the dimension for the board
    # return: a list which is a random game board, e.g. [[2, 0, 6], [4, 8, 3], [5, 1, 7]]

    board = []  # Initiates a list for the game board
    elements = list(range(1, p_dim*p_dim)) + [0]  # Initiates a list [1, ..., p_dim*p_dim, 0]
    
    # Make the board which is a list consisting of p_dim amount of row lists.
    for _ in range(p_dim):
        row = []
        # Make a list for each row, consisting of p_dim amount of random element from elements list.
        for _ in range(p_dim):
            element = random.choice(elements)
            row.append(element)
            elements.remove(element)  # Remove appended element from the elements list so it won't be chosen again
        board.append(row)
    
    return board


def nested_to_linear_list(p_list):
    # Converts a nested list into a standard list.
    # e.g. [[1, 2, 3], [4, 5, 6], [7, 8, 0]] -> [1, 2, 3, 4, 5, 6, 7, 8, 0]
    #
    # param p_list (list): a nested list
    # return: a list which has been converted

    dim = len(p_list)
    linear_list = []

    # Iterate through every element in p_list and directly append to linear_list.
    for i in range(dim):
        for j in range(dim):
            linear_list.append(p_list[i][j])
    
    return linear_list


def count_inv(p_list):
    # An inversion is any pair of tiles i and j where i < j but i appears after j.
    #
    # param p_list (list): the list to be calculated
    # return: an integer (number of inversions)

    inversions = 0
    length = len(p_list)
    for i in range(length-1):
        for j in range(i, length):
            if p_list[i] != 0 and p_list[j] != 0 and p_list[i] > p_list[j]:
                inversions += 1
    
    return inversions


def is_solvable(p_board):
    # Checks if the board is solvable.
    # If the board is in odd dimension (e.g. 3x3), it is solvable if the number of inversions is even.
    # If the board is in even dimension (e.g. 4x4), it is solvable if 
    # a. the blank is on an even row counting from the bottom (second-last, fourth-last, etc.) 
    #    and number of inversions is odd, OR
    # b. the blank is on an odd row counting from the bottom (last, third-last, fifth-last, etc.) 
    #    and number of inversions is even.
    #
    # param p_board (list): the game board to be checked
    # return: Boolean (True if the board is solvable, False if the board is not solvable)

    list_board = nested_to_linear_list(p_board)  # Converts p_board into a linear list    
    inversions = count_inv(list_board)  # Calculate the number of inversions
    
    # Get the row index of the blank tile from bottom.
    dim = len(p_board)
    blank_pos = get_blank_pos(p_board)
    blank_row_bottom = dim - blank_pos[0]

    if dim % 2 == 1:
        # Judge solvability for odd-dim board
        if inversions % 2 == 0:
            return True
        else:
            return False
    else:
        # Judge solvability for even-dim board
        if inversions % 2 == 1 and blank_row_bottom % 2 == 0:
            return True
        elif inversions % 2 == 0 and blank_row_bottom % 2 == 1:
            return True
        else:
            return False


def move_tile(p_board, p_move):
    # Moves the tile on the board based on the move given by user.
    #
    # param p_board (list): the game board
    # param p_move (str): the letter user inputted corresponding to a move
    # return: None

    blank_y, blank_x = get_blank_pos(p_board)  # Get the index position of the blank tile (y-th row, x-th column)
    if is_valid_move(p_board, p_move):
        if p_move == moves["LEFT"]:
            # If move is left, swap the blank tile with the element on the right
            p_board[blank_y][blank_x] = p_board[blank_y][blank_x + 1]
            p_board[blank_y][blank_x + 1] = 0 
        elif p_move == moves["RIGHT"]:
            # If move is right, swap the blank tile with the element on the left
            p_board[blank_y][blank_x] = p_board[blank_y][blank_x - 1]
            p_board[blank_y][blank_x - 1] = 0
        elif p_move == moves["UP"]:
            # If move is up, swap the blank tile with the element below it
            p_board[blank_y][blank_x] = p_board[blank_y + 1][blank_x]
            p_board[blank_y + 1][blank_x] = 0
        elif p_move == moves["DOWN"]:
            # If move is down, swap the blank tile with the element on top of it
            p_board[blank_y][blank_x] = p_board[blank_y - 1][blank_x]
            p_board[blank_y - 1][blank_x] = 0


def check_board(p_board):
    # Checks if the current state of the board is equal to the answer board, i.e. solved.
    #
    # param p_board (list): the game board to be checked
    # return: Boolean (True if the board is solved, False if the board is not yet solved)

    return p_board == answer_board


def print_board(p_board):
    # Prints the game board, e.g.
    # 1  2  3
    # 4  5  6
    # 7  8   
    #
    # param p_board (list): the board to be printed
    # return: None

    dim = len(p_board)  # Get the dimension of the board
    # Print the board
    for i in range(dim):
        for j in range(dim):
            if p_board[i][j] == 0:
                print("  ", end=" ") # The blank tile is represented by an empty space
            else:
                print("%-2s" %(p_board[i][j]), end=" ")
        print()


def main():
    global answer_board

    # Print brief introduction of the game.
    print("Welcome to Sliding Puzzle game!")
    print("In this game, you will try to rearrange a randomized puzzle by sliding tiles into the blank tile until it becomes in order.")
    print("There are two choices of game: 8-puzzle (3x3 grid) and 15-puzzle (4x4 grid).")
    print("You may choose your own distinct keys for left, right, up, and down move.")
    print("Let's start the game!")
    print("Firstly, choose your keys for your move, four distinct letters each separated by a space.")
    
    # Prompt user for keys input
    prompt_assign_keys()

    # Repeat until user quits the game
    while True:
        # Prompt user to select board dimension or quit the game.
        choice = prompt_dim_or_end()
        if choice == "q":
            break # User quits the game
        elif choice == "1":
            dim = 3  # Set the dimension of board to 3, creating a 3x3 game board (8-puzzle)
        else:
            dim = 4  # Set the dimension of board to 4, creating a 4x4 game board (15-puzzle)

        answer_board = get_initial_board(dim)  # Generate the answer board

        # Generate and print the game board
        current_board = get_new_puzzle(dim)
        while not is_solvable(current_board):
            current_board = get_new_puzzle(dim)  # Generate a new puzzle if the previous puzzle is not solvable
        print_board(current_board)

        num_steps = 0  # Number of steps taken by user

        # Repeat until board is solved
        while True:
            if check_board(current_board):
                break  # Break out of the loop if current_board is solved
            move = prompt_moves(current_board)
            move_tile(current_board, move)  # Do the tile move
            print_board(current_board)  # Display current_board after doing the move
            num_steps += 1

        # Print the final statement with the total number of steps done.
        print(f"Congratulations! You solved the puzzle in {num_steps} moves!")
    
    # Statement after user quits the game
    print("Thank you for playing!")


main()

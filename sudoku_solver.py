import tkinter as tk  


# create the main window of the gui
root = tk.Tk()
root.title('Sudoku Solver')
root.geometry('250x280')

# create a weight for each row and column
for i in range(9):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# create the 9 x 9 grid of entry widgets for the sudoku board
initial_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

entries = [[None] * 9 for _ in range(9)]

def build_widget(initial_board):
    for i in range(9):
        for j in range(9):
            value = initial_board[i][j]
            entry = tk.Entry(root, width=2, font=('arial', 14), justify='center')
            entry.grid(row=i, column=j)

            # Set the initial value for the entry widget
            if value != 0:  
                entry.insert(0, str(value))
            
            # store a reference to each entry widget
            entries[i][j] = entry  

build_widget(initial_board)

# get the current state of the puzzle from the GUI
def get_board_state():
    board_state = []
    for i in range(9):
        row_values = [int(entry.get() or 0) for entry in entries[i]]
        board_state.append(row_values)
    return board_state

# find the empty space in the sudoku board
def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

# check whether a specific number can be used for specific dimensions
def valid_cell(board, num, pos):

    row, col = pos 

    # check if all row elements include this number
    for j in range (9):
        if board [row][j] == num:
            return False
    
    # check if all column elements include this number
    for i in range (9):
        if board [i][col] == num:
            return False
        
    # check if number is already included in the block
        row_block_start = 3*(row // 3)
        col_block_start = 3*(col // 3)

        row_block_end = row_block_start + 3
        col_block_end = col_block_start + 3
        for i in range(row_block_start, row_block_end):
            for j in range (col_block_start,col_block_end):
                if board [i][j] == num:
                    return False
            
        return True


# implement the backtracking algorithm in order to solve the sudoku board
def solve_sudoku(board,cache):

    blank = find_empty(board)
    if not blank:
        # return an empty list if the board is already solved
        return []  
    else:
        row, col = blank
        for value in range(1, 10):
            if valid_cell(board, value, (row, col)):
                board[row][col] = value
                print (f'Trying {value} at ({row},{col})')
                solution_steps = solve_sudoku(board,cache)
                # backtrack if the current value doesn't lead to a solution
                if not solution_steps:  
                    print(f'Backtracking from ({row},{col})')
                    board[row][col] = 0
                else:
                    return [(row, col, value)] + solution_steps
        # return an empty list if no valid solution is found
        print ('No valid solution found')
        return []


# implementation of the backtracking algorithm in order to solve the sudoku puzzle
def solve_with_cache(board, cache):
    blank = find_empty(board)
    if not blank:
        return True
    else:
        row, col = blank
        for value in range(1, 10):
            if valid_cell(board, value, (row, col)):
                board[row][col] = value
                solution_steps = solve_sudoku(board)
                if solution_steps is not None:
                    return [(row, col, value)] + solution_steps
                # backtrack if the current value doesn't lead to a solution
                board[row][col] = 0 
        return None

    for value in cache[(row,col)]:
        if valid_cell(board, value, blank):
            board[row][col] = value

        if solve_with_cache(board, cache):
                return True

        board[row][col] = 0
    return False

# store in a dictionary the legitimate values for each individual cell
def cache_valid_values(board, i, j):
    cache = dict()
    for i in range (9):
        for i in range (9):
            if board [i][j] == 0:
                cache [(i,j)] = allowed_values(board,i,j)
        return cache 

# determine values that could be possible valid inputs on the board
def allowed_values(board,row,col):

    numbers_list = list()
    for number in range(1, 10):
        found = False
        # check if all row elements include this number
        for j in range(9):
            if board[row][j] == number:
                found = True
                break
        # check if all column elements include this number
        if found:
            continue
        else:
            for i in range(9):
                if board[i][col] == number:
                    found = True
                    break
        # check if the number is already included in the block
        if found:
            continue
        else:
            row_block_start = 3 * (row // 3)
            col_block_start = 3 * (col // 3)
            row_block_end = row_block_start + 3
            col_block_end = col_block_start + 3
            for i in range(row_block_start, row_block_end):
                for j in range(col_block_start, col_block_end):
                    if board[i][j] == number:
                        found = True
                        break
        if not found:
            numbers_list.append(number)
    return numbers_list


# use available info on each row, change the order that each value will be will be 'guessed' by the algorithm 
def order_valid_values(board, cache):
        
        def count_appearance(cache, row_start, col_start, row_end, col_end):
            count = dict()
            for row in range(row_start, row_end):
                for col in range(col_start, col_end):
                    if (row, col) in cache.keys():
                        for value in cache[(row, col)]:
                            if value in count:
                                count[value] += 1
                            else:
                                count[value] = 1
            return cache

        def count_appearance_all_blocks(cache):
            count_appearance_block = [dict() for _ in range(9)]
            for row_block_start in range(0, 9, 3):
                for col_block_start in range(0, 9, 3):
                    row_block_end = row_block_start + 3
                    col_block_end = col_block_start + 3
                    count_appearance_block[(row_block_start // 3) * 3 + col_block_start // 3] = count_appearance(
                        cache, row_block_start, col_block_start, row_block_end, col_block_end
                    )
            return count_appearance_block

        def update_cache_priority(cache, count_appearance_row, count_appearance_col, count_appearance_block):
            cache_priority = dict()
            for row in range(9):
                for col in range(9):
                    temp_list = list()
                    block_number = (row // 3) * 3 + col // 3
                    if (row, col) in cache.keys():
                        for value in cache[(row, col)]:
                            freq = (
                                count_appearance_row[row][value]
                                + count_appearance_col[col][value]
                                + count_appearance_block[block_number][value]
                            )
                            temp_list.append(freq)
                            cache_priority[(row, col)] = temp_list
            return cache_priority

        def set_board_values(cache, count_appearance_row, count_appearance_col, count_appearance_block, board):
            for row in range(9):
                for col in range(9):
                    temp_list = list()
                    block_number = (row // 3) * 3 + col // 3
                    if (row, col) in cache.keys():
                        for value in cache[(row, col)]:
                            if (
                                count_appearance_row[row][value] == 1
                                or count_appearance_col[col][value] == 1
                                or count_appearance_block[block_number][value] == 1
                            ):
                                board[row][col] = value
            return board

        def sort_cache(cache, cache_priority):
            for row in range(9):
                for col in range(9):
                    if (row, col) in cache.keys():
                        cache[(row, col)] = [i for _, i in sorted(zip(cache_priority[(row, col)], cache[(row, col)]))]
            return cache

        def order_valid_values(board, cache):
            count_appearance_row = [dict() for _ in range(9)]
            count_appearance_col = [dict() for _ in range(9)]
            count_appearance_block = count_appearance_all_blocks(cache)

            cache_priority = update_cache_priority(cache, count_appearance_row, count_appearance_col, count_appearance_block)
            cache = sort_cache(cache, cache_priority)

            board = set_board_values(cache, count_appearance_row, count_appearance_col, count_appearance_block, board)

            return cache

# update_gui_with_solution function should be implemented
def update_gui_with_solution(solution_steps):
    for step in solution_steps:
        if step is not None:
            row, col, value = step
            entries[row][col].delete(0, tk.END)
            entries[row][col].insert(0, str(value))
        else:            
            print("No valid solution found for the current configuration.")


# update the GUI with the solution steps
def update_gui(board):
    for i in range(9):
        for j in range(9):
            entry = entries[i][j]
            entry.delete(0, tk.END)
            entry.insert(0, str(board[i][j]))

# solve the sudoku board 
def solve(board):
    print(f"Solving: {board}")
    empty = find_empty(board)
    if not empty:
        # board is solved
        print ('Board solved')
        return True 
    else:
        row, col = empty
        for value in range(1, 10):
            if valid_cell(board, value, (row, col)):
                board[row][col] = value
                if solve(board):
                    # move to the next empty cell
                    return board 
                # backtrack if the current value doesn't lead to a solution
                board[row][col] = 0 
        # no valid value found for the current cell 
        return None 



# final soltution function should call the solving algorithm and update the GUI
def final_solution():
    current_board = get_board_state()
    cache = order_valid_values(current_board, cache_valid_values(current_board, 0, 0))
    solved_board = solve(current_board)
    if solved_board:
        print ('Solved')
        update_gui(solved_board)
    else:
        print("No solution found.")


# solve button
solve_button = tk.Button(root, text='Solve', fg='black', command=final_solution, bg='white',justify='center')
solve_button.grid(row=10, columnspan=9)

root.mainloop()





selected_numbers = []
boards = dict()

def is_bingo(board):
    # Search for row bingo
    for row in board:
        num_correct = 0
        for val in row:
            if val[1] == 'Y':
                num_correct += 1
        if num_correct == 5:
            return True
    for n in range(0, len(board)):
        num_correct = 0
        for row in board:
            if row[n][1] == 'Y':
                num_correct += 1
        if num_correct == 5:
            return True
    return False

with open('./input.txt') as f:
    board_number = 0
    lines = f.readlines()
    selected_numbers = lines[0].strip().split(',')
    board = []
    for n in range(1, len(lines)):
        if len(lines[n].strip()) == 0:
            if len(board) > 0:
                final_board = []
                for row in board:
                    new_row = []
                    for val in row:
                        new_row.append([int(val), 'N'])
                    final_board.append(new_row)
                boards[board_number] = final_board
            board_number += 1
            board = []
        else:
            board.append(lines[n].strip().split())
    if len(board) > 0:
        final_board = []
        for row in board:
            new_row = []
            for val in row:
                new_row.append([int(val), 'N'])
            final_board.append(new_row)
        boards[board_number] = final_board

for num in selected_numbers:
    for board in boards:
        for row in boards[board]:
            for val in row:
                if val[0] == int(num):
                    val[1] = 'Y'
    # Do we have a bingo?
    for board in boards:
        if is_bingo(boards[board]):
        
            print(f"bingo on board {board} with final number of {int(num)}")
            sum_unmarked = 0
            for row in boards[board]:
                for val in row:
                    if val[1] == 'N':
                        sum_unmarked += val[0]
            print(f"sum of unmarked = {sum_unmarked}")
            print(f"score = {sum_unmarked * int(num)}")
            exit()
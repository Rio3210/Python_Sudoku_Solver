import pygame
import time

from constant import reset_board

# Sudoku board
board = [
    [0,2,0,0,0,0,0,0,0],
    [0,0,0,6,0,0,0,0,3],
    [0,7,4,0,8,0,0,0,0],
    [0,0,0,0,0,3,0,0,2],
    [0,8,0,0,4,0,0,1,0],
    [6,0,0,5,0,0,0,0,0],
    [0,0,0,0,1,0,7,8,0],
    [5,0,0,0,0,9,0,0,0],
    [0,0,0,0,0,0,0,4,0]
]
# board = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]


# Pygame colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_SIZE = (500, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sudoku Solver")

# Set the font
font = pygame.font.Font(None, 40)

# Set the cell size
CELL_SIZE = 50

# Set the margin
MARGIN = 20

# Function to draw the Sudoku board
def draw_board():
    screen.fill(BLACK)
    
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, WHITE)
                screen.blit(text, (MARGIN + j * CELL_SIZE + 15, MARGIN + i * CELL_SIZE + 5))
    
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(screen, WHITE, (MARGIN, MARGIN + i * CELL_SIZE), (MARGIN + 9 * CELL_SIZE, MARGIN + i * CELL_SIZE), 3)
            pygame.draw.line(screen, WHITE, (MARGIN + i * CELL_SIZE, MARGIN), (MARGIN + i * CELL_SIZE, MARGIN + 9 * CELL_SIZE), 3)
        else:
            pygame.draw.line(screen, WHITE, (MARGIN, MARGIN + i * CELL_SIZE), (MARGIN + 9 * CELL_SIZE, MARGIN + i * CELL_SIZE), 1)
            pygame.draw.line(screen, WHITE, (MARGIN + i * CELL_SIZE, MARGIN), (MARGIN + i * CELL_SIZE, MARGIN + 9 * CELL_SIZE), 1)

# Function to find an empty cell in the Sudoku board
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None

# Function to solve the Sudoku board
def solve_sudoku():
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            draw_board()
            pygame.display.update()
            time.sleep(0.1)

            if solve_sudoku():
                return True

            board[row][col] = 0
            draw_board()
            pygame.display.update()
            time.sleep(0.1)

    return False
def solve_sudo():
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve_sudo():
                return True

            board[row][col] = 0

    return False

def solve_and_render():
    if solve_sudo():
        draw_board()
        pygame.display.update()
    else:
        print("No solution exists for this Sudoku board.")


# Function to check if a value is valid in a Sudoku board
def valid(board, num, pos):
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True
def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def display_time(screen, time):
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (255, 255, 255))
    screen.blit(text, (500 - 260, 520))

    
def reset_b():
    global board
    board = reset_board()
    
    
# Main function
def main():
    # Main game loop
    running = True
    selected = None
    start = time.time()

    while running:
        play_time = round(time.time() - start)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_row = (pos[1] - MARGIN) // CELL_SIZE
                clicked_col = (pos[0] - MARGIN) // CELL_SIZE
                if MARGIN < pos[0] < MARGIN + 9 * CELL_SIZE and MARGIN < pos[1] < MARGIN + 9 * CELL_SIZE:
                    selected = (clicked_row, clicked_col)
                else:
                    selected = None

            if event.type == pygame.KEYDOWN:
                if selected:
                    row, col = selected
                    if event.unicode.isdigit() and board[row][col] == 0:
                        num = int(event.unicode)
                        if valid(board, num, (row, col)):
                            board[row][col] = num
                            draw_board()
                            pygame.display.update()
                        else:
                            print("Wrong")
                    elif event.key == pygame.K_DELETE and board[row][col] == 0:
                        board[row][col] = 0
                        draw_board()
                        pygame.display.update()
                if event.key == pygame.K_r:  # Press 'R' key to reset the board
                    reset_b()
                if event.key == pygame.K_SPACE:
                    solve_and_render()

        draw_board()
        display_time(screen,play_time)
        pygame.display.update()

    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()

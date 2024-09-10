import pygame
from constants import BLOCK_SIZE, ROWS, COLUMNS, BLACK


# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

def create_empty_grid():
    """Creates an empty grid for the Tetris game."""
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def is_valid_position(grid, tetromino, offset):
    """Checks if the tetromino can be placed at the given offset."""
    x_offset, y_offset = offset
    for y, row in enumerate(tetromino):
        for x, cell in enumerate(row):
            if cell:
                new_x = x + x_offset
                new_y = y + y_offset
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return False  # Out of bounds
                if grid[new_y][new_x]:
                    return False  # Collides with existing blocks
    return True

def lock_tetromino(grid, tetromino, offset):
    """Locks the tetromino in the grid."""
    x_offset, y_offset = offset
    for y, row in enumerate(tetromino):
        for x, cell in enumerate(row):
            if cell:
                grid[y + y_offset][x + x_offset] = 1

def clear_full_rows(grid):
    """Clears full rows and returns the new grid and number of lines cleared."""
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = GRID_HEIGHT - len(new_grid)
    new_grid = [[0] * GRID_WIDTH for _ in range(lines_cleared)] + new_grid
    return new_grid, lines_cleared

def rotate_tetromino(tetromino):
    """Rotates the tetromino 90 degrees clockwise."""
    return [list(row) for row in zip(*tetromino[::-1])]

def draw_grid(screen, grid):
    """Draws the grid on the Pygame screen."""
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, (0, 0, 0),
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_tetromino(screen, tetromino, offset, color):
    """Draws the current tetromino on the Pygame screen."""
    x_offset, y_offset = offset
    for y, row in enumerate(tetromino):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color,
                                 ((x + x_offset) * BLOCK_SIZE, (y + y_offset) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, (0, 0, 0),
                                 ((x + x_offset) * BLOCK_SIZE, (y + y_offset) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_scoreboard(screen, score):
    """Draws the score on the Pygame screen."""
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def check_collision(grid, tetromino, offset=(0, 0)):
    shape = tetromino.image()
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, value in enumerate(row):
            if value:
                if x + tetromino.x + off_x < 0 or x + tetromino.x + off_x >= COLUMNS:
                    return True
                if y + tetromino.y + off_y >= ROWS:
                    return True
                if grid[y + tetromino.y + off_y][x + tetromino.x + off_x]:
                    return True
    return False

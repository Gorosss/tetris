import pygame
import random
from utils import (
    create_empty_grid, draw_grid, draw_tetromino, draw_scoreboard,
    is_valid_position, lock_tetromino, clear_full_rows, rotate_tetromino, check_collision
)

from constants import SHAPES, COLORS, COLUMNS


SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
FPS = 60
FONT_SIZE = 24

TETROMINO_SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]]
}

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()

    grid = create_empty_grid()
    score = 0
    current_tetromino = random.choice(list(TETROMINO_SHAPES.values()))
    color = random.choice(list(COLORS))

    tetromino_offset = [GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0]
    fall_time = 0
    level_speed = 50
    running = True

    def check_game_over():
        """Check if the game is over."""
        for x in range(GRID_WIDTH):
            if grid[0][x] != 0:
                return True
        return False

    while running:
        screen.fill((0, 0, 0))  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    rotated_tetromino = rotate_tetromino(current_tetromino)
                    if is_valid_position(grid, rotated_tetromino, tetromino_offset):
                        current_tetromino = rotated_tetromino
                if event.key == pygame.K_RIGHT:
                    tetromino_offset[0] += 1
                    if not is_valid_position(grid, current_tetromino, tetromino_offset):
                        tetromino_offset[0] -= 1
                if event.key == pygame.K_LEFT:
                    tetromino_offset[0] -= 1
                    if not is_valid_position(grid, current_tetromino, tetromino_offset):
                        tetromino_offset[0] += 1



        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_DOWN]:
            tetromino_offset[1] += 1
            if not is_valid_position(grid, current_tetromino, tetromino_offset):
                tetromino_offset[1] -= 1
                lock_tetromino(grid, current_tetromino, tetromino_offset)
                grid, lines_cleared = clear_full_rows(grid)
                score += lines_cleared * 100
                current_tetromino = random.choice(list(TETROMINO_SHAPES.values()))
                tetromino_offset = [GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0]
                color = random.choice(list(COLORS))
                if check_game_over():
                    running = False


        fall_time += clock.get_rawtime()
        clock.tick()  
        if fall_time >= level_speed:
            fall_time = 0
            tetromino_offset[1] += 1
            if not is_valid_position(grid, current_tetromino, tetromino_offset):
                tetromino_offset[1] -= 1
                lock_tetromino(grid, current_tetromino, tetromino_offset)
                grid, lines_cleared = clear_full_rows(grid)
                score += lines_cleared * 100
                current_tetromino = random.choice(list(TETROMINO_SHAPES.values()))

                tetromino_offset = [GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0]
                

                if check_game_over():
                    running = False

        draw_grid(screen, grid)
        draw_tetromino(screen, current_tetromino, tetromino_offset, color)
        draw_scoreboard(screen, score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()

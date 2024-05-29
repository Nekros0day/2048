import pygame
import random

# Initialize the pygame
pygame.init()

# Constants
SIZE = WIDTH, HEIGHT = 400, 450  # Increased height for the score bar
TILE_SIZE = WIDTH // 4
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
FONT_COLOR = (119, 110, 101)
FONT = pygame.font.Font(None, 50)
SCORE_FONT = pygame.font.Font(None, 36)
ANIMATION_SPEED = 45  # Speed of tile movement in pixels per frame
FPS = 60  # Frames per second

# Initialize screen
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('2048')

class Tile:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y

    def set_position(self, x, y):
        self.target_x = x
        self.target_y = y

    def update_position(self):
        # Move towards the target position each frame
        if self.x < self.target_x:
            self.x = min(self.x + ANIMATION_SPEED, self.target_x)
        elif self.x > self.target_x:
            self.x = max(self.x - ANIMATION_SPEED, self.target_x)
        
        if self.y < self.target_y:
            self.y = min(self.y + ANIMATION_SPEED, self.target_y)
        elif self.y > self.target_y:
            self.y = max(self.y - ANIMATION_SPEED, self.target_y)

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, get_tile_color(self.value), rect)
        if self.value != 0:
            text = FONT.render(str(self.value), True, FONT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)

def initialize_game():
    board = [[None] * 4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] is None]
    if not empty_cells:
        return
    i, j = random.choice(empty_cells)
    value = 2 if random.random() < 0.9 else 4
    board[i][j] = Tile(value, j * TILE_SIZE, i * TILE_SIZE + 50)

def get_tile_color(value):
    if value in TILE_COLORS:
        return TILE_COLORS[value]
    return (60, 58, 50)

def draw_board(board, score):
    screen.fill(BACKGROUND_COLOR)
    # Draw score
    score_text = SCORE_FONT.render(f"Score: {score}", True, FONT_COLOR)
    screen.blit(score_text, (10, 10))
    
    for row in board:
        for tile in row:
            if tile is not None:
                tile.draw(screen)
    pygame.display.flip()

def move_left(row):
    new_row = [tile for tile in row if tile is not None]
    for i in range(len(new_row) - 1):
        if new_row[i] is not None and new_row[i + 1] is not None and new_row[i].value == new_row[i + 1].value:
            new_row[i].value *= 2
            new_row[i + 1] = None
    new_row = [tile for tile in new_row if tile is not None]
    while len(new_row) < 4:
        new_row.append(None)
    return new_row

def transpose(board):
    return [list(row) for row in zip(*board)]

def reverse(board):
    return [list(reversed(row)) for row in board]

def set_tile_positions(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] is not None:
                board[i][j].set_position(j * TILE_SIZE, i * TILE_SIZE + 50)

def move(board, direction):
    if direction == 'UP':
        board = transpose(board)
        new_board = [move_left(row) for row in board]
        board = transpose(new_board)
    elif direction == 'DOWN':
        board = transpose(board)
        new_board = reverse([move_left(row) for row in reverse(board)])
        board = transpose(new_board)
    elif direction == 'LEFT':
        new_board = [move_left(row) for row in board]
        board = new_board
    elif direction == 'RIGHT':
        new_board = reverse([move_left(row) for row in reverse(board)])
        board = new_board
    set_tile_positions(board)
    return board

def boards_are_equal(board1, board2):
    return all((board1[i][j] is None and board2[i][j] is None) or 
               (board1[i][j] is not None and board2[i][j] is not None and board1[i][j].value == board2[i][j].value)
               for i in range(4) for j in range(4))

def game_over(board):
    for row in board:
        if any(tile is None for tile in row):
            return False
    for i in range(4):
        for j in range(3):
            if board[i][j] is not None and board[i][j + 1] is not None and board[i][j].value == board[i][j + 1].value:
                return False
            if board[j][i] is not None and board[j + 1][i] is not None and board[j][i].value == board[j + 1][i].value:
                return False
    return True

def calculate_score(board):
    return sum(tile.value for row in board for tile in row if tile is not None)

def main():
    board = initialize_game()
    score = calculate_score(board)
    draw_board(board, score)
    
    running = True
    clock = pygame.time.Clock()

    while running:
        previous_board = [row[:] for row in board]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    new_board = move(board, 'UP')
                elif event.key == pygame.K_s:
                    new_board = move(board, 'DOWN')
                elif event.key == pygame.K_a:
                    new_board = move(board, 'LEFT')
                elif event.key == pygame.K_d:
                    new_board = move(board, 'RIGHT')
                else:
                    new_board = board

                if not boards_are_equal(board, new_board):
                    board = new_board
                    add_new_tile(board)
                    score = calculate_score(board)
        
        # Update tile positions
        for row in board:
            for tile in row:
                if tile is not None:
                    tile.update_position()

        draw_board(board, score)
        pygame.display.flip()
        clock.tick(FPS)

        if game_over(board):
            print("Game Over!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()

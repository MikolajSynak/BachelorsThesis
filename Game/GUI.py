# PyGame
import pygame
from Engine import Game
from Engine import Player


pygame.init()
pygame.font.init()
pygame.display.set_caption("Battleship")
FONT = pygame.font.SysFont("fresansttf", 75)

# Global variables
SQUARE_SIZE = 55
HORIZONTAL_MARGIN = SQUARE_SIZE * 4
VERTICAL_MARGIN = SQUARE_SIZE
WIDTH = SQUARE_SIZE * 10 * 2 + HORIZONTAL_MARGIN
HEIGHT = SQUARE_SIZE * 10 * 2 + VERTICAL_MARGIN
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
INDENT = 10

HUMAN1 = False
HUMAN2 = False


# Colors
BLACK = (0, 0, 0)
GREY = (40, 60, 80)
WHITE = (255, 250, 250)
GREEN = (50, 200, 150)
BLUE = (50, 150, 200)
ORANGE = (250, 140, 20)
RED = (250, 50, 100)
COLORS = {"U": GREY, "M": BLUE, "H": ORANGE, "S": RED}


# Function to draw a grid
def draw_grid(player, left=0, top=0, search=False):
    for i in range(100):
        x = left + i % 10 * SQUARE_SIZE
        y = top + i // 10 * SQUARE_SIZE
        square = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width=3)
        if search:
            x += SQUARE_SIZE // 2
            y += SQUARE_SIZE // 2
            pygame.draw.circle(SCREEN, COLORS[player.search[i]], (x,y), radius=SQUARE_SIZE//4)


# Function to draw ships onto position grids
def draw_ships(player, left=0, top=0):
    for ship in player.ships:
        x = left + ship.col * SQUARE_SIZE + INDENT
        y = top + ship.row * SQUARE_SIZE + INDENT
        if ship.orientation == 'H':
            width = ship.size * SQUARE_SIZE - 2 * INDENT
            height = SQUARE_SIZE - 2 * INDENT
        else:
            width = SQUARE_SIZE - 2 * INDENT
            height = ship.size * SQUARE_SIZE - 2 * INDENT
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, GREEN, rectangle, border_radius=15)


game = Game(HUMAN1, HUMAN2)

# Pygame Loop
animating = True
pausing = False


while animating:

    # Track user interaction
    for event in pygame.event.get():

        # User closes PyGame window
        if event.type == pygame.QUIT:
            animating = False

        # User clicks on mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if not game.over and game.player1_turn and x < SQUARE_SIZE*10 and y < SQUARE_SIZE*10:
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                index = row * 10 + col
                game.make_move(index)
            elif not game.over and not game.player1_turn and x > WIDTH - SQUARE_SIZE*10 and y > SQUARE_SIZE*10 + VERTICAL_MARGIN:
                row = (y - SQUARE_SIZE*10 - VERTICAL_MARGIN) // SQUARE_SIZE
                col = (x - SQUARE_SIZE*10 - HORIZONTAL_MARGIN) // SQUARE_SIZE
                index = row * 10 + col
                game.make_move(index)

        # User presses key on keyboard
        if event.type == pygame.KEYDOWN:

            # escape key to close the animation
            if event.key == pygame.K_ESCAPE:
                animating = False

            # space bar to pause and unpause the animation, "not pausing" so it works both ways
            if event.key == pygame.K_SPACE:
                pausing = not pausing

            # Return key to restart the game
            if event.key == pygame.K_RETURN:
                game = Game(HUMAN1, HUMAN2)

    # Execution
    if not pausing:
        # Draw background
        SCREEN.fill(GREY)

        # Draw search grid
        draw_grid(game.player1, search=True)
        draw_grid(game.player2, search=True, left=(WIDTH - HORIZONTAL_MARGIN) // 2 + HORIZONTAL_MARGIN, top=(HEIGHT - VERTICAL_MARGIN) // 2 + VERTICAL_MARGIN)

        # Draw position grids
        draw_grid(game.player1, top=(HEIGHT - VERTICAL_MARGIN) // 2 + VERTICAL_MARGIN)
        draw_grid(game.player2, left=(WIDTH - HORIZONTAL_MARGIN) // 2 + HORIZONTAL_MARGIN)

        # Draw ships onto position grids
        draw_ships(game.player1, top=(HEIGHT - VERTICAL_MARGIN) // 2 + VERTICAL_MARGIN)
        draw_ships(game.player2, left=(WIDTH - HORIZONTAL_MARGIN) // 2 + HORIZONTAL_MARGIN)

        # Computer moves
        if not game.over and game.computer_turn:
            game.random_ai()

        # Game over message
        if game.over:
            text = "Player " + str(game.result) + " wins!"
            textbox = FONT.render(text, False, BLACK, WHITE)
            SCREEN.blit(textbox, (WIDTH//2 - 240, HEIGHT//2 - 50))
        # Update screen
        pygame.time.wait(0)
        pygame.display.flip()

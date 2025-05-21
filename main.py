import random
import pygame
import time
import numpy as np


# Constants
WIDTH = 720  # Maze Width
HEIGHT = 720  # Maze Height
SIDE_BAR_HEIGHT = 48  # Side Bar Height

N_ITERATION = 1000  # Number of mazes the agent will solve before stopping
WALL_CHANGE_COEFF = 10  # Number of walls changed after each agent's move
INITIAL_WALL_CHANGE = 2000  # Number of walls changed while generating the initial maze
TICKS = 20  # Speed of executing the code

C_SIZE = 72  # Size of 1 cell of the maze
N_ROW = HEIGHT // C_SIZE  # Number of rows in the maze
N_COL = WIDTH // C_SIZE  # Number of columns in the maze

random.seed("Potter")  # Randomness Seed

# Initializing PyGame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + SIDE_BAR_HEIGHT))
pygame.display.set_caption("Dynamic Maze")

# Setting up
clock = pygame.time.Clock()
running = True

step_counts = []
nodes_expanded = []

# Colors
WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
RED = (150, 30, 30)
GREEN = (30, 150, 30)

# Fonts
pygame.font.init()
font16 = pygame.font.SysFont("menlo", 16)
font32 = pygame.font.SysFont("luminari", 32)
font64 = pygame.font.SysFont("luminari", 64)


# Game Manager
class GameManager:
    def __init__(self):
        self.state = "Menu"

        self.grid = [[Cell(row, col) for col in range(N_COL)] for row in range(N_ROW)]

        self.origin = self.grid[-1][-1]
        self.player = self.grid[0][0]
        self.goal = self.grid[-1][-1]

        self.start = False
        self.method = None
        self.show_indicator = False

        self.step_count = 0
        self.iteration = 0
        self.nodes_expanded = 0

        self.path = []

        self.initialize_maze()

    def initialize_maze(self):
        for row in range(N_ROW):
            for col in range(N_COL):
                if col != N_COL - 1:
                    self.grid[row][col].direction = "R"
                elif row != N_ROW - 1:
                    self.grid[row][col].direction = "D"

    def change_borders(self, n=1):
        # Changes borders n times

        for _ in range(n):
            direction = None
            nxt_origin = None

            while not nxt_origin:
                direction = random.choice(["U", "D", "L", "R"])

                nxt_origin = self.origin.get_neighbour(direction)

            self.origin.direction = direction
            nxt_origin.direction = None
            self.origin = nxt_origin

    @staticmethod
    def get_available_moves(cell):
        directions = ["U", "L", "D", "R"]  # order matters
        moves = []

        for direction in directions:
            if cell.direction == direction:
                moves.append(direction)
                continue

            neighbour = cell.get_neighbour(direction)
            inverse_direction = directions[(directions.index(direction) + 2) % 4]
            if neighbour and neighbour.direction == inverse_direction:
                moves.append(direction)

        return moves

    def move_player(self, direction=None):
        if not direction:
            direction = self.get_optimal_direction()
        elif direction not in self.get_available_moves(self.player):
            return

        self.player = self.player.get_neighbour(direction)
        self.change_borders(WALL_CHANGE_COEFF)
        self.step_count += 1

        if not self.start and self.player == self.goal:
            self.restart()
            self.start = False

    def get_optimal_direction(self):
        directions = self.get_available_moves(self.player)

        if self.method == "Manhattan":
            directions.sort(key=lambda x: self.get_manhattan_distance(self.player.get_neighbour(x)))

            if len(directions) >= 2:
                first_value = self.get_manhattan_distance(self.player.get_neighbour(directions[0]))
                second_value = self.get_manhattan_distance(self.player.get_neighbour(directions[1]))

                if first_value < second_value:
                    return directions[0]
                else:
                    return random.choice(directions[0:2])
            else:
                return directions[0]
        elif self.method == "A star":
            self.get_a_star_path()
            return max(directions, key=lambda x: self.path[-1] == self.player.get_neighbour(x))
        elif self.method == "D star":
            if self.player in self.path:
                player_ind = self.path.index(self.player)
            else:
                player_ind = 0

            current_direction = max(["U", "D", "R", "L"], key=lambda x: self.path[player_ind-1] == self.player.get_neighbour(x))
            if current_direction not in directions:
                self.get_a_star_path()
                return max(directions, key=lambda x: self.path[-1] == self.player.get_neighbour(x))

            return max(directions, key=lambda x: self.path[player_ind-1] == self.player.get_neighbour(x))
        return None

    def get_manhattan_distance(self, cell):
        return abs(cell.row - self.goal.row) + abs(cell.col - self.goal.col)

    def get_a_star_path(self):
        self.path = []

        frontier = {self.player: 0}
        expanded = []
        came_from = {}

        solved = False

        while not solved:
            current = min(frontier.keys(), key=lambda x: frontier[x] + self.get_manhattan_distance(x))

            if current == self.goal:
                solved = True
            else:
                expanded.append(current)
                self.nodes_expanded += 1

                for direction in self.get_available_moves(current):
                    neighbour = current.get_neighbour(direction)

                    if neighbour not in expanded:
                        if neighbour not in frontier.keys() or frontier[current] + 1 < frontier[neighbour]:
                            frontier[neighbour] = frontier[current] + 1
                            came_from[neighbour] = current

            frontier.pop(current)

        cell = self.goal
        while cell != self.player:
            self.path.append(cell)
            cell = came_from[cell]

    def solve(self):
        self.move_player()

        if self.player == self.goal:
            if self.iteration < N_ITERATION:
                step_counts.append(self.step_count)
                nodes_expanded.append(self.nodes_expanded)

                self.iteration += 1
                self.restart()
            else:
                self.start = False

    def restart(self):
        self.grid = [[Cell(row, col) for col in range(N_COL)] for row in range(N_ROW)]

        self.origin = self.grid[-1][-1]
        self.player = self.grid[0][0]
        self.goal = self.grid[-1][-1]

        self.start = True
        self.step_count = 0
        self.nodes_expanded = 0

        self.initialize_maze()
        self.change_borders(INITIAL_WALL_CHANGE)

    def draw(self):
        if self.state == "Maze":
            self.draw_maze()
            self.draw_sidebar()
        elif self.state == "Menu":
            self.draw_menu()

    def draw_maze(self):
        screen.fill(WHITE)
        for row in self.grid:
            for cell in row:
                cell.draw_cell()

    def draw_menu(self):
        screen.fill(WHITE)

        title = font64.render("Dynamic Maze", True, RED)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 4)))

        authors = font16.render("By Mher Beginyan, Sofi Khachatryan, Veronika Khachatryan", True, BLACK)
        screen.blit(authors, authors.get_rect(bottomright=(WIDTH * 0.98, HEIGHT + SIDE_BAR_HEIGHT)))

        subtitle = font32.render("Choose method for visualization", True, BLACK)
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 1 * HEIGHT // 12)))

        manhattan_txt = font32.render("Manhattan Distance", True, BLACK)
        manhattan_rect = manhattan_txt.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 3 * HEIGHT // 12))

        a_star_txt = font32.render("A* with Real Time Updates", True, BLACK)
        a_star_rect = a_star_txt.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 4 * HEIGHT // 12))

        d_star_txt = font32.render("Dynamic A*", True, BLACK)
        d_star_rect = d_star_txt.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 5 * HEIGHT // 12))

        if manhattan_rect.collidepoint(pygame.mouse.get_pos()):
            manhattan_txt = font32.render("Manhattan Distance", True, RED)
            if pygame.mouse.get_pressed(3)[0]:
                self.state = "Maze"
                self.method = "Manhattan"
        if a_star_rect.collidepoint(pygame.mouse.get_pos()):
            a_star_txt = font32.render("A* with Real Time Updates", True, RED)
            if pygame.mouse.get_pressed(3)[0]:
                self.state = "Maze"
                self.method = "A star"
                self.get_a_star_path()
        if d_star_rect.collidepoint(pygame.mouse.get_pos()):
            d_star_txt = font32.render("Dynamic A*", True, RED)
            if pygame.mouse.get_pressed(3)[0]:
                self.state = "Maze"
                self.method = "D star"
                self.get_a_star_path()

        screen.blit(manhattan_txt, manhattan_rect)
        screen.blit(a_star_txt, a_star_rect)
        screen.blit(d_star_txt, d_star_rect)

    def draw_sidebar(self):
        pygame.draw.line(screen, BLACK, (0, HEIGHT), (WIDTH, HEIGHT), 5)

        back_txt = font16.render("Menu", True, BLACK)
        back_rect = back_txt.get_rect(center=(WIDTH // 3, HEIGHT + SIDE_BAR_HEIGHT // 2))

        if not game.start:
            txt = "Start"
        else:
            txt = "Stop"

        start_txt = font16.render(txt, True, BLACK)
        start_rect = start_txt.get_rect(center=(2 * WIDTH // 3, HEIGHT + SIDE_BAR_HEIGHT // 2))

        if back_rect.collidepoint(pygame.mouse.get_pos()):
            back_txt = font16.render("Menu", True, RED)
            if pygame.mouse.get_pressed(3)[0]:
                self.state = "Menu"
                self.start = False
        if start_rect.collidepoint(pygame.mouse.get_pos()):
            start_txt = font16.render(txt, True, RED)
            if pygame.mouse.get_pressed(3)[0]:
                self.start = not self.start
                time.sleep(0.1)

        screen.blit(back_txt, back_rect)
        screen.blit(start_txt, start_rect)


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * C_SIZE
        self.y = row * C_SIZE

        self.direction = None

    def draw_cell(self):
        # Drawing Cell
        pygame.draw.rect(screen, WHITE, (self.x, self.y, C_SIZE, C_SIZE))

        if game.goal == self:
            pygame.draw.rect(screen, GREEN, (self.x, self.y, C_SIZE, C_SIZE))

        if self in game.path and (game.player not in game.path or game.path.index(self) < game.path.index(game.player)):
            pygame.draw.circle(screen, GREEN, (self.x + C_SIZE // 2, self.y + C_SIZE // 2), 5)

        if game.player == self:
            pygame.draw.circle(screen, RED, (self.x + C_SIZE // 2, self.y + C_SIZE // 2), 15)
        elif game.origin == self and game.show_indicator:
            pygame.draw.circle(screen, BLACK, (self.x + C_SIZE // 2, self.y + C_SIZE // 2), 15)

        if self.direction != "U" and self.get_neighbour("U") and self.get_neighbour("U").direction != "D":
            pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x + C_SIZE, self.y), 3)

        if self.direction != "D" and self.get_neighbour("D") and self.get_neighbour("D").direction != "U":
            pygame.draw.line(screen, BLACK, (self.x, self.y + C_SIZE), (self.x + C_SIZE, self.y + C_SIZE), 3)

        if self.direction != "L" and self.get_neighbour("L") and self.get_neighbour("L").direction != "R":
            pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x, self.y + C_SIZE), 3)

        if self.direction != "R" and self.get_neighbour("R") and self.get_neighbour("R").direction != "L":
            pygame.draw.line(screen, BLACK, (self.x + C_SIZE, self.y), (self.x + C_SIZE, self.y + C_SIZE), 3)

    def get_neighbour(self, direction):
        if direction == "U":
            if self.row == 0:
                return None
            return game.grid[self.row - 1][self.col]

        elif direction == "D":
            if self.row == N_ROW - 1:
                return None
            return game.grid[self.row + 1][self.col]

        elif direction == "L":
            if self.col == 0:
                return None
            return game.grid[self.row][self.col - 1]

        elif direction == "R":
            if self.col == N_COL - 1:
                return None
            return game.grid[self.row][self.col + 1]
        return None


game = GameManager()
game.change_borders(INITIAL_WALL_CHANGE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.show_indicator = not game.show_indicator

            if event.key == pygame.K_UP:
                game.move_player("U")
            if event.key == pygame.K_DOWN:
                game.move_player("D")
            if event.key == pygame.K_LEFT:
                game.move_player("L")
            if event.key == pygame.K_RIGHT:
                game.move_player("R")

            if event.key == pygame.K_s:
                game.start = not game.start

    game.draw()

    if game.start:
        game.solve()

    pygame.display.flip()
    clock.tick(TICKS)

pygame.quit()

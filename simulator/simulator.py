import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.select_surf = pygame.image.load('selection.png').convert_alpha()

        self.path = []

    def empty_path(self):
        self.path = []

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // 32
        col = mouse_pos[0] // 32
        current_cell_value = self.matrix[row][col]
        if current_cell_value == 1:
            rect = pygame.Rect((col * 32, row * 32), (32, 32))
            screen.blit(self.select_surf, rect)
        # print(row,col)

    def create_path(self):
        # start
        start_x, start_y = [9,6]
        start = self.grid.node(start_x, start_y)

        mouse_pos = pygame.mouse.get_pos()
        end_x, end_y = mouse_pos[0] // 32, mouse_pos[1] // 32
        end = self.grid.node(end_x, end_y)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = x = point.x * 32 + 16
                y = point.y * 32 + 16
                points.append((x, y))

            pygame.draw.lines(screen, '#3EEBFF', False, points, 5)

    def update(self):
        self.draw_active_cell()
        self.draw_path()

pygame.init()
screen = pygame.display.set_mode((608, 409))
clock = pygame.time.Clock()

bg_surf = pygame.image.load('Frame.png').convert()
matrix = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

pathfinder = Pathfinder(matrix)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pathfinder.create_path()

    screen.blit(bg_surf, (0, 0))
    # pathfinder.draw_active_cell()
    pathfinder.update()

    pygame.display.update()
    clock.tick(60)

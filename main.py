# ----------------------------------------------------
#
# Version       Date           Info
# 1.0           2021      Initial Version
# 
# ----------------------------------------------------

import pygame
from copy import deepcopy
import numpy as np
from numba import njit
# from random import randint

RES = WIDTH, HEIGHT = 1900, 1000
TILE = 5
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 60

pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

next_field = np.array([[0 for _ in range(W)] for _ in range(H)])
current_field = np.array([[1 if not i % 9 else 0 for i in range(W)] for j in range(H)]) # 2,5,8,9,10,11,13,18,21,22,26,30,33,65

# current_field = np.array([[1 if not (j * i // 7) % 5 or j == H // 2 else 0 for i in range(W)] for j in range(H)])
# current_field = np.array([[1 if not(j * i // 3) % 6 else 0 for i in range(W)] for j in range(H)])
# current_field = np.array([[1 if not(j * i // 4) % 2 else 0 for i in range(W)] for j in range(H)])
# current_field = np.array([[1 if not(i % 3) else 0 for i in range(W)] for j in range(H)])
# current_field = np.array([[1 if 1 == i % W else 0 for i in range(W)] for j in range(H)])
# current_field = np.array([[1 if not(i % 5) else 0 for i in range(W)] for j in range(H)])
# current_field = np.array([[1 if i == W // 2 or j == H // 2 else 0 for i in range(W)] for j in range(H)])
# current_field = np.array([[randint(0, 1) for i in range(W)] for j in range(H)])
# current_field = np.array([[1 if not (i * j) % 22 else 0 for i in range(W)] for j in range(H)]) # 5,6,9,22,33
# current_field = np.array([[1 if not i % 7 else randint(0, 1) for i in range(W)] for j in range(H)])

def check_cell(current_field_local, x, y): # без numba
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if current_field_local[j][i]:
                count += 1

    if current_field_local[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 1:
            return 1
        return 0


@njit(fastmath=True)
def check_cell_numba(current_field, next_field): # с numba
    res = []
    for x in range(1, W - 1):
        for y in range(1, H - 1):
            count = 0
            for j in range(y - 1, y + 2):
                for i in range(x - 1, x + 2):
                    if current_field[j][i] == 1:
                        count += 1

            if current_field[y][x] == 1:
                count -= 1
                if count == 2 or count == 3:
                    next_field[y][x] = 1
                    res.append((x, y))
                else:
                    next_field[y][x] = 0
            else:
                if count == 3:
                    next_field[y][x] = 1
                    res.append((x, y))
                else:
                    next_field[y][x] = 0
    return next_field, res


while True:

    surface.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # draw grid
    # [pygame.draw.line(surface, pygame.Color('darkslategray'), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
    # [pygame.draw.line(surface, pygame.Color('darkslategray'), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]
    #
    # draw life
    # for x in range(1, W - 1):
    #   for y in range(1, H - 1):
    #       if current_field[y][x]:
    #           pygame.draw.rect(surface, pygame.Color('forestgreen'), (x * TILE + 2, y * TILE + 2, TILE - 2, TILE - 2))
    #        next_field[y][x] = check_cell(current_field, x, y)

    # draw life numba
    next_field, res = check_cell_numba(current_field, next_field)
    [pygame.draw.rect(surface, pygame.Color('darkorange'),
                      (x * TILE + 1, y * TILE + 1, TILE - 1, TILE - 1)) for x, y in res]

    current_field = deepcopy(next_field)

    pygame.display.flip()
    clock.tick(FPS)

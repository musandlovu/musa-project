import pygame
from pygame.locals import *
import sys
import random


class cube():
   def __init__(self, digit, guess, color, cube_num, width=40, position=40):
       self.digit = digit
       self.color = color
       self.highlighter = (250, 0, 0, 1)
       self.cube_num = cube_num
       self.guess = guess
       self.row = cube_num // 9
       self.column = cube_num % 9
       self.width = width
       self.position = position
       self.x_coord = self.column * self.width + self.position
       self.y_coord = self.row * self.width + self.position
       self.rect_coords = (self.x_coord, self.y_coord, self.width, self.width)
       self.center_coords = (self.x_coord + self.width // 2, self.y_coord + self.width // 2)
       self.is_tapped = False

   def draw_cube(self, surface):
       if self.is_tapped:
           pygame.draw.rect(surface, self.highlighter, self.rect_coords, 3)
       else:
           pygame.draw.rect(surface, self.color, self.rect_coords, 1)

   def draw_upper_left_number(self, surface):
       if self.guess != 0:
           myFont = pygame.font.SysFont("comicsans", 27)
           text = myFont.render(str(self.guess), 1, (0, 0, 0))
           surface.blit(text, (self.x_coord + 2, self.y_coord + 2, self.width, self.width))

   def draw_center_number(self, surface):
       if self.digit != 0:
           myFont = pygame.font.SysFont("comicsans", 40)
           text = myFont.render(str(self.digit), 1, (0, 0, 0))
           text_rect = text.get_rect(center=self.center_coords)
           surface.blit(text, text_rect)


class board():
   def __init__(self, surface, color=(0, 0, 0)):
       self.surface = surface
       self.color = color
       self.cube_array = []
       self.width = 40
       self.position = 40

   def add_cubes(self, sudoku_matrix, guess_matrix):
       for i in range(len(sudoku_matrix)):
           for j in range(len(sudoku_matrix[i])):
               c = cube(sudoku_matrix[i][j], guess_matrix[i][j], self.color, cube_num=9 * i + j)
               self.cube_array.append(c)

   def draw_board(self):
       self.surface.fill((255, 255, 255))
       drawn_hor_line = False
       drawn_vert_line = False

       #drawing vertical thick lines
       pygame.draw.line(self.surface, self.color, (self.position + self.width * 6, self.position),(self.position + self.width * 6, self.position + self.width * 9), 4)
       pygame.draw.line(self.surface, self.color, (self.position + self.width * 3, self.position),(self.position + self.width * 3, self.position + self.width * 9), 4)

       #drawing horizontal thick lines
       pygame.draw.line(self.surface, self.color, (self.position, self.position + self.width * 3),(self.position + self.width * 9, self.position + self.width * 3), 4)
       pygame.draw.line(self.surface, self.color, (self.position, self.position + self.width * 6),(self.position + self.width * 9, self.position + self.width * 6), 4)

       for c in self.cube_array:
           c.draw_cube(self.surface)
           c.draw_center_number(self.surface)
           c.draw_upper_left_number(self.surface)

   def tap_cube(self, position1):
       if position1[0] >= self.position and position1[0] <= self.width * 9 + self.position and position1[1] >= self.position and \
               position1[1] <= self.width * 9 + self.position:
           col = (position1[0] - self.position) // self.width
           row = (position1[1] - self.position) // self.width
           return column + row * 9
       else:
           return 0

   def highlight_cube(self, cube_num):
       for c in self.cube_array:
           if c.cube_number == cube_num:
               c.is_tapped= True
           else:
               c.is_tapped = False


   def change_guess(self, cube_num, new_digit):
       c = self.cube_array[cube_num]
       c.guess = new_digit

   def change_digit(self, cube_num, correct_matrix):
       c = self.cube_array[cube_num]
       if c.guess == correct_matrix[c.row][c.col]:
           c.highlighter = (0, 255, 0)
           c.digit = c.guess
           c.guess = 0
       else:
           c.guess = 0


   def check_digit(self, cube_num, correct_matrix, key):
       c = self.cube_array[cube_num]
       if key == correct_matrix[c.row][c.col]:
           return True
       else:
           return False


def is_valid(matrix, row_num, col_num, digit):
   if valid_box(matrix, row_num, col_num, digit) and valid_col(matrix, col_num, digit) and valid_row(matrix,row_num, digit):
       return True
   else:
       return False


def valid_row(matrix, row_num, digit):
   for i in range(9):
       val = matrix[row_num][i]
       if val == digit:
           return False
   return True


def valid_col(matrix, col_num, value):
   for i in range(9):
       val = matrix[i][col_num]
       if val == value:
           return False
   return True


def valid_box(matrix, row_num, col_num, digit):
   row_num = (row_num // 3) * 3
   col_num = (col_num // 3) * 3
   for i in range(3):
       for j in range(3):
           val = matrix[i + row_num][j + col_num]
           if val == digit:
               return False
   return True


def find_empty(matrix):
   for i in range(9):
       for j in range(9):
           if matrix[i][j] == 0:
               return [i, j]
   return None


def board_finished(matrix):
   for i in range(9):
       for j in range(9):
           if matrix[i][j] == 0:
               return False
   return True


def solve_board(matrix):
   row_col = find_empty(matrix)
   if row_col:
       row_num = row_col[0]
       col_num = row_col[1]
   else:
       return True

   for digit in range(1, 10):
       if is_valid(matrix, row_num, col_num, digit):
           matrix[row_num][col_num] = digit
           if solve_board(matrix):
               return True

           matrix[row_num][col_num] = 0
   return False


def print_board(matrix):
   print('printing board')
   for i in range(len(matrix)):
       print(matrix[i])


sudoku_matrix = [[5, 0, 2, 1, 0, 9, 3, 0, 0],
                [8, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 7, 0, 0, 0, 0, 3, 1],
                [0, 0, 3, 0, 1, 0, 0, 8, 0],
                [9, 0, 0, 8, 6, 3, 0, 0, 5],
                [0, 5, 0, 0, 9, 0, 5, 0, 0],
                [1, 3, 0, 0, 0, 0, 2, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 7, 8],
                [0, 0, 5, 2, 0, 6, 3, 0, 0]]

another_matrix = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                [5, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 7, 0, 0, 0, 0, 3, 1],
                [0, 0, 3, 0, 1, 0, 0, 8, 0],
                [9, 0, 0, 8, 6, 3, 0, 0, 5],
                [0, 5, 0, 0, 9, 0, 6, 0, 0],
                [1, 3, 0, 0, 0, 0, 2, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 7, 4],
                [0, 0, 9, 1, 0, 5, 4, 0, 0]]

solve_board(another_matrix)

guess_matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(9)]

pygame.init()

width = 440
height = 480
surface = pygame.display.set_mode((width, height))

pygame.display.set_caption('Sudoku')
surface.fill((255, 255, 255))

key = None

board = board(surface)
board.add_cubes(sudoku_matrix, guess_matrix)
board.draw_board()

while True:

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           sys.exit()
       elif event.type == pygame.KEYDOWN:
           key = event.key
           if key == pygame.K_1:
               key = 1
           elif key == pygame.K_2:
               key = 2
           elif key == pygame.K_3:
               key = 3
           elif key == pygame.K_4:
               key = 4
           elif key == pygame.K_5:
               key = 5
           elif key == pygame.K_6:
               key = 6
           elif key == pygame.K_7:
               key = 7
           elif key == pygame.K_8:
               key = 8
           elif key == pygame.K_9:
               key = 9
           elif key == pygame.K_RETURN:
               key = 'ENTER'
           else:
               key = None

       if isinstance(key, int):
           board.change_guess(cube_num, key)
           key = None
       if key == 'ENTER':
           board.change_value(cube_num, another_matrix)

       if event.type == pygame.MOUSEBUTTONDOWN:
           position1 = pygame.mouse.get_pos()
           cube_num = board.click_cube(position1)
           if cube_num != 0:
               board.highlight_cube(cube_num)
               key = None

   board.draw_board()
   pygame.display.update()


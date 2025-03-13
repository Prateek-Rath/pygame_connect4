import pygame
import sys
import numpy as np
import time 


# init stuff
pygame.init()
f = 100
screen = pygame.display.set_mode((9*f, 9*f))
pygame.display.set_caption('Connect4')
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)


class TextBox:
    def __init__(self, text):
        self.text = text
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.textbox = self.font.render(f"{text}", True, (255, 255, 255))
        # screen.blit(text, (200, 250))
    def update_tb(self):
        self.textbox = self.font.render(f"{self.text}", True, (255, 255, 255))

class Circle:
    def __init__(self, color, f):
        if color == 'red':
            self.color = (255, 0, 0)
        elif color == 'yellow':
            self.color = (0, 255, 255)
        else:
            self.color = (255, 255, 255)
        self.circle = pygame.Surface((f, f))
        self.circle = self.circle.convert()
        self.circle.fill((0, 0, 0))
        pygame.draw.circle(self.circle, self.color, [f/2, f/2], f/3, 3)
        pygame.draw.line(self.circle, (0, 0, 255), (0,0), (0, f), 3)
        pygame.draw.line(self.circle, (0, 0, 255), (0,0), (f, 0), 3)
        pygame.draw.line(self.circle, (0, 0, 255), (0,f), (f, f), 3)
        pygame.draw.line(self.circle, (0, 0, 255), (f,0), (f, f), 3)
        # pygame.draw.line(screen, (0, 0, 255), (f*1, i*f*1 + 2*f), (8*f, i*f*1 + 2*f))

class EmptyCell:
    def __init__(self, f):
        self.cell = pygame.Surface((f, f))
        self.cell = self.cell.convert()
        self.cell.fill((0, 0, 0))
        pygame.draw.line(self.cell, (0, 0, 255), (0,0), (0, f), 3)
        pygame.draw.line(self.cell, (0, 0, 255), (0,0), (f, 0), 3)
        pygame.draw.line(self.cell, (0, 0, 255), (0,f), (f, f), 3)
        pygame.draw.line(self.cell, (0, 0, 255), (f,0), (f, f), 3)
        

red_circle = Circle('red', f)
yellow_circle = Circle('yellow', f)
white_circle = Circle('white', f)
# exit(0)
red_turn_text = TextBox('Red Turn')
yellow_turn_text = TextBox('Yellow Turn')
empty_cell = EmptyCell(f)


# assume that 0 is red and 1 is yellow


# classes
class Game(object):
    def __init__(self, f):
        self.rows=6
        self.cols=7
        self.grid = np.array([[-1 for j in range(0, self.cols)] for i in range(0,self.rows)])
        # self.grid[5][6] = 1
        print('the shape is', self.grid.shape)
        self.player1 = Player('red')
        self.player2 = Player('yellow')
        self.turn = 0
        self.f = f
        print(self.grid)
        self.winner = -1 # no winner rn
        self.move_count = 0

    def draw_board(self, screen):
        f=self.f
        board_outline = pygame.draw.rect(screen, (0, 0, 255), [1*f, 2*f, 7*f, 6*f], 3)
        #column lines
        for i in range(1, self.cols):
            pygame.draw.line(screen, (0, 0, 255), (i*f*1+1*f, 2*f), (i*f*1+1*f, 8*f), 3)
        #row lines
        for i in range(1, self.rows):
            pygame.draw.line(screen, (0, 0, 255), (f*1, i*f*1 + 2*f), (8*f, i*f*1 + 2*f), 3)
    
    def draw_coins(self, screen):
        for i in range(self.rows):
            for j in range(self.cols):
                # print(self.grid[i][j], end=' ') 
                if self.grid[i][j] == 0:
                    #put a red circle there
                    screen.blit(red_circle.circle, (f+j*f, 2*f+i*f))
                    # screen.blit(white_circle.circle, (f+2*f, 2*f+3*f))
                elif self.grid[i][j] == 1:
                    screen.blit(yellow_circle.circle, (f+j*f, 2*f+i*f))
            # print()
    def dummy_update(self, i, j, color):
        self.grid[i][j] = color
        print(self.grid) 

    def draw_text(self, screen):
        if self.winner != -1:
            if self.winner == 0:
                font1 = pygame.font.Font('freesansbold.ttf', 30)
                textbox = font1.render(f"GAME OVER\n WINNER IS RED", True, (255, 255, 255))
                screen.blit(textbox, (3*f, f/2))
            else:
                font1 = pygame.font.Font('freesansbold.ttf', 30)
                textbox = font1.render(f"GAME OVER\n WINNER IS YELLOW", True, (255, 255, 255))
                screen.blit(textbox, (3*f, f/2))
        elif self.move_count == 42:
            font1 = pygame.font.Font('freesansbold.ttf', 30)
            textbox = font1.render(f"GAME DRAWN", True, (255, 255, 255))
            screen.blit(textbox, (3*f, f/2))
        elif self.turn == 0:
            screen.blit(red_turn_text.textbox, (4*f,f/2))
        else:
            screen.blit(yellow_turn_text.textbox, (4*f,f/2))

    def draw_prompt(self, screen, pos):
        x_cor = pos[0]//f * f
        y_cor = f
        if x_cor < f or x_cor >= 8*f:
            return
        if self.turn == 0:
            screen.blit(red_circle.circle, (x_cor, y_cor))
        else:
            screen.blit(yellow_circle.circle, (x_cor, y_cor))
    
    def remove_prompt(self, screen, pos):
        x_cor = pos[0]//f * f
        y_cor = f
        if x_cor < f or x_cor >= 8*f:
            return
        screen.blit(empty_cell.cell, (x_cor, y_cor))
    
    def move(self, pos):
        x_cor = pos[0]//f * f
        y_cor = f
        if x_cor < f or x_cor >= 8*f:
            return
        col = x_cor//f
        col -= 1 # for 0 indexing
        if col<0 or col > 7:
            return
        # find the highest empty i value in that column
        for i in range(5, -1, -1):
            if self.grid[i][col] == -1:
                self.grid[i][col]=self.turn
                self.turn  = 1 - self.turn
                self.move_count += 1
                break

    def check_winner(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == (1-self.turn):
                    horlen = 0
                    vertlen = 0
                    diag1len = 0
                    diag2len = 0
                    # check vertical
                    for a in range(i-3, i+1):
                        if a < self.rows and a >=0 and self.grid[a][j] == (1 - self.turn):
                            vertlen += 1
                            if vertlen >= 4:
                                print(f'verlen achieved at {i}, {j}')
                                self.winner = 1 - self.turn
                                return self.winner
                        else:
                            vertlen = 0
                    for a in range(i+1, i+4):
                        if a < self.rows and a >=0 and self.grid[a][j] == (1 - self.turn):
                            vertlen += 1
                            if vertlen >= 4:
                                print(f'verlen+ achieved at {i}, {j}')
                                self.winner = 1 - self.turn
                                return self.winner
                        else:
                            vertlen = 0
                    

                    #check horizontal
                    for a in range(j-3, j+1):
                        if a < self.cols and a>=0 and self.grid[i][a] == (1 - self.turn):
                            horlen += 1
                            if  horlen >= 4:
                                print(f'horlen achieved at {i}, {j}')
                                self.winner = 1 - self.turn
                                return self.winner
                        else:
                            horlen = 0
                    
                    for a in range(j+1, j+4):
                        if a < self.cols and a>=0 and self.grid[i][a] == (1 - self.turn):
                            horlen += 1
                            if  horlen >= 4:
                                print(f'horlen+ achieved at {i}, {j}')
                                self.winner = 1 - self.turn
                                return self.winner
                        else:
                            horlen = 0
                    

                    # check diagonal1
                    for a in range(-3,1):
                        if i+a < self.rows and j+a < self.cols and self.grid[i+a][j+a] == (1-self.turn):
                            diag1len += 1
                            if diag1len >=4 :
                                print(f'diag1len achieved at {i}, {j}')
                                self.winner = 1 - self.turn
                                return self.winner
                        else:
                            diag1len = 0
                    
                    for a in range(1,4):
                        if i+a < self.rows and j+a < self.cols and self.grid[i+a][j+a] == (1-self.turn):
                            diag1len += 1
                            if diag1len >=4:
                                print(f'diag1len+ achieved at {i}, {j}')
                                self.winner = 1 - self.turn
                                return self.winner
                        else:
                            diag1len = 0
                    
                    
                    # check diagonal2
                    for a in range(-3,1):
                        if i+a < self.rows and j-a < self.cols and self.grid[i+a][j-a] == (1-self.turn):
                            diag2len += 1
                            if diag2len >= 4:
                                print(f'diag2len achieved at {i}, {j}')
                                self.winner = 1 - self.turn
                                return self.winner
                        else:
                            diag2len = 0
                    for a in range(1,4):
                        if i+a < self.rows and j-a < self.cols and self.grid[i+a][j-a] == (1-self.turn):
                            diag2len += 1
                            if diag2len >= 4:
                                print(f'diag2len+ achieved at {i}, {j}')
                                self.winner = 1 - self.turn
                                return self.winner
                        else:
                            diag2len = 0
        return -1



class Player(object):
    def __init__(self, color):
        self.color = color


# actual code
game = Game(f=f)

clock= pygame.time.Clock()
running = True
prevpos = (-1, -1)
curpos = pygame.mouse.get_pos()
while running:
    screen.fill("black")
    game.draw_board(screen)
    game.draw_coins(screen=screen)
    game.check_winner()
    game.draw_text(screen=screen)
    curpos = pygame.mouse.get_pos()
    game.draw_prompt(screen, curpos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.MOUSEMOTION:
        #     prevpos = curpos
        #     curpos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # print(f'Mouse button {event.button} pressed at {event.pos}')
            game.move(curpos)
            
            pass
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     print(f'Mouse button {event.button} released at {event.pos}')
        prevpos = curpos
        
        # print(f'Mouse moved to {event.pos}')
        pass
    # game.dummy_update(3,4,0)
    
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()






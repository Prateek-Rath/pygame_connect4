import pygame
import sys
class GameObject:

    def __init__(self, image, height, speed):

        self.speed = speed

        self.image = image

        self.pos = image.get_rect().move(0, height)
        print(image.get_rect())
        

    def move(self):

        self.pos = self.pos.move(self.speed, 0)

        if self.pos.right > 600:
            print('voila')
            print(self.pos.left, self.pos.right, self.pos.top, self.pos.bottom)
            self.pos.left = 0
            self.pos.right = 50

    
screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()            #get a pygame clock object

player = pygame.image.load('rocket.png').convert()
player = pygame.transform.scale(player, (50, 50))

background = pygame.image.load('background.png').convert()
screen.blit(background, (0, 0))

objects = []

for x in range(1,2):               

    o = GameObject(player, x*40, 2)

    objects.append(o)

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            sys.exit()

    for o in objects:

        screen.blit(background, o.pos, o.pos)

    for o in objects:

        o.move()

        screen.blit(o.image, o.pos)

    pygame.display.update()

    clock.tick(60)  
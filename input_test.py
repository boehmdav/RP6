import pygame
import time
import sys
import select

#SNES-Controller:
#0 = X
#1 = A
#2 = B
#3 = Y
#4 = 
#5 =
#6 = L
#7 = R
#8 = Select
#9 = Start
#10 =
#11 =
#12 =
#13 =
#14 =
#15 =

if __name__ == "__main__":
    pygame.init()
    gp = pygame.joystick.Joystick(0)
    gp.init()
    
    print(gp.get_numaxes())
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        for i in range(0,gp.get_numaxes()):
            print("%d: %d" %(i,gp.get_axis(i)))
        time.sleep(0.1)

import pygame

print('Setap start')
pygame.init()
window = pygame.display.set_mode(size=(600, 400))
print('Setap End')

print('Loop Start')
while True:
    #check for all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT() # close window
            quit() # end pygame
            

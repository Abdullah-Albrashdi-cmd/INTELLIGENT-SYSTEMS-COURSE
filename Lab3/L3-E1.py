import pygame

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pygame lab3")

clock = pygame.time.Clock()
x,y = 800//2 , 600//2
color = (255,0,0)
w, h = 80 , 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x-= 5
            if event.key == pygame.K_RIGHT:
                x+= 5
            if event.key == pygame.K_UP:
                y-= 5
            if event.key == pygame.K_DOWN:
                y+= 5

    screen.fill((255,255,255))
    pygame.draw.rect(screen, color, (x,y,w,h))
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
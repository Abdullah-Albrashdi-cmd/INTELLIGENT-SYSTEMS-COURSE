import pygame

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pygame lab3")

clock = pygame.time.Clock()
circles = []
left_click = (255,0,0)
right_click = (0,255,0)
cursor= (0,0,255)
follow_redius = 15
radius = 30


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button==1:
                circles.append((pos, left_click, radius))
            if event.button == 3:
                circles.append((pos, right_click, radius))
        elif event.type == pygame.MOUSEWHEEL:
            follow_redius = follow_redius + event.y

            
    screen.fill((255,255,255))

    pos1 = pygame.mouse.get_pos()
    pygame.draw.circle(screen, cursor, pos1, follow_redius)

    for pos, color, radius in circles:
        pygame.draw.circle(screen, color, pos, radius)    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
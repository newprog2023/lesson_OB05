import pygame
pygame.init()

window_size = (1500, 750)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Заголовок главного окна")

image1 = pygame.image.load("image/chelovechek.png")
image_rect1 = image1.get_rect()
image2 = pygame.image.load("image/HP.png")
image_rect2 = image2.get_rect()

speed = 10

run = True

while run:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = pygame.mouse.get_pos()
            image_rect1.x = mouseX-40
            image_rect1.y = mouseY-80


        if keys[pygame.K_a]:
            image_rect2.x -= speed
        if keys[pygame.K_d]:
            image_rect2.x += speed
        if keys[pygame.K_w]:
            image_rect2.y -= speed
        if keys[pygame.K_s]:
            image_rect2.y += speed

    screen.fill((30, 70, 100))
    screen.blit(image1, image_rect1)
    screen.blit(image2, image_rect2)
    pygame.display.flip()

pygame.quit()

import pygame

pygame.init()

# Создание окна
size = width, height = 1280, 720
pygame.display.set_icon(pygame.image.load("data/PngFiles/Other/Small_Icon.png"))
pygame.display.set_caption("BottleField 2")
screen = pygame.display.set_mode(size)

# Игра
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
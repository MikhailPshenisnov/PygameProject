import pygame

pygame.init()

# Создание окна
size = width, height = 1280, 720
pygame.display.set_icon(pygame.image.load("data/PngFiles/Other/Small_Icon.png"))
pygame.display.set_caption("BottleField 2")
screen = pygame.display.set_mode(size)

# Флаги окон
start_window_flag = True
info_window_flag = False
achievements_window_flag = False
first_level_text_flag = False
first_level_flag = False
second_level_text_flag = False
second_level_1_flag = False
second_level_2_flag = False
second_level_3_flag = False
final_window_flag = False

# Игра
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Стартовый экран
    while start_window_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_window_flag = False
        pygame.display.flip()

    # Окно с общей информацией
    while info_window_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                info_window_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_window_flag = True
                    info_window_flag = False
        pygame.display.flip()

    # Окно с достижениями
    while achievements_window_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                achievements_window_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_window_flag = True
                    achievements_window_flag = False
        pygame.display.flip()

    # Обучение для первого уровня
    while first_level_text_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                first_level_text_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    first_level_flag = True
                    first_level_text_flag = False
                elif event.key == pygame.K_ESCAPE:
                    start_window_flag = True
                    first_level_text_flag = False
        pygame.display.flip()

    # Первый уровень
    while first_level_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                first_level_flag = False

            # Временный выход с первого уровня
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                first_level_flag = False
                start_window_flag = True

        pygame.display.flip()

    # Обучение для второго уровня
    while second_level_text_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                second_level_text_flag = False
        pygame.display.flip()

    # Первый этап второго уровня
    while second_level_1_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                second_level_1_flag = False
        pygame.display.flip()

    # Второй этап второго уровня
    while second_level_2_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                second_level_2_flag = False
        pygame.display.flip()

    # Третий этап второго уровня
    while second_level_3_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                second_level_3_flag = False
        pygame.display.flip()

    # Концовка
    while final_window_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                final_window_flag = False
        pygame.display.flip()
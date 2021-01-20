import pygame
from random import choice


# Универсальный класс бутылки (несет лишь информацию об названии и пути до изображения бутылки)
class Bottle:
    def __init__(self, bottle_type, icon_path, half_icon_path):
        self.text = bottle_type
        self.icon_path = icon_path
        self.half_icon_path = half_icon_path


# Класс бутылки V
class VBottle(Bottle):
    def __init__(self):
        super().__init__("V", "data/PngFiles/Bottles/Bottle1.png",
                         "data/PngFiles/Bottles/Bottle11.png")


# Класс бутылки E
class EthanolBottle(Bottle):
    def __init__(self):
        super().__init__("E", "data/PngFiles/Bottles/Bottle2.png",
                         "data/PngFiles/Bottles/Bottle22.png")


# Класс бутылки S
class SolventBottle(Bottle):
    def __init__(self):
        super().__init__("S", "data/PngFiles/Bottles/Bottle3.png",
                         "data/PngFiles/Bottles/Bottle33.png")


# Класс бутылки M
class MedicineBottle(Bottle):
    def __init__(self):
        super().__init__("M", "data/PngFiles/Bottles/Bottle4.png",
                         "data/PngFiles/Bottles/Bottle44.png")


# Класс бутылки, который используется при отсутствии бутылки
class NoBottle(Bottle):
    def __init__(self):
        super().__init__("", "data/PngFiles/Bottles/Bottle5.png",
                         "data/PngFiles/Bottles/Bottle55.png")


# Родительский класс для всех кнопок и прочих спрайтов
class UniversalSprite(pygame.sprite.Sprite):
    def __init__(self, group, image, x, y):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Кнопка "Начать игру" / "Продолжить" (при нажатии запускает 1 уровень если нет сохраненного прогресса,
# запускает уровень (НЕ этап), на котором игрок остановился, если есть сохраненный прогресс)
class PlayButton(UniversalSprite):
    def __init__(self, group, image, x, y):
        super().__init__(group, image, x, y)

    def update(self, *args):
        global first_level_text_flag, start_window_flag, game_progress, second_level_text_flag, \
            pop_sound, first_level_music_name, second_level_music_name
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and start_window_flag:
            if args[0].button == 1:
                pop_sound.play()
                if game_progress == 0:
                    pygame.mixer.music.load(first_level_music_name)
                    pygame.mixer.music.play(-1, 0.0, 1500)
                    start_window_flag = False
                    first_level_text_flag = True
                elif game_progress == 1:
                    pygame.mixer.music.load(second_level_music_name)
                    pygame.mixer.music.play(-1, 0.0, 1500)
                    start_window_flag = False
                    second_level_text_flag = True


# Кнопка "Инфо" (при нажатии запускает окно с общей информацией об игре)
class InfoButton(UniversalSprite):
    def __init__(self, group, image, x, y):
        super().__init__(group, image, x, y)

    def update(self, *args):
        global info_window_flag, start_window_flag, pop_sound
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and start_window_flag:
            if args[0].button == 1:
                pop_sound.play()
                start_window_flag = False
                info_window_flag = True


# Кнопка "Достижения" (при нажатии запускает окно с достижениями)
class AchievementsButton(UniversalSprite):
    def __init__(self, group, image, x, y):
        super().__init__(group, image, x, y)

    def update(self, *args):
        global achievements_window_flag, start_window_flag, pop_sound
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and start_window_flag:
            if args[0].button == 1:
                pop_sound.play()
                start_window_flag = False
                achievements_window_flag = True


# Кнопка "Сбросить прогресс" (при нажатии сбраывает сохранение, но не достижения)
class ResetProgressButton(UniversalSprite):
    def __init__(self, group, image, x, y):
        super().__init__(group, image, x, y)

    def update(self, *args):
        global start_window_flag, game_progress, pop_sound
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and start_window_flag:
            if args[0].button == 1:
                pop_sound.play()
                game_progress = 0
                reset_achievements_flags()
                with open("data/TxtFiles/GameProgress.txt", "w", encoding="utf8") as file:
                    file.write("0")


# Функция для отрисовывания многострочного текста
def draw_text(full_text, screen_name, font1, font2, indent, title_x, title_y,
              text_x, text_y, exit_message_x, exit_message_y):
    text_title = full_text[:2]
    text_text = full_text[2:-1]
    exit_message = full_text[-1:][0]
    # Отрисовывает заголовок текста (первые 2 строчки)
    for string in range(len(text_title)):
        next_string1 = font1.render(text_title[string], True, (255, 255, 255))
        next_string2 = font1.render(text_title[string], True, (0, 0, 0))
        screen_name.blit(next_string2, ((title_x + 2), (title_y + 2) + (indent + 2) * string))
        screen_name.blit(next_string1, (title_x, title_y + (indent + 2) * string))
    # Отрисовывает основной текст
    for string in range(len(text_text)):
        next_string1 = font2.render(text_text[string], True, (255, 255, 255))
        next_string2 = font2.render(text_text[string], True, (0, 0, 0))
        screen_name.blit(next_string2, ((text_x + 2), (text_y + 2) + indent * string))
        screen_name.blit(next_string1, (text_x, text_y + indent * string))
    # Сообщение для выхода с экрана
    next_string1 = font2.render(exit_message, True, (255, 207, 72))
    next_string2 = font2.render(exit_message, True, (0, 0, 0))
    screen_name.blit(next_string2, ((exit_message_x + 2), (exit_message_y + 2)))
    screen_name.blit(next_string1, (exit_message_x, exit_message_y))


# Инициализация pygame.mixer и pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Создание окна
size = width, height = 1280, 720
pygame.display.set_icon(pygame.image.load("data/PngFiles/Other/Small_Icon.png"))
pygame.display.set_caption("BottleField 2")
screen = pygame.display.set_mode(size)

# Задние фоны
start_window_bg = pygame.image.load("data/PngFiles/Windows/StartWindow.png")
info_window_bg = pygame.image.load("data/PngFiles/Windows/UniversalWindow.png")
achievements_window_bg = pygame.image.load("data/PngFiles/Windows/AchievementsWindow.png")
first_level_text_bg = pygame.image.load("data/PngFiles/Windows/UniversalWindow.png")
first_level_bg = pygame.image.load("data/PngFiles/Windows/FirstLevel.png")
game_over_window_bg = pygame.image.load("data/PngFiles/Windows/UniversalWindow.png")
second_level_text_bg = pygame.image.load("data/PngFiles/Windows/UniversalWindow.png")
second_level_bg = pygame.image.load("data/PngFiles/Windows/SecondLevel.png")
final_window_bg = pygame.image.load("data/PngFiles/Windows/UniversalWindow.png")

# Флаги окон
start_window_flag = True
info_window_flag = False
achievements_window_flag = False
first_level_text_flag = False
first_level_flag = False
game_over_window_flag = False
second_level_text_flag = False
second_level_flag = False
final_window_flag = False
credits_window_flag = False

# Прогресс прохождения игры
with open("data/TxtFiles/GameProgress.txt", "r", encoding="utf8") as file:
    game_progress = int(file.read().split("\n")[0])

# Здоровье для 1 уровня
HP = 3

# Список бутылок
bottles_list = [NoBottle(), NoBottle(), NoBottle()]

# Событие для движения конвейера и счетчик для него
CONVEYORTIMER = pygame.USEREVENT + 1
pygame.time.set_timer(CONVEYORTIMER, 200)
first_level_seconds = 0

# Счетик бутылок для 1 уровня
bottles_counter = 0

# Кнопки стартового экрана
start_window_buttons = pygame.sprite.Group()
PlayButton(start_window_buttons, pygame.image.load("data/PngFiles/BigBtn/PlayBtn.png"), 590, 400)
InfoButton(start_window_buttons, pygame.image.load("data/PngFiles/BigBtn/InfoBtn.png"), 700, 400)
AchievementsButton(start_window_buttons, pygame.image.load("data/PngFiles/BigBtn/AchBtn.png"), 480, 400)

# Шрифты
title_font = pygame.font.Font("data/Fonts/19363.ttf", 30)
text_font = pygame.font.Font("data/Fonts/19363.ttf", 20)
very_big_font = pygame.font.Font("data/Fonts/19363.ttf", 120)
small_font = pygame.font.Font("data/Fonts/19363.ttf", 16)

# Тексты
# Основная информация
with open("data/TxtFiles/Info.txt", "r", encoding="utf8") as text:
    info_text = text.read().split("\n")
# Достижения
with open("data/TxtFiles/AchievementsText.txt", "r", encoding="utf8") as text:
    achievements_window_text = text.read().split("\n")
# Обучение для первого уровня
with open("data/TxtFiles/FirstLevelTutorial.txt", "r", encoding="utf8") as text:
    first_level_text = text.read().split("\n")
# Game Over
with open("data/TxtFiles/GameOverText.txt", "r", encoding="utf8") as text:
    game_over_text = text.read().split("\n")
# Обучение для второго уровня
with open("data/TxtFiles/SecondLevelTutorial.txt", "r", encoding="utf8") as text:
    second_level_text = text.read().split("\n")
# Финальное послание
with open("data/TxtFiles/FinalText.txt", "r", encoding="utf8") as text:
    final_window_text = text.read().split("\n")
# Текст титров
with open("data/TxtFiles/CreditsText.txt", "r", encoding="utf8") as text:
    credits_text = text.read().split("\n")

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
            start_window_buttons.update(event)
        screen.blit(start_window_bg, (0, 0))
        start_window_buttons.draw(screen)
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
        screen.blit(info_window_bg, (0, 0))
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
        screen.blit(achievements_window_bg, (0, 0))
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
        screen.blit(first_level_text_bg, (0, 0))
        pygame.display.flip()

    # Первый уровень
    while first_level_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                first_level_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_window_flag = True
                    first_level_flag = False

            # Временный выход с первого уровня
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                first_level_flag = False
                start_window_flag = True

        screen.blit(first_level_bg, (0, 0))
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

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


# Кнопка "Утилизировать" (при нажатии вызывает функцию utilize_bottle())
class UtilizeButton(UniversalSprite):
    def __init__(self, group, image, x, y):
        super().__init__(group, image, x, y)

    def update(self, *args):
        global first_level_flag
        if args and first_level_flag:
            if args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                if args[0].button == 1:
                    utilize_bottle()
            if args[0].type == pygame.KEYDOWN:
                if args[0].key == pygame.K_z:
                    utilize_bottle()


# Кнопка "Выпить" (при нажатии вызывает функцию drink_bottle())
class DrinkButton(UniversalSprite):
    def __init__(self, group, image, x, y):
        super().__init__(group, image, x, y)

    def update(self, *args):
        global first_level_flag
        if args and first_level_flag:
            if args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                if args[0].button == 1:
                    drink_bottle()
            if args[0].type == pygame.KEYDOWN:
                if args[0].key == pygame.K_x:
                    drink_bottle()


# Кнопка "Следующий" (при нажатии досрочно сдвигает конвейер, и
# отсчет события сдвигания конвейера начинает отсчитываться от нового момента времени)
class NextButton(UniversalSprite):
    def __init__(self, group, image, x, y):
        super().__init__(group, image, x, y)

    def update(self, *args):
        global first_level_flag
        if args and first_level_flag:
            if args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
                if args[0].button == 1:
                    move_conveyor()
            if args[0].type == pygame.KEYDOWN:
                if args[0].key == pygame.K_c:
                    move_conveyor()


class ResetAchievementsButton(UniversalSprite):
    def __init__(self, group, image, x, y):
        super().__init__(group, image, x, y)

    def update(self, *args):
        global achievements_window_flag, game_progress, pop_sound
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and achievements_window_flag:
            if args[0].button == 1:
                pop_sound.play()
                with open("data/TxtFiles/Achievements.txt", "w", encoding="utf8") as file:
                    file.write("000000")
                reset_achievements_flags()
                game_progress = 0
                with open("data/TxtFiles/GameProgress.txt", "w", encoding="utf8") as file:
                    file.write("0")


# Класс клетки поля для второго уровня, определяет изображение и свойства клетки
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        global tiles_group, tile_width, tile_height, walls_group, larek_group, level_part_num, \
            tile_images
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(570 + tile_width * pos_x, 10 + tile_height * pos_y)
        if tile_type == "D" or tile_type == "U" or tile_type == "I" or tile_type == "R":
            self.add(walls_group)
        if tile_type == "F":
            if level_part_num == 3:
                self.image = pygame.image.load("data/PngFiles/SecondLevel/ValeraHouse.png")
            self.add(larek_group)


# Класс персонажа для второго уровня, определяет изображение персонажа, определяет
# передвижение персонажа по карте
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        global player_group, player_image, tile_width, tile_height
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(570 + tile_width * pos_x, 10 + tile_height * pos_y)

    def displacement(self, direction):
        global player, steps_counter, walls_group, step, steps_counter, move_sound
        old_position = (player.rect.x, player.rect.y)
        if direction == 'up':
            while not pygame.sprite.spritecollideany(player, walls_group):
                player.rect.y -= step
                if player.rect.y < -60:
                    player.rect.y = -60
                    break
            player.rect.y += step
        if direction == 'down':
            while not pygame.sprite.spritecollideany(player, walls_group):
                player.rect.y += step
                if player.rect.y > 710:
                    player.rect.y = 710
                    break
            player.rect.y -= step
        if direction == 'left':
            while not pygame.sprite.spritecollideany(player, walls_group):
                player.rect.x -= step
                if player.rect.x < 500:
                    player.rect.x = 500
                    break
            player.rect.x += step
        if direction == 'right':
            while not pygame.sprite.spritecollideany(player, walls_group):
                player.rect.x += step
                if player.rect.x > 1270:
                    player.rect.x = 1270
                    break
            player.rect.x -= step
        new_position = (player.rect.x, player.rect.y)
        if old_position != new_position:
            move_sound.play()
            steps_counter -= 1


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


# Возвращает случайно выбранный класс бутылки
def generate_bottle():
    # Некоторые бутылки встречаются 2 раза, таким образом их вероятность повышается
    new_bottle = choice([EthanolBottle(), EthanolBottle(),
                         VBottle(), VBottle(),
                         SolventBottle(), SolventBottle(),
                         MedicineBottle()])
    return new_bottle


# Сдвигает конвейер на одну ячейку вправо, изменяет HP и
# счетчик бутылок до победы в соответствии с правилами
def move_conveyor():
    global bottles_list, bottle_1, bottle_2, bottle_3, valera, valera_idle, \
        HP, first_level_seconds, bottles_counter, no_damage_flag, move_conveyor_sound, \
        damage_sound
    move_conveyor_sound.play()
    bottles_list = [generate_bottle(), bottles_list[0], bottles_list[1]]
    bottle_1.image = pygame.image.load(bottles_list[0].icon_path)
    bottle_2.image = pygame.image.load(bottles_list[1].icon_path)
    bottle_3.image = pygame.image.load(bottles_list[2].half_icon_path)
    valera.image = valera_idle
    old_hp = HP
    if bottles_list[2].text:
        if bottles_list[2].text == "V":
            damage_sound.play()
            HP -= 1
            bottles_counter -= 1
        elif bottles_list[2].text == "E":
            bottles_counter += 1
        elif bottles_list[2].text == "S":
            damage_sound.play()
            HP -= 1
            bottles_counter -= 1
        elif bottles_list[2].text == "M":
            damage_sound.play()
            HP -= 1
            bottles_counter -= 1
    new_hp = HP
    if new_hp < old_hp:
        no_damage_flag = "1"
        update_achievements_flags()
    check_hp()
    first_level_seconds = 0


# Убирает бутылку из 2 слота, меняет изображение Валеры в соответствии с бутылкой,
# изменяет HP и счетчик бутылок в соответствии с правилами
def drink_bottle():
    global bottles_list, HP, valera, valera_drink_v, valera_drink_e, \
        valera_drink_m, valera_drink_s, bottle_2, bottles_counter, no_damage_flag, \
        drink_bottle_sound, damage_sound
    old_hp = HP
    if bottles_list[1].text:
        drink_bottle_sound.play()
        if bottles_list[1].text == "V":
            valera.image = valera_drink_v
            bottles_counter += 1
        elif bottles_list[1].text == "E":
            damage_sound.play()
            HP -= 1
            bottles_counter -= 1
            valera.image = valera_drink_e
        elif bottles_list[1].text == "S":
            damage_sound.play()
            HP -= 1
            bottles_counter -= 1
            valera.image = valera_drink_s
        elif bottles_list[1].text == "M":
            HP += 1
            bottles_counter += 1
            valera.image = valera_drink_m
    new_hp = HP
    if new_hp < old_hp:
        no_damage_flag = "1"
        update_achievements_flags()
    bottles_list[1] = NoBottle()
    bottle_2.image = pygame.image.load(bottles_list[1].icon_path)
    check_hp()


# Убирает бутылку из 2 слота, изменяет HP и счетчик бутылок в соответствии с правилами
def utilize_bottle():
    global bottles_list, HP, bottle_2, bottles_counter, no_damage_flag, \
        utilize_bottle_sound, damage_sound
    old_hp = HP
    if bottles_list[1].text:
        utilize_bottle_sound.play()
        if bottles_list[1].text == "V":
            damage_sound.play()
            HP -= 1
            bottles_counter -= 1
        elif bottles_list[1].text == "E":
            damage_sound.play()
            HP -= 1
            bottles_counter -= 1
        elif bottles_list[1].text == "S":
            bottles_counter += 1
        elif bottles_list[1].text == "M":
            bottles_counter += 1
    new_hp = HP
    if new_hp < old_hp:
        no_damage_flag = "1"
        update_achievements_flags()
    bottles_list[1] = NoBottle()
    bottle_2.image = pygame.image.load(bottles_list[1].icon_path)
    check_hp()


# Обнуляет некоторые параметры и перезапускает первый уровень
def restart_first_level():
    global HP, bottles_list, bottles_counter, first_level_seconds, \
        bottle_1, bottle_2, bottle_3, valera, valera_idle
    HP = 3
    bottles_list = [NoBottle(), NoBottle(), NoBottle()]
    bottle_1.image = pygame.image.load(bottles_list[0].icon_path)
    bottle_2.image = pygame.image.load(bottles_list[1].icon_path)
    bottle_3.image = pygame.image.load(bottles_list[2].half_icon_path)
    valera.image = valera_idle
    bottles_counter = 0
    first_level_seconds = 0


# Проверяет HP и отрисовывает их в соответствии с количеством HP, при 0 HP завершает первый уровень
def check_hp():
    global HP, hit_point_1, hit_point_2, hit_point_3, game_over_window_flag, first_level_flag, \
        no_death_flag, empty_hp_image, hp_image
    if HP > 3:
        HP = 3
    elif HP <= 0:
        hit_point_1.image = empty_hp_image
        hit_point_2.image = empty_hp_image
        hit_point_3.image = empty_hp_image
        give_achievement(6)
        no_death_flag = "1"
        update_achievements_flags()
        game_over_window_flag = True
        first_level_flag = False
    elif HP == 3:
        hit_point_1.image = hp_image
        hit_point_2.image = hp_image
        hit_point_3.image = hp_image
    elif HP == 2:
        hit_point_1.image = hp_image
        hit_point_2.image = hp_image
        hit_point_3.image = empty_hp_image
    elif HP == 1:
        hit_point_1.image = hp_image
        hit_point_2.image = empty_hp_image
        hit_point_3.image = empty_hp_image


# Проверяет не ушел ли счетчик бутылок ниже 0
def check_bottles_counter():
    global bottles_counter
    if bottles_counter < 0:
        bottles_counter = 0


# Считывает карту уровня с файла
def load_level(filename):
    with open(filename, "r", encoding="utf8") as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


# Отрисовывает уровень по карте уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "S":
                Tile("=", x, y)
                new_player = Player(x, y)

            else:
                Tile(level[y][x], x, y)
    return new_player


# Обнуляет некоторые параметры и перезапускает второй уровень
def restart_second_level(part_num):
    global player, tiles_group, player_group, larek_group, walls_group, steps_counter, level_part_num
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    larek_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    if part_num == 1:
        level_part_num = 1
        steps_counter = 9
        player = generate_level(load_level("data/TxtFiles/Second_Level_1.txt"))
    elif part_num == 2:
        steps_counter = 9
        player = generate_level(load_level("data/TxtFiles/Second_Level_2.txt"))
    elif part_num == 3:
        steps_counter = 22
        player = generate_level(load_level("data/TxtFiles/Second_Level_3.txt"))


# Выдает достижение
def give_achievement(ach_num):
    with open("data/TxtFiles/Achievements.txt", "r", encoding="utf8") as file:
        text = list(file.read().split("\n")[0])
    text[ach_num - 1] = "1"
    with open("data/TxtFiles/Achievements.txt", "w", encoding="utf8") as file:
        file.write("".join(text))


#
def update_achievements_flags():
    global no_death_flag, no_damage_flag
    with open("data/TxtFiles/AchievementsFlags.txt", "w", encoding="utf8") as file:
        file.write(f"NoDamage-{no_damage_flag}\nNoDeath-{no_death_flag}")


# Проверяет наличие достижений и меняет изображение при наличии/отсутствии достижения
def check_achievements():
    global achievement_1, achievement_2, achievement_3, achievement_4, achievement_5, achievement_6
    with open("data/TxtFiles/Achievements.txt", "r", encoding="utf8") as file:
        ach = file.read().split("\n")[0]
    for i in range(len(ach)):
        if ach[i] == "1":
            if i + 1 == 1:
                achievement_1.image = pygame.image.load("data/PngFiles/Achievements/Ach1.png")
            elif i + 1 == 2:
                achievement_2.image = pygame.image.load("data/PngFiles/Achievements/Ach2.png")
            elif i + 1 == 3:
                achievement_3.image = pygame.image.load("data/PngFiles/Achievements/Ach3.png")
            elif i + 1 == 4:
                achievement_4.image = pygame.image.load("data/PngFiles/Achievements/Ach4.png")
            elif i + 1 == 5:
                achievement_5.image = pygame.image.load("data/PngFiles/Achievements/Ach5.png")
            elif i + 1 == 6:
                achievement_6.image = pygame.image.load("data/PngFiles/Achievements/Ach6.png")
        else:
            if i + 1 == 1:
                achievement_1.image = pygame.image.load("data/PngFiles/Achievements/Ach1BW.png")
            elif i + 1 == 2:
                achievement_2.image = pygame.image.load("data/PngFiles/Achievements/Ach2BW.png")
            elif i + 1 == 3:
                achievement_3.image = pygame.image.load("data/PngFiles/Achievements/Ach3BW.png")
            elif i + 1 == 4:
                achievement_4.image = pygame.image.load("data/PngFiles/Achievements/Ach4BW.png")
            elif i + 1 == 5:
                achievement_5.image = pygame.image.load("data/PngFiles/Achievements/Ach5BW.png")
            elif i + 1 == 6:
                achievement_6.image = pygame.image.load("data/PngFiles/Achievements/Ach6BW.png")


#
def reset_achievements_flags():
    global no_death_flag, no_damage_flag
    with open("data/TxtFiles/AchievementsFlags.txt", "w", encoding="utf8") as file:
        file.write(f"NoDamage-0\nNoDeath-0")
    no_damage_flag = "0"
    no_death_flag = "0"


# Инициализация pygame.mixer и pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Создание окна
size = width, height = 1280, 720
pygame.display.set_icon(pygame.image.load("data/PngFiles/Other/Icon.ico"))
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
ResetProgressButton(start_window_buttons, pygame.image.load("data/PngFiles/BigBtn/ResetProgressBtn.png"), 1072, 680)

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

# Достижения
achievements_group = pygame.sprite.Group()
ResetAchievementsButton(achievements_group, pygame.image.load("data/PngFiles/BigBtn/ResetProgressBtn.png"), 540, 590)
achievement_1 = UniversalSprite(achievements_group,
                                pygame.image.load("data/PngFiles/Achievements/Ach1BW.png"), 100, 50)
achievement_2 = UniversalSprite(achievements_group,
                                pygame.image.load("data/PngFiles/Achievements/Ach2BW.png"), 380, 230)
achievement_3 = UniversalSprite(achievements_group,
                                pygame.image.load("data/PngFiles/Achievements/Ach3BW.png"), 930, 50)
achievement_4 = UniversalSprite(achievements_group,
                                pygame.image.load("data/PngFiles/Achievements/Ach4BW.png"), 100, 375)
achievement_5 = UniversalSprite(achievements_group,
                                pygame.image.load("data/PngFiles/Achievements/Ach5BW.png"), 650, 230)
achievement_6 = UniversalSprite(achievements_group,
                                pygame.image.load("data/PngFiles/Achievements/Ach6BW.png"), 930, 375)
with open("data/TxtFiles/AchievementsFlags.txt", "r", encoding="utf8") as file:
    no_damage_flag, no_death_flag = [x.split("-")[1] for x in file.read().split("\n")]

# Кнопки 1 уровня
first_level_buttons = pygame.sprite.Group()
UtilizeButton(first_level_buttons, pygame.image.load("data/PngFiles/SmallBtn/XBtn.png"), 550, 280)
DrinkButton(first_level_buttons, pygame.image.load("data/PngFiles/SmallBtn/DrBtn.png"), 650, 280)
NextButton(first_level_buttons, pygame.image.load("data/PngFiles/SmallBtn/NextBtn.png"), 750, 280)

# Бутылки для 1 уровня
bottles = pygame.sprite.Group()
bottle_1 = UniversalSprite(bottles, pygame.image.load(bottles_list[0].icon_path), 220, 480)
bottle_2 = UniversalSprite(bottles, pygame.image.load(bottles_list[1].icon_path), 590, 480)
bottle_3 = UniversalSprite(bottles, pygame.image.load(bottles_list[1].half_icon_path), 1125, 480)

# Жизни для 1 уровня
hit_points = pygame.sprite.Group()
hp_image = pygame.image.load("data/PngFiles/Other/HP.png")
empty_hp_image = pygame.image.load("data/PngFiles/Other/EmptyHP.png")
hit_point_1 = UniversalSprite(hit_points, hp_image, 1195, 100)
hit_point_2 = UniversalSprite(hit_points, hp_image, 1195, 160)
hit_point_3 = UniversalSprite(hit_points, hp_image, 1195, 220)

# Валера для 1 уровня
valera_group = pygame.sprite.Group()
valera_drink_v = pygame.image.load("data/PngFiles/Valeras/ValeraDrinkV.png")
valera_drink_e = pygame.image.load("data/PngFiles/Valeras/ValeraDrinkE.png")
valera_drink_s = pygame.image.load("data/PngFiles/Valeras/ValeraDrinkS.png")
valera_drink_m = pygame.image.load("data/PngFiles/Valeras/ValeraDrinkM.png")
valera_idle = pygame.image.load("data/PngFiles/Valeras/ValeraIdle.png")
valera = UniversalSprite(valera_group, valera_idle, 575, 365)

# Звуки
move_conveyor_sound = pygame.mixer.Sound("data/Sounds/ConveyorSound.wav")
move_conveyor_sound.set_volume(0.5)
drink_bottle_sound = pygame.mixer.Sound("data/Sounds/DrinkSound.wav")
drink_bottle_sound.set_volume(0.5)
utilize_bottle_sound = pygame.mixer.Sound("data/Sounds/UtilizeBottleSound.wav")
utilize_bottle_sound.set_volume(0.5)
damage_sound = pygame.mixer.Sound("data/Sounds/DamageSound.wav")
damage_sound.set_volume(0.5)
pop_sound = pygame.mixer.Sound("data/Sounds/PopSound.wav")
pop_sound.set_volume(0.1)
move_sound = pygame.mixer.Sound("data/Sounds/MoveSound.wav")
move_sound.set_volume(0.1)
buy_v_sound = pygame.mixer.Sound("data/Sounds/BuyVSound.wav")
buy_v_sound.set_volume(0.5)
win_sound = pygame.mixer.Sound("data/Sounds/WinSound.wav")
win_sound.set_volume(0.5)

# Музыка
pygame.mixer.music.set_volume(0.1)
menu_music_name = "data/Sounds/MenuMusic.mp3"
first_level_music_name = "data/Sounds/CPU_Talk.mp3"
second_level_music_name = "data/Sounds/Rain.mp3"
final_music_name = "data/Sounds/Digestive_biscuit.mp3"
pygame.mixer.music.load(menu_music_name)

# Группы спрайтов для 2 уровня
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
larek_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()

# Изображения для 2 уровня
tile_images = {"=": pygame.image.load("data/PngFiles/SecondLevel/RoadLR.png"),
               "+": pygame.image.load("data/PngFiles/SecondLevel/RoadTBLR.png"),
               "|": pygame.image.load("data/PngFiles/SecondLevel/RoadTB.png"),
               "L": pygame.image.load("data/PngFiles/SecondLevel/RoadTR.png"),
               "J": pygame.image.load("data/PngFiles/SecondLevel/RoadLT.png"),
               "/": pygame.image.load("data/PngFiles/SecondLevel/RoadRB.png"),
               "7": pygame.image.load("data/PngFiles/SecondLevel/RoadBL.png"),
               "D": pygame.image.load("data/PngFiles/SecondLevel/HouseD.png"),
               "U": pygame.image.load("data/PngFiles/SecondLevel/HouseT.png"),
               "I": pygame.image.load("data/PngFiles/SecondLevel/HouseL.png"),
               "R": pygame.image.load("data/PngFiles/SecondLevel/HouseR.png"),
               "F": pygame.image.load("data/PngFiles/SecondLevel/LarekKalitka.png"),
               "Z": pygame.image.load("data/PngFiles/SecondLevel/RoadRBL.png"),
               "X": pygame.image.load("data/PngFiles/SecondLevel/RoadTRB.png"),
               "C": pygame.image.load("data/PngFiles/SecondLevel/RoadLTR.png"),
               "V": pygame.image.load("data/PngFiles/SecondLevel/RoadBLT.png")}
player_image = pygame.image.load("data/PngFiles/Valeras/ValeraHead.png")
step = tile_width = tile_height = 70

# Счетчик шагов для 2 уровня
steps_counter = 0

# Персонаж для 2 уровня
player = None

# Счетчик для этапов 2 уровня
level_part_num = 1

# Позиция титров по y
credits_y = 720

# ФПС для титров
clock = pygame.time.Clock()
credits_FPS = 60

# Игра
pygame.mixer.music.play(-1, 0.0, 1500)
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
                    pop_sound.play()
                    start_window_flag = True
                    info_window_flag = False
        screen.blit(info_window_bg, (0, 0))
        draw_text(info_text, screen, title_font, text_font, 40, 420, 30, 250, 150, 250, 600)
        pygame.display.flip()

    # Окно с достижениями
    while achievements_window_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                achievements_window_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pop_sound.play()
                    start_window_flag = True
                    achievements_window_flag = False
            achievements_group.update(event)
        screen.blit(achievements_window_bg, (0, 0))
        check_achievements()
        achievements_group.draw(screen)
        draw_text(achievements_window_text, screen, title_font, small_font, 30, 525, 100, 125, 300, 495, 650)
        pygame.display.flip()

    # Обучение для первого уровня
    while first_level_text_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                first_level_text_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pop_sound.play()
                    first_level_flag = True
                    restart_first_level()
                    first_level_text_flag = False
        screen.blit(first_level_text_bg, (0, 0))
        draw_text(first_level_text, screen, title_font, text_font, 35, 460, 15, 250, 120, 400, 625)
        pygame.display.flip()

    # Первый уровень
    while first_level_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                first_level_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pop_sound.play()
                    pygame.mixer.music.load(menu_music_name)
                    pygame.mixer.music.play(-1, 0.0, 1500)
                    start_window_flag = True
                    first_level_flag = False
            if event.type == CONVEYORTIMER:
                first_level_seconds += 200
            first_level_buttons.update(event)
        screen.blit(first_level_bg, (0, 0))
        check_bottles_counter()
        draw_text(["", "", f"Бутылок: {bottles_counter} / 100", ""], screen,
                  title_font, text_font, 35, 0, 0, 1070, 30, 0, 0)
        first_level_buttons.draw(screen)
        hit_points.draw(screen)
        valera_group.draw(screen)
        bottles.draw(screen)
        check_hp()
        if bottles_counter <= 10:
            if first_level_seconds == 1600:
                move_conveyor()
        elif 10 < bottles_counter <= 25:
            if first_level_seconds == 1400:
                move_conveyor()
        elif 25 < bottles_counter <= 50:
            if first_level_seconds == 1200:
                move_conveyor()
        elif 50 < bottles_counter <= 90:
            if first_level_seconds == 1000:
                move_conveyor()
        elif 90 < bottles_counter <= 100:
            if first_level_seconds == 800:
                move_conveyor()
        if bottles_counter >= 100:
            win_sound.play()
            give_achievement(4)
            pygame.mixer.music.load(second_level_music_name)
            pygame.mixer.music.play(-1, 0.0, 1500)
            game_progress = 1
            with open("data/TxtFiles/GameProgress.txt", "w", encoding="utf8") as file:
                file.write("1")
            second_level_text_flag = True
            first_level_flag = False
        pygame.display.flip()

    # Окно Game Over
    while game_over_window_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over_window_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pop_sound.play()
                    restart_first_level()
                    first_level_flag = True
                    game_over_window_flag = False
        screen.blit(game_over_window_bg, (0, 0))
        draw_text(game_over_text, screen, very_big_font, text_font, 150, 300, 100, 0, 600, 310, 600)
        pygame.display.flip()

    # Обучение для второго уровня
    while second_level_text_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                second_level_text_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pop_sound.play()
                    restart_second_level(1)
                    second_level_flag = True
                    second_level_text_flag = False
        screen.blit(second_level_text_bg, (0, 0))
        draw_text(second_level_text, screen, title_font, text_font, 35, 450, 15, 250, 120, 400, 625)
        pygame.display.flip()

    # Второй уровень
    while second_level_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                second_level_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pop_sound.play()
                    pygame.mixer.music.load(menu_music_name)
                    pygame.mixer.music.play(-1, 0.0, 1500)
                    start_window_flag = True
                    second_level_flag = False
                if event.key == pygame.K_a:
                    player.displacement('left')
                elif event.key == pygame.K_d:
                    player.displacement('right')
                elif event.key == pygame.K_w:
                    player.displacement('up')
                elif event.key == pygame.K_s:
                    player.displacement('down')
        screen.blit(second_level_bg, (0, 0))
        draw_text(["Управление:", "", "Для предвижения используйте WASD", ""],
                  screen, title_font, text_font, 35, 20, 300, 20, 350, 0, 0)
        draw_text(["Цель:", "", "Добраться до дома или ларька за данное", "кол-во движений", ""],
                  screen, title_font, text_font, 35, 20, 400, 20, 450, 0, 0)
        draw_text(["", "", f"Ходов осталось: {steps_counter}", ""],
                  screen, title_font, text_font, 35, 0, 0, 150, 600, 0, 0)
        pygame.draw.rect(screen, pygame.color.Color("gray"), (570, 10, 700, 700), 5)
        tiles_group.draw(screen)
        player_group.draw(screen)
        if pygame.sprite.spritecollideany(player, larek_group):
            if level_part_num == 3:
                win_sound.play()
                game_progress = 0
                with open("data/TxtFiles/GameProgress.txt", "w", encoding="utf8") as file:
                    file.write("0")
                pygame.mixer.music.load(final_music_name)
                pygame.mixer.music.play(-1, 1.0, 1500)
                give_achievement(1)
                give_achievement(5)
                if no_death_flag == "0":
                    give_achievement(2)
                if no_damage_flag == "0":
                    give_achievement(3)
                reset_achievements_flags()
                final_window_flag = True
                second_level_flag = False
                break
            else:
                buy_v_sound.play()
                level_part_num += 1
                restart_second_level(level_part_num)
        if steps_counter <= 0:
            give_achievement(6)
            damage_sound.play()
            no_damage_flag = "1"
            no_death_flag = "1"
            update_achievements_flags()
            restart_second_level(level_part_num)
        pygame.display.flip()

    # Концовка
    while final_window_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                final_window_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pop_sound.play()
                    pygame.mixer.music.set_volume(0.5)
                    credits_window_flag = True
                    final_window_flag = False
        screen.blit(final_window_bg, (0, 0))
        draw_text(final_window_text, screen, title_font, text_font, 35, 550, 50, 250, 150, 400, 600)
        pygame.display.flip()

    # Титры
    while credits_window_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                credits_window_flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pop_sound.play()
                    credits_y = 720
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.load(menu_music_name)
                    pygame.mixer.music.play(-1, 0.0, 1500)
                    start_window_flag = True
                    credits_window_flag = False
        screen.fill(pygame.color.Color("black"))
        draw_text(credits_text, screen, title_font, text_font, 35, 0, 0, 250, credits_y, 0, 0)
        credits_y -= 1
        clock.tick(credits_FPS)
        pygame.display.flip()

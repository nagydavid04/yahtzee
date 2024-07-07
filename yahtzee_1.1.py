
import pygame
from ftplib import FTP
import os
import io
import random
import yahtzee_offline as offlinegamefile
pygame.init()

DISPLAY_INFO = pygame.display.Info()
WIDTH, HEIGHT = DISPLAY_INFO.current_w, DISPLAY_INFO.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FPS = 60

VERSION = 1.1

combinations = ["Sum", "Pair", "Drill", "Two pair", "Four of a kind", "Full", "Small straight", "Big straight", "Five of a kind"]

WIDTH_DICE = HEIGHT // 7
SPACE_BETWEEN_DICES = (HEIGHT - WIDTH_DICE * 5) // 10

WIDTH_ROW = WIDTH // 3
HEIGHT_ROW = HEIGHT // (9 * 1.3)

SPACE_BETWEEN_ROWS = HEIGHT_ROW // 10

WIDTH_FIRST_COLUMN = WIDTH_ROW // 2
WIDTH_SECOND_COLUMN = WIDTH_ROW // 4
WIDTH_THIRD_COLUMN = WIDTH_SECOND_COLUMN

X_FIRST_COL = WIDTH // 7
X_SECOND_COL = X_FIRST_COL + WIDTH_FIRST_COLUMN
X_THIRD_COL = X_SECOND_COL + WIDTH_SECOND_COLUMN
Y_COL = (HEIGHT - HEIGHT_ROW * 9 - 8 * SPACE_BETWEEN_ROWS) // 2

X_FIRST_TEXT = X_FIRST_COL + WIDTH_FIRST_COLUMN // 2
X_SECOND_BIG_TEXT = X_SECOND_COL + WIDTH_SECOND_COLUMN // 2
X_SECOND_SMALL_TEXT = X_SECOND_COL + WIDTH_SECOND_COLUMN * 5 // 6
X_THIRD_BIG_TEXT = X_THIRD_COL + WIDTH_THIRD_COLUMN // 2
X_THIRD_SMALL_TEXT = X_THIRD_COL + WIDTH_THIRD_COLUMN * 5 // 6

SPACE_BETWEEN_LINE_AND_SMALL_TEXT = HEIGHT_ROW // 4

grey = (200, 200, 200)
green = (0, 200, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 40, 40)
purple = (130, 0, 130)

COURIERNEW_BIG = pygame.font.SysFont("couriernew", WIDTH // 25)
COURIERNEW_BIG_BOLD = pygame.font.SysFont("couriernew", WIDTH // 25, bold=True)
COURIERNEW_MEDIUM = pygame.font.SysFont("couriernew", WIDTH // 40)
COURIERNEW_MEDIUM_BOLD = pygame.font.SysFont("couriernew", WIDTH // 40, bold=True)
COURIERNEW_SMALL = pygame.font.SysFont("couriernew", WIDTH // 75)
COURIERNEW_SMALL_BOLD = pygame.font.SysFont("couriernew", WIDTH // 75, bold=True)

TAB = "     "

NAME_COMPUTER = os.getenv('COMPUTERNAME')

#I won't give you access to the ftp server
server = FTP("???", "???", "???")
server.cwd("yahtzee")

def list_dir():
    files = server.nlst()

    files.remove(".")
    files.remove("..")

    return files

def upload_request(name, parameters):
    server.cwd("requests")
    server.storbinary(f"STOR {name}", io.BytesIO(str(parameters).encode("utf-8")))
    server.cwd("..")
def download_response_for_user(name):
    server.cwd("responses")
    files = list_dir()

    for filename in files:
        if filename == name:
            data = []
            server.retrbinary(f"RETR {filename}", data.append)
            data = data[0].decode()

            server.delete(filename)
            server.cwd("..")

            return data

    server.cwd("..")

    return None

class Row:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

        self.reset()

    def reset(self):
        self.val_player1 = ""
        self.val_player2 = ""

        self.val_not_selected_player1 = ""
        self.val_not_selected_player2 = ""

    def update(self, game_variables):
        datas = game_variables[self.name]

        if datas[1] != None:
            self.val_player1 = datas[1]

        if datas[2] != None:
            self.val_player2 = datas[2]

        if game_variables["player1_choose"] and not game_variables["loop_throw"]:
            self.val_not_selected_player1 = datas[0] if datas[0] != None else ""
            self.val_not_selected_player2 = ""

        elif game_variables["player2_choose"] and not game_variables["loop_throw"]:
            self.val_not_selected_player2 = datas[0] if datas[0] != None else ""
            self.val_not_selected_player1 = ""

    def draw(self, game_variables):
        pygame.draw.rect(screen, black, (self.x, self.y, WIDTH_ROW, HEIGHT_ROW), width=WIDTH // 250)
        pygame.draw.line(screen, black, (X_SECOND_COL, self.y), (X_SECOND_COL, self.y + HEIGHT_ROW - 1), width=WIDTH // 250)
        pygame.draw.line(screen, black, (X_THIRD_COL, self.y), (X_THIRD_COL, self.y + HEIGHT_ROW - 1), width=WIDTH // 250)

        text_name = COURIERNEW_SMALL_BOLD.render(self.name, True, black)

        text_val_player1 = COURIERNEW_MEDIUM_BOLD.render(str(self.val_player1), True, black)
        text_val_player2 = COURIERNEW_MEDIUM_BOLD.render(str(self.val_player2), True, black)

        text_val_not_selected_player1 = COURIERNEW_SMALL_BOLD.render(str(self.val_not_selected_player1), True, black)
        text_val_not_selected_player2 = COURIERNEW_SMALL_BOLD.render(str(self.val_not_selected_player2), True, black)

        screen.blit(text_name, (X_FIRST_TEXT - text_name.get_width() // 2, self.y + HEIGHT_ROW // 2 - text_name.get_height() // 2))

        screen.blit(text_val_player1, (X_SECOND_BIG_TEXT - text_val_player1.get_width() // 2, self.y + HEIGHT_ROW // 2 - text_val_player1.get_height() // 2))
        screen.blit(text_val_player2, (X_THIRD_BIG_TEXT - text_val_player2.get_width() // 2, self.y + HEIGHT_ROW // 2 - text_val_player2.get_height() // 2))

        if game_variables["player1_choose"] and not game_variables["loop_throw"]:
            screen.blit(text_val_not_selected_player1, (X_SECOND_SMALL_TEXT - text_val_not_selected_player1.get_width() // 2, self.y + SPACE_BETWEEN_LINE_AND_SMALL_TEXT - text_val_not_selected_player1.get_height() // 2))
        elif game_variables["player2_choose"] and not game_variables["loop_throw"]:
            screen.blit(text_val_not_selected_player2, (X_THIRD_SMALL_TEXT - text_val_not_selected_player2.get_width() // 2, self.y + SPACE_BETWEEN_LINE_AND_SMALL_TEXT - text_val_not_selected_player2.get_height() // 2))
class Dice:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width

        self.value = 1

        self.coordinates = {"topleft": (self.x + self.width // 5, self.y + self.width // 5),
                            "left": (self.x + self.width // 5, self.y + self.width // 2),
                            "bottomleft": (self.x + self.width // 5, self.y + self.width * 4 // 5),
                            "center": (self.x + self.width // 2, self.y + self.width // 2),
                            "topright": (self.x + self.width * 4 // 5, self.y + self.width // 5),
                            "right": (self.x + self.width * 4 // 5, self.y + self.width // 2),
                            "bottomright": (self.x + self.width * 4 // 5, self.y + self.width * 4 // 5)}

    def draw(self):
        def draw_dots(*points):
            for point in points:
                pygame.draw.circle(screen, black, (self.coordinates[point]), WIDTH // 125)

        pygame.draw.rect(screen, black, (self.x, self.y, WIDTH_DICE, WIDTH_DICE), width = WIDTH // 250)

        if self.value == 1:
            draw_dots("center")

        elif self.value == 2:
            draw_dots("topleft", "bottomright")

        elif self.value == 3:
            draw_dots("bottomleft", "center", "topright")

        elif self.value == 4:
            draw_dots("topleft", "bottomleft", "topright", "bottomright")

        elif self.value == 5:
            draw_dots("topleft", "bottomleft", "center", "topright", "bottomright")

        elif self.value == 6:
            draw_dots("topleft", "left", "bottomleft", "topright", "right", "bottomright")
class Label:
    def __init__(self, x, y, text, font, color):
        self.x = x
        self.y = y
        self.text = str(text)
        self.font = font
        self.color = color

        self.rendered_text = self.font.render(self.text, True, self.color)

        self.half_width = self.rendered_text.get_width() // 2
        self.half_height = self.rendered_text.get_height() // 2

    def draw(self):
        screen.blit(self.rendered_text, (self.x - self.half_width, self.y - self.half_height))

    def update(self):
        self.rendered_text = self.font.render(self.text, True, self.color)

        self.half_width = self.rendered_text.get_width() // 2
        self.half_height = self.rendered_text.get_height() // 2
class TextInput:
    def __init__(self, x, y, font, max_length, color_inactive, color_active, color_text, text_label, font_label, is_password=False):
        self.x = x
        self.y = y
        self.font = font
        self.max_length = max_length
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color_text = color_text

        self.rendered_text_label = font_label.render(text_label, True, self.color_text)

        self.is_password = is_password

        self.text = TAB
        self.rect = None
        self.active = False

    def draw(self):
        if self.is_password and self.text != TAB:
            rendered_text = self.font.render(len(self.text) * "*", True, self.color_text)
        else:
            rendered_text = self.font.render(self.text, True, self.color_text)
        self.rect = pygame.Rect(self.x - rendered_text.get_width() * 0.5, self.y - rendered_text.get_height() * 0.5, rendered_text.get_width(), rendered_text.get_height())

        if self.active:
            pygame.draw.rect(screen, self.color_active, self.rect)
        else:
            pygame.draw.rect(screen, self.color_inactive, self.rect)

        screen.blit(rendered_text, (self.x - rendered_text.get_width() // 2, self.y - rendered_text.get_height() // 2))

        screen.blit(self.rendered_text_label, (self.x - self.rendered_text_label.get_width() // 2, self.y - rendered_text.get_height() // 2 - self.rendered_text_label.get_height()))

    def loop(self, pressed_key):
        if self.active and pressed_key != None:
            if pressed_key != "backspace":
                if len(self.text) != self.max_length:
                    if self.text == TAB:
                        self.text = ""
                    self.text += pressed_key
            else:
                if self.text != TAB:
                    self.text = self.text[:-1]
                    if self.text == "":
                        self.text = TAB

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
               self.active = True
            else:
                self.active = False
class Button:
    def __init__(self, x, y, width, height, color_text, color_button, text, font, command=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_text = color_text
        self.color_button = color_button
        self.rendered_text = font.render(text, True, self.color_text)
        self.command = command

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect_shadow = pygame.Rect(self.rect.x + self.width // 20, self.rect.y + self.height // 20,
                                       self.width * 18 // 20, self.height * 18 // 20)
        self.pressed = False

    def draw(self):
        pygame.draw.rect(screen, self.color_button, self.rect)

        if self.pressed:
            pygame.draw.rect(screen, [color / 2 for color in self.color_button], self.rect_shadow, width=WIDTH // 300)

        screen.blit(self.rendered_text, (self.x + self.width // 2 - self.rendered_text.get_width() // 2, self.y + self.height // 2 - self.rendered_text.get_height() // 2))

    def loop(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.pressed = True

        elif self.pressed:
            self.pressed = False
            if self.command is not None:
                self.command()
            return True

        return False
class Table:
    def __init__(self, x, y, num_of_names, font, color, username):
        self.x = x
        self.y = y
        self.num_of_names = num_of_names
        self.font = font
        self.color = color

        self.username = username

        self.count = 0

        self.page = 0

        self.button_up = Button(self.x, self.y + num_of_names * self.font.render("A", True, self.color).get_height() * 1.5, WIDTH * 0.1, HEIGHT * 0.05, black, grey, "UP", self.font, self.func_button_up)
        self.button_down = Button(self.x + WIDTH * 0.25, self.y + num_of_names * self.font.render("A", True, self.color).get_height() * 1.5, WIDTH * 0.1, HEIGHT * 0.05, black, grey, "DOWN", self.font, self.func_button_down)

        self.rendered_texts = []
        self.buttons = []
        for index in range(self.num_of_names):
            button = Button(self.x + WIDTH * 0.25, self.y + index * self.font.render("", True, self.color).get_height() * 1.5, WIDTH * 0.1, HEIGHT * 0.05, black, grey, "Invite", self.font)
            self.buttons.append(button)
    def func_button_up(self):
        if self.page > 0:
            self.page -= 1

    def func_button_down(self):
        if len(self.accounts) - (self.num_of_names * (self.page + 1)) > 0:
            self.page += 1

    def draw(self):
        self.button_up.draw()
        self.button_down.draw()

        index = 0
        for button, rendered_text in zip(self.buttons, self.rendered_texts):
            screen.blit(rendered_text, (self.x, self.y + index * rendered_text.get_height() * 1.5))
            button.draw()

            index += 1

    def update(self, online_players_status):
        self.accounts = online_players_status.copy()
        try:
            self.accounts.pop(self.username)
        except KeyError:
            pass
        accounts2 = self.accounts.copy()
        for key, val in accounts2.items():
            if val["in_match"]:
                self.accounts.pop(key)
        self.rendered_texts = []

        for index, account in enumerate(list(self.accounts.keys())[
                                        self.page * self.num_of_names: self.page * self.num_of_names + self.num_of_names]):
            rendered_text = self.font.render(account, True, self.color)
            self.rendered_texts.append(rendered_text)
    def loop(self):
        self.button_up.loop()
        self.button_down.loop()

        for index in range(len(self.rendered_texts)):
            if self.buttons[index].loop():
                return list(self.accounts.keys())[self.page * self.num_of_names + index]

def show_match(users, my_username):
    def draw_match():
        screen.fill(white)

        label_Quit_ESC.draw()
        label_player1.draw()
        label_player2.draw()

        label_points_player1.text = str(game_variables["player1_points"])
        label_points_player1.update()
        label_points_player1.draw()

        label_points_player2.text = str(game_variables["player2_points"])
        label_points_player2.update()
        label_points_player2.draw()

        if game_variables["player1_throw"]:
            label_turn.text = f"{users[0]} throws!"
        elif game_variables["player1_choose"]:
            label_turn.text = f"{users[0]} chooses!"
        if game_variables["player2_throw"]:
            label_turn.text = f"{users[1]} throws!"
        elif game_variables["player2_choose"]:
            label_turn.text = f"{users[1]} chooses!"
        label_turn.update()
        label_turn.draw()

        button_throw.draw()

        for dice in dices:
            dice.draw()

        for row in rows:
            row.draw(game_variables)

    def update_rows():
        for row in rows:
            row.update(game_variables)

    def update_dices():
        for index, dice in enumerate(dices):
            dice.value = game_variables["dices"][index]

    def update_combinations_value_in_game_variables():
        def count_number(num):
            count = 0
            for val in values:
                if val == num:
                    count += 1
            return count

        values = [dice.value for dice in dices]

        no_duplicates_values = sorted(set(values))
        counts = [count_number(val) for val in no_duplicates_values]

        no_duplicates_values = no_duplicates_values[::-1]
        counts = counts[::-1]

        for index_combination, combination in enumerate(combinations):
            if game_variables["player1_choose"] and game_variables[combination][1] != None:
                game_variables[combination][0] = None
                continue
            if game_variables["player2_choose"] and game_variables[combination][2] != None:
                game_variables[combination][0] = None
                continue

            points = 0

            if index_combination == 0:
                points = sum(values)

            elif index_combination == 1:
                for index, count in enumerate(counts):
                    if count >= 2:
                        points = no_duplicates_values[index] * 2
                        break

            elif index_combination == 2:
                for index, count in enumerate(counts):
                    if count >= 3:
                        points = no_duplicates_values[index] * 3
                        break

            elif index_combination == 3:
                pairs = []
                for index, count in enumerate(counts):
                    if count >= 2:
                        pairs.append(no_duplicates_values[index])

                if len(pairs) >= 2:
                    points = (pairs[0] + pairs[1]) * 2

            elif index_combination == 4:
                for index, count in enumerate(counts):
                    if count >= 4:
                        points = no_duplicates_values[index] * 4
                        break

            elif index_combination == 5:
                if counts == [3, 2] or counts == [2, 3]:
                    points = sum(values)

            elif index_combination == 6:
                if no_duplicates_values in [[6, 5, 4, 3], [5, 4, 3, 2], [4, 3, 2, 1]]:
                    points = 15

            elif index_combination == 7:
                if no_duplicates_values in [[6, 5, 4, 3, 2], [5, 4, 3, 2, 1]]:
                    points = 20

            elif index_combination == 8:
                if len(no_duplicates_values) == 1:
                    points = 50

            game_variables[combination][0] = points

    def upload_game_variables(need_response):
        if need_response:
            upload_request(f"{NAME_COMPUTER}%%%upload_game_variables%%%", f"{path}%%%{game_variables}%%%True%%%")

            response = None
            while response is None:
                response = download_response_for_user(f"{NAME_COMPUTER}%%%upload_game_variables%%%")

        else:
            upload_request(f"{NAME_COMPUTER}%%%upload_game_variables%%%", f"{path}%%%{game_variables}%%%False%%%")

    def download_game_variables():
        upload_request(f"{NAME_COMPUTER}%%%download_game_variables%%%", f"{path}%%%True%%%")

        response = None
        while response is None:
            response = download_response_for_user(f"{NAME_COMPUTER}%%%download_game_variables%%%")
            try:
                response = eval(response)
            except:
                response = None

        return response

    def handle_select_player1():
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            for index, rect in enumerate(player1_rectangles):
                row_name = rows[index].name
                if rect.collidepoint(pos) and game_variables[row_name][1] == None:
                    game_variables[row_name][1] = game_variables[row_name][0]
                    game_variables["player1_points"] += game_variables[row_name][0]
                    return True

    def handle_select_player2():
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            for index, rect in enumerate(player2_rectangles):
                row_name = rows[index].name
                if rect.collidepoint(pos) and game_variables[row_name][2] == None:
                    game_variables[row_name][2] = game_variables[row_name][0]
                    game_variables["player2_points"] += game_variables[row_name][0]
                    return True

    def get_match_status():
        upload_request(f"{NAME_COMPUTER}%%%get_online_players_status%%%", "___%%%True%%%")
        response = None
        while response is None:
            response = download_response_for_user(f"{NAME_COMPUTER}%%%get_online_players_status%%%")

        online_players_status = eval(response)
        try:
            if my_username == player1:
                if online_players_status[player2]["in_match"]:
                    return True
                else:
                    return False
            else:
                if online_players_status[player1]["in_match"]:
                    return True
                else:
                    return False
        except KeyError:
            return False


    dices = []
    y = SPACE_BETWEEN_DICES
    for _ in range(5):
        dices.append(Dice(int(WIDTH - 2 * SPACE_BETWEEN_DICES - WIDTH_DICE), y, HEIGHT // 7))
        y += 2 * SPACE_BETWEEN_DICES + WIDTH_DICE

    player1_rectangles = []
    player2_rectangles = []
    rows = []
    y = Y_COL
    for name in combinations:
        player1_rectangles.append(pygame.Rect(X_SECOND_COL, y, WIDTH_ROW * 0.25, HEIGHT_ROW))
        player2_rectangles.append(pygame.Rect(X_THIRD_COL, y, WIDTH_ROW * 0.25, HEIGHT_ROW))

        rows.append(Row(X_FIRST_COL, y, name))
        y += HEIGHT_ROW + SPACE_BETWEEN_ROWS

    player1 = users[0]
    player2 = users[1]

    path = f"{player1}_{player2}.txt"

    game_variables = {"player1_points": 0, "player2_points": 0, "num_of_throws": 0, "player1_throw": True,
                      "player1_choose": False, "player2_throw": False, "player2_choose": False,
                      "dices": [dice.value for dice in dices], "loop_throw": False, "loop_count": 0,
                      "Sum": [None, None, None, None, None], "Pair": [None, None, None, None, None], "Drill": [None, None, None, None, None], "Two pair": [None, None, None, None, None],
                      "Four of a kind": [None, None, None, None, None], "Full": [None, None, None, None, None], "Small straight": [None, None, None, None, None],
                      "Big straight": [None, None, None, None, None], "Five of a kind": [None, None, None, None, None]}

    if my_username == player2:
        upload_game_variables(True)

    label_Quit_ESC = Label(dices[0].x - SPACE_BETWEEN_DICES - WIDTH // 4 + WIDTH * 0.0625, HEIGHT - Y_COL * 0.5, "Quit - ESC", COURIERNEW_MEDIUM_BOLD, black)
    label_player1 = Label(X_SECOND_BIG_TEXT, Y_COL // 2, player1, COURIERNEW_SMALL_BOLD, black)
    label_player2 = Label(X_THIRD_BIG_TEXT, Y_COL // 2, player2, COURIERNEW_SMALL_BOLD, black)
    label_points_player1 = Label(X_SECOND_BIG_TEXT, HEIGHT - Y_COL // 2, game_variables["player1_points"], COURIERNEW_MEDIUM_BOLD, black)
    label_points_player2 = Label(X_THIRD_BIG_TEXT, HEIGHT - Y_COL // 2, game_variables["player2_points"], COURIERNEW_MEDIUM_BOLD, black)
    label_turn = Label(WIDTH * 0.7, HEIGHT * 0.1, "", COURIERNEW_MEDIUM_BOLD, black)

    button_throw = Button(dices[0].x - SPACE_BETWEEN_DICES - WIDTH // 4, HEIGHT // 2 - HEIGHT // 20, WIDTH * 0.125, HEIGHT // 10, black, grey, "Throw", COURIERNEW_MEDIUM_BOLD)

    run = True
    game_ended = False

    match_status = True
    check_match_status_count = 1

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        if not game_variables["loop_throw"]:
            if player1 == my_username:
                if game_variables["player1_throw"]:
                    if button_throw.loop():
                        game_variables["loop_throw"] = True

                        game_variables["player1_throw"] = False
                        game_variables["player1_choose"] = True

                        game_variables["num_of_throws"] += 1

                        upload_game_variables(True)

                elif game_variables["player1_choose"]:
                    if handle_select_player1():
                        game_variables["player1_choose"] = False
                        game_variables["player2_throw"] = True

                        upload_game_variables(True)
                        update_rows()

                else:
                    if check_match_status_count % (FPS // 6) == 0:
                        status = get_match_status()
                        if not status:
                            match_status = False
                            run = False
                        check_match_status_count = 1
                    check_match_status_count += 1

                    game_variables = download_game_variables()
                    update_rows()
                    update_dices()

            if player2 == my_username:
                if game_variables["player2_throw"]:
                    if button_throw.loop():
                        game_variables["loop_throw"] = True

                        game_variables["player2_throw"] = False
                        game_variables["player2_choose"] = True

                        game_variables["num_of_throws"] += 1

                        upload_game_variables(True)

                elif game_variables["player2_choose"]:
                    if handle_select_player2():
                        game_variables["player2_choose"] = False
                        game_variables["player1_throw"] = True

                        upload_game_variables(True)
                        update_rows()

                else:
                    if check_match_status_count % (FPS // 6) == 0:
                        status = get_match_status()
                        if not status:
                            match_status = False
                            run = False
                        check_match_status_count = 1
                    check_match_status_count += 1

                    game_variables = download_game_variables()
                    update_rows()
                    update_dices()

        else:
            game_variables["loop_count"] += 1

            if game_variables["loop_count"] % (FPS // 6) == 0:
                game_variables["dices"] = [random.randint(1, 6) for _ in range(5)]
                update_dices()

            if game_variables["loop_count"] == FPS * 2:
                game_variables["loop_throw"] = False
                game_variables["loop_count"] = 0

                if game_variables["player1_choose"] and my_username == player1 or game_variables["player2_choose"] and my_username == player2:
                    update_combinations_value_in_game_variables()

                    upload_game_variables(True)
                    update_dices()
                    update_rows()

        if game_variables["num_of_throws"] == 18 and game_variables["player1_throw"]:
            run = False
            game_ended = True

        draw_match()
        pygame.display.update()

    if game_ended:
        if my_username == player1:
            server.cwd("matches")
            server.delete(path)
            server.cwd("..")

        upload_request(f"{NAME_COMPUTER}%%%modify_status%%%", f"{my_username}%%%False%%%None%%%False%%%False%%%")

        pygame.time.wait(2000)
        show_after_match(game_variables, my_username, users)

    else:
        if not match_status:
            server.cwd("matches")
            server.delete(path)
            server.cwd("..")
        upload_request(f"{NAME_COMPUTER}%%%modify_status%%%", f"{my_username}%%%False%%%None%%%False%%%False%%%")
        show_menu(my_username)
def show_after_match(game_variables, my_username, users):
    screen.fill(white)

    win = False

    if game_variables["player1_points"] > game_variables["player2_points"]:
        if my_username == users[0]:
            win = True

    elif game_variables["player1_points"] < game_variables["player2_points"]:
        if my_username == users[1]:
            win = True

    else:
        win = "DRAW"


    if win == "DRAW":
        label = Label(WIDTH * 0.5, HEIGHT * 0.5, "You played draw!", COURIERNEW_BIG_BOLD, black)

    elif win:
        label = Label(WIDTH * 0.5, HEIGHT * 0.5, "Congratulations for winning!", COURIERNEW_BIG_BOLD, black)

    else:
        label = Label(WIDTH * 0.5, HEIGHT * 0.5, "You lost!", COURIERNEW_BIG_BOLD, black)

    label.draw()

    pygame.display.update()

    pygame.time.wait(3000)

    show_menu(my_username)
def show_menu(my_username):
    def draw_menu():
        screen.fill(white)

        label_logged_in_as.draw()
        label_searching.draw()
        label_you_have_been_invited_by.draw()
        label_player.draw()
        label_Quit_ESC.draw()

        button_search_for_game.draw()
        button_cancel.draw()

        if label_player.text != "":
            button_accept.draw()

        table.draw()

    def func_button_search_for_game():
        upload_request(f"{NAME_COMPUTER}%%%modify_status%%%", f"{my_username}%%%True%%%None%%%False%%%False%%%")

        label_searching.text = "searching"
        label_searching.update()

    def func_button_cancel():
        upload_request(f"{NAME_COMPUTER}%%%modify_status%%%", f"{my_username}%%%False%%%None%%%False%%%False%%%")

        label_searching.text = ""
        label_searching.update()

    def func_button_accept():
        upload_request(f"{NAME_COMPUTER}%%%modify_status%%%", f"{my_username}%%%False%%%{label_player.text}%%%False%%%False%%%")

    def check_for_invite(online_players_status):
        for user in online_players_status.keys():
            if online_players_status[user]["invite"] == my_username:
                label_you_have_been_invited_by.text = "You have been invited by: "
                label_player.text = user

                label_you_have_been_invited_by.update()
                label_player.update()
                break
        else:
            label_you_have_been_invited_by.text = ""
            label_player.text = ""

            label_you_have_been_invited_by.update()
            label_player.update()

    def check_for_match(online_players_status):
        nonlocal run, match
        for user in online_players_status.keys():
            if online_players_status[user]["invite"] == my_username and online_players_status[my_username]["invite"] == user:
                run = False
                match = sorted([my_username, user])

    label_logged_in_as = Label(WIDTH * 0.2, HEIGHT * 0.05, f"Logged in as {my_username}", COURIERNEW_MEDIUM_BOLD, black)
    label_searching = Label(WIDTH * 0.725, HEIGHT * 0.25, "", COURIERNEW_MEDIUM_BOLD, black)
    label_you_have_been_invited_by = Label(WIDTH * 0.68 + WIDTH * 0.045, HEIGHT * 0.03, "", COURIERNEW_MEDIUM_BOLD, black)
    label_player = Label(WIDTH * 0.68 + WIDTH * 0.045, HEIGHT * 0.08, "", COURIERNEW_MEDIUM_BOLD, black)
    label_Quit_ESC = Label(WIDTH - 2 * SPACE_BETWEEN_DICES - WIDTH_DICE - SPACE_BETWEEN_DICES - WIDTH // 4 + WIDTH * 0.0625, HEIGHT - Y_COL * 0.5,"Quit - ESC", COURIERNEW_MEDIUM_BOLD, black)

    button_search_for_game = Button(WIDTH * 0.6, HEIGHT * 0.3, WIDTH * 0.25, HEIGHT * 0.1, black, grey, "Search for game", COURIERNEW_MEDIUM_BOLD, func_button_search_for_game)
    button_cancel = Button(WIDTH * 0.65, HEIGHT * 0.42, WIDTH * 0.15, HEIGHT * 0.1, black, grey, "Cancel", COURIERNEW_MEDIUM_BOLD, func_button_cancel)
    button_accept = Button(WIDTH * 0.68, HEIGHT * 0.15, WIDTH * 0.09, HEIGHT * 0.08, black, green, "ACCEPT", COURIERNEW_MEDIUM_BOLD, func_button_accept)

    table = Table(WIDTH * 0.05, HEIGHT * 0.15, 10, COURIERNEW_MEDIUM_BOLD, black, my_username)

    match = []
    run = True

    request_get_online_players_status_sent = False
    online_players_status = None

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        if request_get_online_players_status_sent:
            online_players_status = download_response_for_user(f"{NAME_COMPUTER}%%%get_online_players_status%%%")
            if online_players_status is not None:
                online_players_status = eval(online_players_status)
                table.update(online_players_status)
                request_get_online_players_status_sent = False
        else:
            upload_request(f"{NAME_COMPUTER}%%%get_online_players_status%%%", "___%%%True%%%")
            request_get_online_players_status_sent = True

        if online_players_status is not None:
            check_for_invite(online_players_status)
            check_for_match(online_players_status)

        button_search_for_game.loop()
        button_cancel.loop()
        button_accept.loop()

        ret_table = table.loop()
        if ret_table != None:
            upload_request(f"{NAME_COMPUTER}%%%modify_status%%%", f"{my_username}%%%False%%%{ret_table}%%%False%%%False%%%")

        draw_menu()
        pygame.display.update()

    if len(match) == 2:
        upload_request(f"{NAME_COMPUTER}%%%modify_status%%%", f"{my_username}%%%False%%%None%%%True%%%False%%%")
        show_match(match, my_username)
    else:
        upload_request(f"{NAME_COMPUTER}%%%remove_status%%%", f"{my_username}%%%False%%%")
        show_login()
def show_login():
    def draw_login():
        screen.fill(white)

        label_please_log_in.draw()
        label_dont_have_an_account_yet.draw()
        label_error.draw()

        input_username.draw()
        input_password.draw()

        button_login.draw()
        button_register.draw()
        button_play_offline.draw()

    def func_button_login():
        nonlocal run, menu

        upload_request(f"{NAME_COMPUTER}%%%login%%%", f"{input_username.text}%%%{input_password.text}%%%True%%%")

        response = None
        while response is None:
            response = download_response_for_user(f"{NAME_COMPUTER}%%%login%%%")

        if response != "Done!":
            label_error.text = response
            label_error.update()
        else:
            run = False
            menu = True

    def func_button_register():
        nonlocal run, register

        run = False
        register = True

    def play_offline():
        offlinegame = offlinegamefile.Game()
        offlinegame.show_menu()

    label_please_log_in = Label(WIDTH * 0.5, HEIGHT * 0.1, "Please log in!", COURIERNEW_BIG_BOLD, black)
    label_dont_have_an_account_yet = Label(WIDTH * 0.4, HEIGHT * 0.9, "Don't have an account yet?", COURIERNEW_SMALL_BOLD, black)
    label_error = Label(WIDTH * 0.5, HEIGHT * 0.65, "", COURIERNEW_MEDIUM_BOLD, red)

    input_username = TextInput(WIDTH * 0.5, HEIGHT * 0.35, COURIERNEW_BIG, 15, grey, green, black, "Username", COURIERNEW_BIG_BOLD)
    input_password = TextInput(WIDTH * 0.5, HEIGHT * 0.55, COURIERNEW_BIG, 25, grey, green, black, "Password", COURIERNEW_BIG_BOLD, is_password=True)

    button_login = Button(WIDTH * 0.4, HEIGHT * 0.7, WIDTH * 0.2, HEIGHT * 0.1, black, grey, "Log in", COURIERNEW_BIG_BOLD, func_button_login)
    button_register = Button(WIDTH * 0.53, HEIGHT * 0.875, WIDTH * 0.1, HEIGHT * 0.05, black, grey, "Register", COURIERNEW_SMALL_BOLD, func_button_register)
    button_play_offline = Button(WIDTH * 0.8, HEIGHT * 0.9, WIDTH * 0.2, HEIGHT * 0.1, black, grey, "Play offline", COURIERNEW_MEDIUM_BOLD, play_offline)

    menu = False
    register = False

    run = True
    while run:
        clock.tick(FPS)
        pressed_key = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                elif event.unicode.isalpha() or event.unicode.isdigit():
                    pressed_key = event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    pressed_key = "backspace"

        input_username.loop(pressed_key)
        input_password.loop(pressed_key)

        button_login.loop()
        button_register.loop()
        button_play_offline.loop()

        draw_login()
        pygame.display.update()

    if menu:
        show_menu(input_username.text)
    elif register:
        show_register()
def show_register():
    def draw_register():
        screen.fill(white)

        label_please_register.draw()
        label_error.draw()

        input_username.draw()
        input_email.draw()
        input_password.draw()
        input_password_again.draw()

        button_register.draw()

    def func_button_register():
        nonlocal run

        upload_request(f"{NAME_COMPUTER}%%%register%%%", f"{input_username.text}%%%{input_email.text}%%%{input_password.text}%%%{input_password_again.text}%%%True%%%")

        response = None

        while response is None:
            response = download_response_for_user(f"{NAME_COMPUTER}%%%register%%%")

        if response != "Done!":
            label_error.text = response
            label_error.update()
        else:
            run = False

    label_please_register = Label(WIDTH * 0.5, HEIGHT * 0.1, "Please register!", COURIERNEW_BIG_BOLD, black)
    label_error = Label(WIDTH * 0.5, HEIGHT * 0.95, "", COURIERNEW_MEDIUM_BOLD, red)

    input_username = TextInput(WIDTH * 0.5, HEIGHT * 0.3, COURIERNEW_MEDIUM, 15, grey, green, black, "Username", COURIERNEW_MEDIUM_BOLD)
    input_email = TextInput(WIDTH * 0.5, HEIGHT * 0.45, COURIERNEW_MEDIUM, 40, grey, green, black, "E-mail", COURIERNEW_MEDIUM_BOLD)
    input_password = TextInput(WIDTH * 0.5, HEIGHT * 0.6, COURIERNEW_MEDIUM, 25, grey, green, black, "Password", COURIERNEW_MEDIUM_BOLD, is_password=True)
    input_password_again = TextInput(WIDTH * 0.5, HEIGHT * 0.75, COURIERNEW_MEDIUM, 25, grey, green, black, "Password again", COURIERNEW_MEDIUM_BOLD, is_password=True)

    button_register = Button(WIDTH * 0.4, HEIGHT * 0.83, WIDTH * 0.2, HEIGHT * 0.08, black, grey, "Register", COURIERNEW_MEDIUM_BOLD, func_button_register)

    run = True
    while run:
        clock.tick(FPS)
        pressed_key = None
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_BACKSPACE:
                    pressed_key = "backspace"
                else:
                    pressed_key = event.unicode

        input_username.loop(pressed_key)
        input_email.loop(pressed_key)
        input_password.loop(pressed_key)
        input_password_again.loop(pressed_key)

        button_register.loop()

        draw_register()
        pygame.display.update()

    show_login()


server.cwd("versions")
files = list_dir()
new_version = float(files[-1].replace("yahtzee_", "").replace(".exe", ""))
if new_version > VERSION:
    server.retrbinary(f"RETR {files[-1]}", open(f"yahtzee_{new_version}.exe", "wb").write)
    server.quit()
else:
    server.cwd("..")
    show_login()
    server.quit()

import pygame
import random
pygame.init()

DISPLAY_INFO = pygame.display.Info()
WIDTH, HEIGHT = DISPLAY_INFO.current_w, DISPLAY_INFO.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FPS = 60

combinations = ["Sum", "Pair", "Drill", "Two pair", "Four of a kind", "Full", "Small straight", "Big straight", "Five of a kind"]

WIDTH_DICE = HEIGHT // 7
SPACE_BETWEEN_DICES = (HEIGHT - WIDTH_DICE * 5) // 10

WIDTH_ROW = WIDTH // 3
HEIGHT_ROW = HEIGHT // (len(combinations) * 1.3)

SPACE_BETWEEN_ROWS = HEIGHT_ROW // 10

WIDTH_FIRST_COLUMN = WIDTH_ROW // 2
WIDTH_SECOND_COLUMN = WIDTH_ROW // 4
WIDTH_THIRD_COLUMN = WIDTH_SECOND_COLUMN

X_FIRST_COL = WIDTH // 7
X_SECOND_COL = X_FIRST_COL + WIDTH_FIRST_COLUMN
X_THIRD_COL = X_SECOND_COL + WIDTH_SECOND_COLUMN
Y_COL = (HEIGHT - HEIGHT_ROW * len(combinations) - (len(combinations) - 1) * SPACE_BETWEEN_ROWS) // 2

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

WIDTH_DIFFICULTY_BUTTONS = WIDTH // 10
HEIGHT_DIFFICULTY_BUTTONS = HEIGHT // 10

WIDTH_START_BUTTON = WIDTH // 5
HEIGHT_START_BUTTON = HEIGHT // 5

WIDTH_CONTINUE_BUTTON = WIDTH_DIFFICULTY_BUTTONS // 1.5
HEIGHT_CONTINUE_BUTTON = HEIGHT_DIFFICULTY_BUTTONS // 1.5

WIDTH_THROW_BUTTON = WIDTH // 8
HEIGHT_THROW_BUTTON = HEIGHT // 10


FONT_BIG_VALUE = pygame.font.SysFont("comicsans", WIDTH // 25)
FONT_BIG_VALUE_BOLD = pygame.font.SysFont("comicsans", WIDTH // 25, bold=True)
FONT_MEDIUM_VALUE = pygame.font.SysFont("comicsans", WIDTH // 50)
FONT_MEDIUM_VALUE_BOLD = pygame.font.SysFont("comicsans", WIDTH // 50, bold=True)
FONT_SMALL_VALUE = pygame.font.SysFont("comicsans", WIDTH // 75)
FONT_SMALL_VALUE_BOLD = pygame.font.SysFont("comicsans", WIDTH // 75, bold=True)

BACKGROUND_MENU = pygame.image.load("datas/pictures/menu_background.jpg").convert_alpha()
BACKGROUND_GAME = pygame.image.load("datas/pictures/game_background.jpg").convert_alpha()
BACKGROUND_DICE = pygame.image.load("datas/pictures/dice_background.jpg").convert_alpha()
BACKGROUND_GREEN = pygame.image.load("datas/pictures/green_background.jpg").convert_alpha()
BACKGROUND_GREY = pygame.image.load("datas/pictures/grey_background.jpg").convert_alpha()
BACKGROUND_RED = pygame.image.load("datas/pictures/red_background.jpg").convert_alpha()

BACKGROUND_MENU = pygame.transform.scale(BACKGROUND_MENU, (WIDTH, HEIGHT))
BACKGROUND_GAME = pygame.transform.scale(BACKGROUND_GAME, (WIDTH, HEIGHT))
BACKGROUND_DICE = pygame.transform.scale(BACKGROUND_DICE, (WIDTH_DICE, WIDTH_DICE))
BACKGROUND_START_BUTTON = pygame.transform.scale(BACKGROUND_GREEN, (WIDTH_START_BUTTON, HEIGHT_START_BUTTON))
BACKGROUND_DIFF_BUTTON_GREEN = pygame.transform.scale(BACKGROUND_GREEN, (WIDTH_DIFFICULTY_BUTTONS, HEIGHT_DIFFICULTY_BUTTONS))
BACKGROUND_DIFF_BUTTON_GREY = pygame.transform.scale(BACKGROUND_GREY, (WIDTH_DIFFICULTY_BUTTONS, HEIGHT_DIFFICULTY_BUTTONS))
BACKGROUND_CONTINUE_BUTTON = pygame.transform.scale(BACKGROUND_RED, (WIDTH_CONTINUE_BUTTON, HEIGHT_CONTINUE_BUTTON))
BACKGROUND_THROW_BUTTON = pygame.transform.scale(BACKGROUND_GREY, (WIDTH_THROW_BUTTON, HEIGHT_THROW_BUTTON))

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

        screen.blit(BACKGROUND_DICE, (self.x, self.y))

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

    def update_value(self):
        self.value = random.randint(1, 6)
class Row:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

        self.reset()

    def reset(self):
        self.val_player = ""
        self.val_computer = ""

        self.val_player_notselected = ""
        self.val_computer_notselected = ""

    def update_not_selected_values(self, combinations_points, player_choose, computer_choose):
        if self.name not in combinations_points.keys():
            self.val_player_notselected = ""
            self.val_computer_notselected = ""

        else:
            if player_choose:
                self.val_player_notselected = combinations_points[self.name]
                self.val_computer_notselected = ""

            elif computer_choose:
                self.val_computer_notselected = combinations_points[self.name]
                self.val_player_notselected = ""

    def draw(self, computer_choose, player_choose):
        pygame.draw.rect(screen, black, (self.x, self.y, WIDTH_ROW, HEIGHT_ROW), width=WIDTH // 250)
        pygame.draw.line(screen, black, (X_SECOND_COL, self.y), (X_SECOND_COL, self.y + HEIGHT_ROW - 1), width=WIDTH // 250)
        pygame.draw.line(screen, black, (X_THIRD_COL, self.y), (X_THIRD_COL, self.y + HEIGHT_ROW - 1), width=WIDTH // 250)

        text_name = FONT_MEDIUM_VALUE_BOLD.render(self.name, True, black)

        text_val_computer = FONT_MEDIUM_VALUE_BOLD.render(str(self.val_computer), True, black)
        text_val_player = FONT_MEDIUM_VALUE_BOLD.render(str(self.val_player), True, black)

        text_not_selected_value_computer = FONT_SMALL_VALUE_BOLD.render(str(self.val_computer_notselected), True, black)
        text_not_selected_value_player = FONT_SMALL_VALUE_BOLD.render(str(self.val_player_notselected), True, black)

        screen.blit(text_name, (X_FIRST_TEXT - text_name.get_width() // 2, self.y + HEIGHT_ROW // 2 - text_name.get_height() // 2))

        screen.blit(text_val_computer, (X_SECOND_BIG_TEXT - text_val_computer.get_width() // 2, self.y + HEIGHT_ROW // 2 - text_val_computer.get_height() // 2))
        screen.blit(text_val_player, (X_THIRD_BIG_TEXT - text_val_player.get_width() // 2, self.y + HEIGHT_ROW // 2 - text_val_player.get_height() // 2))

        if computer_choose:
            screen.blit(text_not_selected_value_computer, (X_SECOND_SMALL_TEXT - text_not_selected_value_computer.get_width() // 2, self.y + SPACE_BETWEEN_LINE_AND_SMALL_TEXT - text_not_selected_value_computer.get_height() // 2))
        if player_choose:
            screen.blit(text_not_selected_value_player, (X_THIRD_SMALL_TEXT - text_not_selected_value_player.get_width() // 2, self.y + SPACE_BETWEEN_LINE_AND_SMALL_TEXT - text_not_selected_value_player.get_height() // 2))

class Button:
    def __init__(self, x, y, width, height, color, text, bgs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.bgs = bgs

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect_shadow = pygame.Rect(self.rect.x + self.width // 20, self.rect.y + self.height // 20,
                                       self.width * 18 // 20, self.height * 18 // 20)

        self.pressed = False

    def draw(self):
        screen.blit(self.bgs[self.color], (self.x, self.y))

        if self.pressed:
            pygame.draw.rect(screen, [color / 2 for color in self.color], self.rect_shadow, width=WIDTH // 300)

        screen.blit(self.text, (self.x + self.width // 2 - self.text.get_width() // 2, self.y + self.height // 2 - self.text.get_height() // 2))

    def loop(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.pressed = True

        elif self.pressed:
            self.pressed = False
            return True

        return False
class Game:
    def __init__(self):
        self.dices = []
        y = SPACE_BETWEEN_DICES
        for _ in range(5):
            self.dices.append(Dice(int(WIDTH - 2 * SPACE_BETWEEN_DICES - WIDTH_DICE), y, HEIGHT // 7))
            y += 2 * SPACE_BETWEEN_DICES + WIDTH_DICE

        self.player_s_rectangles = []
        self.rows = []
        y = Y_COL
        for name in combinations:
            self.player_s_rectangles.append(pygame.Rect(X_THIRD_COL, y, WIDTH_ROW // 4, HEIGHT_ROW))

            self.rows.append(Row(X_FIRST_COL, y, name))
            y += HEIGHT_ROW + SPACE_BETWEEN_ROWS

        self.combinations_points = {}
        self.reset_variables()
    def reset_variables(self):
        self.game_variables = {"username": None, "difficulty": None, "computer_points": 0, "player_points": 0,
                               "num_of_throws": 0,
                               "computer_throw": True, "computer_choose": False, "player_throw": False,
                               "player_choose": False}
        for row in self.rows:
            row.reset()

        for dice in self.dices:
            dice.value = 1
    def edit_leaderboard(self, winner):
        file = open("datas/leaderboard.txt", "r", encoding="utf-8")
        data = file.readlines()
        file.close()

        names_scores = {}

        top = False

        for row in data:
            name, score = row.strip().split(",")
            score = int(score)

            names_scores[name] = score

        winner_name, winner_score = winner

        if winner_name in names_scores.keys():
            names_scores[winner_name] = winner_score if winner_score > names_scores[winner_name] else names_scores[
                winner_name]
        else:
            names_scores[winner_name] = winner_score

        names_scores = dict(sorted(names_scores.items(), key=lambda item: (-item[1], item[0])))

        if len(names_scores) > 10:
            names_scores.pop(list(names_scores.keys())[-1])

        if winner_name in names_scores.keys():
            top = True

        file = open("datas/leaderboard.txt", "w", encoding="utf-8")
        index = 0
        for name, score in names_scores.items():
            if index < len(names_scores) - 1:
                file.write(f"{name},{score}\n")
            else:
                file.write(f"{name},{score}")
            index += 1
        file.close()

        return top
    def update_combinations_points(self):
        def count_number(num):
            count = 0
            for val in values:
                if val == num:
                    count += 1
            return count

        values = [dice.value for dice in self.dices]

        noduplicates_values = sorted(set(values))
        counts = [count_number(val) for val in noduplicates_values]

        noduplicates_values = noduplicates_values[::-1]
        counts = counts[::-1]

        self.combinations_points = {}

        for index_combination, combination in enumerate(combinations):

            if self.game_variables["player_choose"] and self.rows[index_combination].val_player != "":
                continue

            elif self.game_variables["computer_choose"] and self.rows[index_combination].val_computer != "":
                continue

            points = 0

            if index_combination == 0:
                points = sum(values)

            elif index_combination == 1:
                for index, count in enumerate(counts):
                    if count >= 2:
                        points = noduplicates_values[index] * 2
                        break

            elif index_combination == 2:
                for index, count in enumerate(counts):
                    if count >= 3:
                        points = noduplicates_values[index] * 3
                        break

            elif index_combination == 3:
                pairs = []
                for index, count in enumerate(counts):
                    if count >= 2:
                        pairs.append(noduplicates_values[index])

                if len(pairs) >= 2:
                    points = (pairs[0] + pairs[1]) * 2

            elif index_combination == 4:
                for index, count in enumerate(counts):
                    if count >= 4:
                        points = noduplicates_values[index] * 4
                        break

            elif index_combination == 5:
                if counts == [3, 2] or counts == [2, 3]:
                    points = sum(values)

            elif index_combination == 6:
                if noduplicates_values == [5, 4, 3, 2, 1]:
                    points = 15

            elif index_combination == 7:
                if noduplicates_values == [6, 5, 4, 3, 2]:
                    points = 20

            elif index_combination == 8:
                if len(noduplicates_values) == 1:
                    points = 50

            self.combinations_points[combination] = points
    def handle_select_computer(self):
        row = None

        if self.game_variables["difficulty"] == 0:
            if sum(self.combinations_points.values()) == 0:
                for row in self.rows:
                    if row.val_computer == "":
                        row.val_computer = 0
                        break
            else:
                for row in self.rows:
                    if row.name in self.combinations_points and row.val_computer == "" and self.combinations_points[row.name] > 0:
                        row.val_computer = self.combinations_points[row.name]
                        break
        else:
            if sum(self.combinations_points.values()) == 0:
                for row in self.rows[::-1]:
                    if row.val_computer == "":
                        row.val_computer = 0
                        break
            else:
                point = max(self.combinations_points.values())
                for row in self.rows:
                    if row.val_computer == "" and self.combinations_points[row.name] == point:
                        row.val_computer = point
                        break

        self.game_variables["computer_points"] += row.val_computer
    def handle_select_player(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            for index, rect in enumerate(self.player_s_rectangles):
                if rect.collidepoint(pos):
                    row = self.rows[index]
                    if row.val_player == "":
                        row.val_player = self.combinations_points[row.name]
                        self.game_variables["player_points"] += row.val_player
                        return True
        return False
    def load_game(self):
        def load_dictionary():
            dictionary = {}
            datas = file.readline().split(",")[:-1]
            for index in range(0, len(datas), 2):
                value = datas[index + 1]
                if value.isdigit():
                    value = int(value)
                elif value == "True":
                    value = True
                elif value == "False":
                    value = False
                dictionary[datas[index]] = value
            return dictionary

        file = open("datas/savedgame.txt", "r", encoding="utf-8")

        self.game_variables = load_dictionary()
        self.combinations_points = load_dictionary()

        for row in self.rows:
            row.val_computer, row.val_player, row.val_computer_notselected, row.val_player_notselected = [int(data) if data.isdigit() else data for data in file.readline().split(",")[:-1]]

        for dice in self.dices:
            dice.value = int(file.readline().strip())

        file.close()

        open("datas/savedgame.txt", "w", encoding="utf-8")
    def save_game(self):
        def save_dict(dictionary):
            text = ""
            for key, value in dictionary.items():
                text += f"{key},{str(value)},"

            file.write(text + "\n")

        file = open("datas/savedgame.txt", "w", encoding="utf-8")

        save_dict(self.game_variables)
        save_dict(self.combinations_points)

        for row in self.rows:
            file.write(
                f"{row.val_computer},{row.val_player},{row.val_computer_notselected},{row.val_player_notselected},\n")

        for dice in self.dices:
            file.write(str(dice.value) + "\n")

        file.close()
    def draw_menu_screen(self, leaderboard, username, easy_button, hard_button, start_button, has_saved_game, continue_button):
        screen.blit(BACKGROUND_MENU, (0, 0))

        text_esc = FONT_MEDIUM_VALUE_BOLD.render("Quit - ESC", True, black)
        screen.blit(text_esc, (WIDTH * 2 // 3 - text_esc.get_width() // 2, HEIGHT - Y_COL - text_esc.get_height() // 2))

        text_leaderboard = FONT_BIG_VALUE_BOLD.render("Leaderboard", True, black)
        screen.blit(text_leaderboard, (WIDTH // 10, HEIGHT // 20 - text_leaderboard.get_height() // 2))

        num = 1
        y = HEIGHT // 6
        for name, point in leaderboard.items():
            text_name = FONT_MEDIUM_VALUE_BOLD.render(name, True, black)
            text_point = FONT_MEDIUM_VALUE_BOLD.render(str(point), True, black)
            text_num = FONT_MEDIUM_VALUE_BOLD.render(str(num) + ".", True, black)

            screen.blit(text_name, (WIDTH // 10, y - text_name.get_height() // 2))
            screen.blit(text_point, (WIDTH // 3.5 - text_point.get_width() // 2, y - text_point.get_height() // 2))
            screen.blit(text_num, (WIDTH // 20, y - text_num.get_height() // 2))

            num += 1
            y += HEIGHT // 20

        text_label_username = FONT_BIG_VALUE_BOLD.render("Please enter your username:", True, black)
        text_username = FONT_BIG_VALUE_BOLD.render(username, True, black)

        screen.blit(text_label_username,
                    (WIDTH * 2 // 3 - text_label_username.get_width() // 2,
                     HEIGHT // 5 - text_label_username.get_height() // 2))
        screen.blit(text_username,
                    (WIDTH * 2 // 3 - text_username.get_width() // 2, HEIGHT // 3 - text_username.get_height() // 2))

        easy_button.draw()
        hard_button.draw()
        start_button.draw()

        if has_saved_game:
            text_saved_game = FONT_MEDIUM_VALUE_BOLD.render("Do you want to continue your saved game?", True, black)

            screen.blit(text_saved_game,
                        (WIDTH // 1.7 - text_saved_game.get_width() // 2, HEIGHT // 15 - text_saved_game.get_height() // 2))

            continue_button.draw()
    def show_menu(self):
        self.reset_variables()
        leaderboard = {}
        try:
            file = open("datas/leaderboard.txt", "r", encoding="utf-8")

            for row in file:
                name, score = row.strip().split(",")
                leaderboard[name] = score

            file.close()
        except:
            open("datas/leaderboard.txt", "w", encoding="utf-8")

        has_saved_game = False
        try:
            if len(open("datas/savedgame.txt", "r", encoding="utf-8").readlines()) != 0:
                has_saved_game = True
        except:
            pass

        easy_button = Button(WIDTH * 7 // 12 - WIDTH_DIFFICULTY_BUTTONS // 2,
                                       HEIGHT // 2 - HEIGHT_DIFFICULTY_BUTTONS // 2, WIDTH_DIFFICULTY_BUTTONS,
                                       HEIGHT_DIFFICULTY_BUTTONS, grey, FONT_MEDIUM_VALUE_BOLD.render("Easy", True, black), {green: BACKGROUND_DIFF_BUTTON_GREEN,
                                                                                                                              grey: BACKGROUND_DIFF_BUTTON_GREY})

        hard_button = Button(WIDTH * 9 // 12 - WIDTH_DIFFICULTY_BUTTONS // 2,
                                       HEIGHT // 2 - HEIGHT_DIFFICULTY_BUTTONS // 2, WIDTH_DIFFICULTY_BUTTONS,
                                       HEIGHT_DIFFICULTY_BUTTONS, grey, FONT_MEDIUM_VALUE_BOLD.render("Hard", True, black), {green: BACKGROUND_DIFF_BUTTON_GREEN,
                                                                                                                              grey: BACKGROUND_DIFF_BUTTON_GREY})

        start_button = Button(WIDTH * 8 // 12 - WIDTH_START_BUTTON // 2,
                                        HEIGHT * 3 // 4 - HEIGHT_START_BUTTON // 2, WIDTH_START_BUTTON,
                                        HEIGHT_START_BUTTON, green, FONT_BIG_VALUE_BOLD.render("Start", True, black), {green: BACKGROUND_START_BUTTON})

        continue_button = Button(WIDTH * 25 // 26 - WIDTH_START_BUTTON // 2,
                                        HEIGHT // 7.6 - HEIGHT_START_BUTTON // 2, WIDTH_CONTINUE_BUTTON,
                                        HEIGHT_CONTINUE_BUTTON, red, FONT_SMALL_VALUE_BOLD.render("Continue", True, black), {red: BACKGROUND_CONTINUE_BUTTON})

        run = True

        username = ""
        difficulty = None

        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        run = False

                    if (event.unicode.isalpha() or event.unicode.isdigit()) and len(username) < 9:
                        username += event.unicode

                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]

            if continue_button.loop() and has_saved_game:
                self.load_game()
                self.show_game()
                return

            elif easy_button.loop():
                easy_button.color = green
                hard_button.color = grey

                difficulty = 0

            elif hard_button.loop():
                easy_button.color = grey
                hard_button.color = green

                difficulty = 1

            elif start_button.loop() and username != "" and not difficulty == None:
                self.game_variables["username"] = username
                self.game_variables["difficulty"] = difficulty

                self.show_game()
                return

            self.draw_menu_screen(leaderboard, username, easy_button, hard_button, start_button, has_saved_game, continue_button)

            pygame.display.update()

        if __name__ == "__main__":
            pygame.quit()
    def throw(self, count):
        if count != 0 and count < round(1.5 * FPS, 0):
            count += 1
            if count % (FPS // 6) == 0:
                for dice in self.dices:
                    dice.update_value()

            if count == round(1.5 * FPS, 0):
                self.update_combinations_points()
                for row in self.rows:
                    row.update_not_selected_values(self.combinations_points, self.game_variables["player_choose"], self.game_variables["computer_choose"])

            return True, count
        else:
            return False, 0
    def draw_game_screen(self, throw_button):
        screen.blit(BACKGROUND_GAME, (0, 0))

        text_esc = FONT_MEDIUM_VALUE_BOLD.render("Quit - ESC", True, black)
        screen.blit(text_esc, (self.dices[0].x - SPACE_BETWEEN_DICES - WIDTH // 4, HEIGHT - Y_COL // 2 - text_esc.get_height() // 2))

        if self.game_variables["computer_throw"] or self.game_variables["computer_choose"]:
            text_computer = FONT_SMALL_VALUE_BOLD.render("COMPUTER", True, purple)
            text_player = FONT_SMALL_VALUE.render(self.game_variables["username"], True, black)
        else:
            text_computer = FONT_SMALL_VALUE.render("COMPUTER", True, black)
            text_player = FONT_SMALL_VALUE_BOLD.render(self.game_variables["username"], True, purple)

        screen.blit(text_computer,
                    (X_SECOND_BIG_TEXT - text_computer.get_width() // 2, Y_COL // 2 - text_computer.get_height() // 2))
        screen.blit(text_player,
                    (X_THIRD_BIG_TEXT - text_player.get_width() // 2, Y_COL // 2 - text_player.get_height() // 2))

        text_computer_points = FONT_MEDIUM_VALUE_BOLD.render(str(self.game_variables["computer_points"]), True, black)
        text_player_points = FONT_MEDIUM_VALUE_BOLD.render(str(self.game_variables["player_points"]), True, black)

        screen.blit(text_computer_points,
                    (X_SECOND_BIG_TEXT - text_computer_points.get_width() // 2,
                     HEIGHT - Y_COL // 2 - text_computer_points.get_height() // 2))
        screen.blit(text_player_points,
                    (X_THIRD_BIG_TEXT - text_player_points.get_width() // 2,
                     HEIGHT - Y_COL // 2 - text_player_points.get_height() // 2))

        for dice in self.dices:
            dice.draw()

        for row in self.rows:
            row.draw(self.game_variables["computer_choose"], self.game_variables["player_choose"])

        if self.game_variables["player_throw"] or self.game_variables["player_choose"]:
            throw_button.draw()
    def show_game(self):
        run = True
        quit_game = False

        throw_button = Button(self.dices[0].x - SPACE_BETWEEN_DICES - WIDTH // 4, HEIGHT // 2 - HEIGHT // 20,
                              WIDTH_THROW_BUTTON, HEIGHT_THROW_BUTTON, grey, FONT_MEDIUM_VALUE_BOLD.render("Throw", True, black), {grey: BACKGROUND_THROW_BUTTON})
        throw_count = 0

        while run:
            clock.tick(FPS)

            throw_loop, throw_count = self.throw(throw_count)

            for event in pygame.event.get():
                pass

            if pygame.key.get_pressed()[pygame.K_ESCAPE] and not throw_loop:
                quit_game = True
                break

            self.draw_game_screen(throw_button)

            pygame.display.update()

            if not throw_loop:

                if self.game_variables["computer_throw"]:
                    pygame.time.wait(1000)
                    throw_count = 1

                    self.game_variables["computer_throw"] = False
                    self.game_variables["computer_choose"] = True

                    self.game_variables["num_of_throws"] += 1

                elif self.game_variables["computer_choose"]:
                    pygame.time.wait(2000)
                    self.handle_select_computer()

                    self.game_variables["computer_choose"] = False
                    self.game_variables["player_throw"] = True

                elif self.game_variables["player_throw"]:
                    if throw_button.loop():
                        throw_count = 1
                        self.game_variables["player_throw"] = False
                        self.game_variables["player_choose"] = True

                        self.game_variables["num_of_throws"] += 1

                elif self.game_variables["player_choose"]:
                    if self.handle_select_player():
                        self.game_variables["player_choose"] = False
                        self.game_variables["computer_throw"] = True

                        if self.game_variables["num_of_throws"] == 18:
                            run = False

        if quit_game:
            self.save_game()
            self.show_menu()

        else:
            self.draw_game_screen(throw_button)

            pygame.display.update()

            pygame.time.wait(500)

            self.show_after_game()
    def show_after_game(self):

        open("datas/savedgame.txt", "w", encoding="utf-8")

        top = False

        text_top = ""

        if self.game_variables["player_points"] != self.game_variables["computer_points"]:
            winner = (self.game_variables["username"], self.game_variables["player_points"]) if self.game_variables["player_points"] > self.game_variables["computer_points"] else ("COMPUTER", self.game_variables["computer_points"])
            top = self.edit_leaderboard(winner)

        if self.game_variables["player_points"] > self.game_variables["computer_points"]:
            text_winner = f"Congratulations {self.game_variables['username']}, you won!"
            if top:
                text_top = "You are on the leaderboard!"

        elif self.game_variables["player_points"] < self.game_variables["computer_points"]:
            text_winner = "The computer has won!"
            if top:
                text_top = "It is now on the leaderboard!"

        else:
            text_winner = f"You played a draw!"

        screen.blit(BACKGROUND_GAME, (0, 0))

        text_winner = FONT_BIG_VALUE.render(text_winner, True, black)
        text_top = FONT_BIG_VALUE.render(text_top, True, black)

        screen.blit(text_winner, (WIDTH // 2 - text_winner.get_width() // 2, HEIGHT // 3 - text_winner.get_height() // 2))
        screen.blit(text_top, (WIDTH // 2 - text_top.get_width() // 2, HEIGHT * 2 // 3 - text_top.get_height() // 2))

        pygame.display.update()

        pygame.time.wait(5000)

        self.show_menu()

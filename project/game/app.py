import pygame

import datetime
import sys
import pathlib
import random
import os

import project.game.style as style
import project.db.tables as tables
import project.game.funcs as funcs


class App:
    def __init__(self, screen, session):
        self.board = None
        self.chances = None
        self.level = None
        self.value = None
        self.cell_size = None
        self.margin = None
        self.board = None
        self.ulta_delete_active = None
        self.points = None
        self.steps = None
        self.start_balance = None
        self.best_score = None

        self.session = session

        self.base_dir = pathlib.Path(__file__).parent.parent
        print(self.base_dir)
        self.move_sounds = [
            pygame.mixer.Sound(
                os.path.join(
                    self.base_dir,
                    "data",
                    "music",
                    f"move_music_{i}.wav",
                ),
            )
            for i in range(1, 4)
        ]

        self.click_sound = pygame.mixer.Sound(
            os.path.join(
                self.base_dir,
                "data",
                "music",
                "click_music.wav",
            ),
        )

        self.screen = screen
        self.screen_size = screen.get_size()

        self.update_settings_and_refresh(1)

        self.start_page()

    def check_valid_cell(self, cell):
        i, j = cell
        i, j = int(i), int(j)
        return self.board[i][j] != 0

    def check_money_for_ulta(self, need_money):
        return funcs.gem_assist.get_balance() >= need_money

    def render_cells(self):
        """Метод, который отображает все поле"""
        for i in range(self.value):
            for j in range(self.value):
                self.render_cell(i, j)

    def render_decoration(self, draw_back_button=False, draw_ulta_red=False):
        width, height = self.screen_size

        # <===== Надпись размер поля =====>
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        text = font.render(
            f"{self.value} x {self.value}",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text = width // 2 - text.get_width() // 2
        button_y_text = 130 - text.get_height() // 2

        self.screen.blit(text, (button_x_text, button_y_text))
        # <===== Надпись размер поля =====>

        # <===== Твой баланс =====>
        pygame.draw.rect(
            self.screen,
            style.S_TABLE_SCORE,
            (40, 10, 150, 60),
            0,
            5,
        )
        pygame.draw.rect(
            self.screen,
            style.S_TABLE_SCORE_BORDER,
            (40, 10, 150, 60),
            5,
            5,
        )
        font = pygame.font.SysFont(
            "spendthrift",
            30,
        )
        text = font.render(
            "Баланс",
            True,
            style.S_TABLE_SCORE_TEXT,
        )

        button_x_text = 115 - text.get_width() // 2
        button_y_text = 28 - text.get_height() // 2

        self.screen.blit(
            text,
            (button_x_text, button_y_text),
        )

        font = pygame.font.SysFont(
            "spendthrift",
            30,
        )
        col_text = font.render(
            f"{funcs.gem_assist.get_balance()}",
            True,
            style.S_TABLE_SCORE_TEXT_VALUE,

        )

        button_x_text = 115 - col_text.get_width() // 2
        button_y_text = 48 - col_text.get_height() // 2

        self.screen.blit(
            col_text,
            (button_x_text, button_y_text),
        )

        # Дальше G
        font = pygame.font.SysFont(
            "spendthrift",
            30,
        )
        g_text = font.render(
            "G",
            True,
            style.S_TABLE_SCORE_TEXT_VALUE_G,
        )

        count_of_digit = len(str(funcs.gem_assist.get_balance()))

        button_x_text = (
                115 + col_text.get_width() - count_of_digit * 4
        )
        button_y_text = 48 - g_text.get_height() // 2

        self.screen.blit(
            g_text,
            (button_x_text, button_y_text),
        )
        # <===== Твой баланс =====>

        # <===== Ульта удаление =====>
        if draw_ulta_red:
            ulta_delete = pygame.draw.rect(
                self.screen,
                style.S_TABLE_SCORE,
                (90, 75, 50, 50),
                0,
                5,
            )
            pygame.draw.rect(
                self.screen,
                style.S_TABLE_SCORE_BORDER,
                (90, 75, 50, 50),
                5,
                5,
            )

            image = pygame.transform.scale(
                funcs.load_image("ulta_delete_click.png", (255, 255, 255)),
                (40, 40),
            )

            self.screen.blit(
                image,
                (ulta_delete.x + 5, ulta_delete.y + 5),
            )
        else:
            ulta_delete = pygame.draw.rect(
                self.screen,
                style.S_TABLE_SCORE,
                (90, 75, 50, 50),
                0,
                5,
            )
            pygame.draw.rect(
                self.screen,
                style.S_TABLE_SCORE_BORDER,
                (90, 75, 50, 50),
                5,
                5,
            )

            image = pygame.transform.scale(
                funcs.load_image("ulta_delete.png", (255, 255, 255)),
                (40, 40),
            )

            self.screen.blit(
                image,
                (ulta_delete.x + 5, ulta_delete.y + 5),
            )
        # <===== Ульта удаление =====>

        # <===== Твои очки =====>
        pygame.draw.rect(
            self.screen,
            style.S_TABLE_SCORE,
            (250, 10, 100, 50),
            0,
            5,
        )
        pygame.draw.rect(
            self.screen,
            style.S_TABLE_SCORE_BORDER,
            (250, 10, 100, 50),
            5,
            5,
        )
        font = pygame.font.SysFont(
            "spendthrift",
            20,
        )
        text = font.render(
            "Счет",
            True,
            style.S_TABLE_SCORE_TEXT,
        )

        button_x_text = 300 - text.get_width() // 2
        button_y_text = 25 - text.get_height() // 2

        self.screen.blit(
            text,
            (button_x_text, button_y_text),
        )

        font = pygame.font.SysFont(
            "spendthrift",
            30,
        )
        text = font.render(
            str(self.points),
            True,
            style.S_TABLE_SCORE_TEXT_VALUE,
        )

        button_x_text = 300 - text.get_width() // 2
        button_y_text = 40 - text.get_height() // 2

        self.screen.blit(
            text,
            (button_x_text, button_y_text),
        )
        # <===== Твои очки =====>

        # <===== Лучшие очки =====>
        pygame.draw.rect(
            self.screen,
            style.S_TABLE_SCORE,
            (360, 10, 100, 50),
            0,
            5,
        )
        pygame.draw.rect(
            self.screen,
            style.S_TABLE_SCORE_BORDER,
            (360, 10, 100, 50),
            5,
            5,
        )
        font = pygame.font.SysFont(
            "spendthrift",
            20,
        )
        text = font.render(
            "Лучший",
            True,
            style.S_TABLE_SCORE_TEXT,
        )

        button_x_text = 410 - text.get_width() // 2
        button_y_text = 25 - text.get_height() // 2

        self.screen.blit(text, (button_x_text, button_y_text))

        font = pygame.font.SysFont(
            "spendthrift",
            30,
        )
        text = font.render(
            str(self.best_score) if self.best_score else "",
            True,
            style.S_TABLE_SCORE_TEXT_VALUE,
        )

        button_x_text = 410 - text.get_width() // 2
        button_y_text = 40 - text.get_height() // 2

        self.screen.blit(
            text,
            (button_x_text, button_y_text),
        )
        # <===== Лучшие очки =====>

        # Прямоугольник для клеточек
        pygame.draw.rect(
            self.screen,
            style.RECT,
            (50, 150, 400, 400),
            0,
            15,
        )

        if draw_back_button:
            # <==== Назад ====>
            button_x = width // 2
            button_y = height - height // 12

            pygame.draw.rect(
                self.screen,
                style.S_BUTTON,
                (button_x - 100, button_y - 25, 200, 50),
                0,
                15,
            )

            font = pygame.font.SysFont(
                "spendthrift",
                40,
            )
            text = font.render(
                "Назад",
                True,
                style.S_BUTTON_TEXT,
            )

            button_x_text = width // 2 - text.get_width() // 2
            button_y_text = height - height // 12 - text.get_height() // 2

            self.screen.blit(
                text,
                (button_x_text, button_y_text),
            )
            # <==== Назад ====>

    def render_cell(self, i, j):
        cell_value = self.board[i][j]
        flag = cell_value != 0
        color = funcs.get_color_cell(cell_value)

        rect = pygame.Rect(
            50 + self.margin * (j + 1) + j * self.cell_size,
            150 + self.margin * (i + 1) + i * self.cell_size,
            self.cell_size,
            self.cell_size,
        )

        self.draw_cell_rect(rect, color)

        if flag:
            self.render_cell_text(cell_value, i, j)

    def draw_cell_rect(self, rect, color):
        """Рисует ячейку"""
        border_color = pygame.Color(color)

        pygame.draw.rect(
            self.screen,
            border_color,
            rect,
            0,
            5,
        )

    def render_cell_text(self, cell_value, i, j):
        """Отображение текста ячейки"""

        color, font_size = funcs.get_color_fontsize_text(cell_value, self.level)
        font = pygame.font.Font(
            None,
            font_size,
        )
        text_rendered = font.render(
            str(cell_value),
            True,
            color,
        )

        text_width, text_height = font.size(str(cell_value))

        text_x = (
                50
                + self.margin * (j + 1)
                + j * self.cell_size
                + (self.cell_size - text_width) // 2
        )
        text_y = (
                150
                + self.margin * (i + 1)
                + i * self.cell_size
                + (self.cell_size - text_height) // 2
        )

        self.screen.blit(
            text_rendered,
            (text_x, text_y),
        )

    def delete_cell(self, cell):
        if cell is not None:
            i, j = cell
            i, j = int(i), int(j)
            self.board[i][j] = 0

    def check_empty_cells(self):
        return not all(all(line) for line in self.board)

    def find_empty_cells(self):
        empty_cells = [
            (i, j)
            for i in range(self.value)
            for j in range(self.value)
            if self.board[i][j] == 0
        ]
        return empty_cells

    def spawn_number(self):
        chances = list(self.chances.items())[:2]
        lst_with_chances = [
            int(number) for number, chance in chances for _ in range(chance)
        ]
        number = random.choice(lst_with_chances)
        empty_cells = self.find_empty_cells()
        rd_empty_cell = random.choice(empty_cells)
        row, col = rd_empty_cell
        self.board[row][col] = number

    def spawn_gem(self):
        empty_cells = self.find_empty_cells()
        if empty_cells:
            rd_empty_cell = random.choice(empty_cells)
            row, col = rd_empty_cell
            self.board[row][col] = "G"

    def fill_random_cells(self):
        if sum(list(self.chances.values())[:2]) != 100:
            raise ValueError("Error: Chances do not add up to 100")
        self.spawn_number()

        is_spawn_g = random.randint(1, 100) in range(
            1, self.chances.get("G") + 1,
        )
        if is_spawn_g:
            self.spawn_gem()

    def move_left(self):
        board = []
        for line in self.board:
            inds_g = [i for i, v in enumerate(line) if v == "G"]
            for ind_g in inds_g:
                if ind_g != len(line) - 1:
                    if [i for i in line[ind_g + 1:] if i and i != "G"]:
                        line[ind_g] = 0
                        funcs.gem_assist.update_balance(1)
            new_line = [i for i in line if i] + [0] * line.count(0)
            board.append(new_line)
        self.board = board

        for i in range(self.value):
            for j in range(self.value - 1):
                if (
                        self.board[i][j] == self.board[i][j + 1]
                        and self.board[i][j + 1] != 0
                ):
                    if self.board[i][j] != "G":
                        result_of_cell = self.board[i][j] * 2
                        self.board[i][j] = result_of_cell
                        self.board[i].pop(j + 1)
                        self.board[i].append(0)
                        self.points += result_of_cell
                    else:
                        result_of_cell = "G"
                        self.board[i][j] = result_of_cell

    def move_right(self):
        board = []
        for line in self.board:
            inds_g = [i for i, v in enumerate(line) if v == "G"]
            for ind_g in inds_g:
                if True:
                    if [i for i in line[:ind_g] if i and i != "G"]:
                        line[ind_g] = 0
                        funcs.gem_assist.update_balance(1)
            new_line = [0] * line.count(0) + [i for i in line if i]
            board.append(new_line)
        self.board = board

        for i in range(self.value):
            for j in range(self.value - 1, 0, -1):
                if self.board[i][j] == self.board[i][j - 1] and self.board[i][j] != 0:
                    if self.board[i][j] != "G":
                        result_of_cell = self.board[i][j] * 2
                        self.board[i][j] = result_of_cell
                        self.board[i].pop(j - 1)
                        self.board[i].insert(0, 0)
                        self.points += result_of_cell
                    else:
                        result_of_cell = "G"
                        self.board[i][j] = result_of_cell

    def move_up(self):
        self.board = [list(line) for line in zip(*self.board)]
        board = []
        for line in self.board:
            inds_g = [i for i, v in enumerate(line) if v == "G"]
            for ind_g in inds_g:
                if ind_g != len(line) - 1:
                    if [i for i in line[ind_g + 1:] if i and i != "G"]:
                        line[ind_g] = 0
                        funcs.gem_assist.update_balance(1)
            new_line = [i for i in line if i] + [0] * line.count(0)
            board.append(new_line)
        self.board = board
        for i in range(self.value):
            for j in range(self.value - 1):
                if (
                        self.board[i][j] == self.board[i][j + 1]
                        and self.board[i][j + 1] != 0
                ):
                    if self.board[i][j] != "G":
                        result_of_cell = self.board[i][j] * 2
                        self.board[i][j] = result_of_cell
                        self.board[i].pop(j + 1)
                        self.board[i].append(0)
                        self.points += result_of_cell
                    else:
                        result_of_cell = "G"
                        self.board[i][j] = result_of_cell
        self.board = [list(line) for line in zip(*self.board)]

    def move_down(self):
        self.board = [list(line) for line in zip(*self.board)]
        board = []
        for line in self.board:
            inds_g = [i for i, v in enumerate(line) if v == "G"]
            for ind_g in inds_g:
                if True:
                    if [i for i in line[:ind_g] if i and i != "G"]:
                        line[ind_g] = 0
                        funcs.gem_assist.update_balance(1)
            new_line = [0] * line.count(0) + [i for i in line if i]
            board.append(new_line)
        self.board = board
        for i in range(self.value):
            for j in range(self.value - 1, 0, -1):
                if self.board[i][j] == self.board[i][j - 1] and self.board[i][j] != 0:
                    if self.board[i][j] != "G":
                        result_of_cell = self.board[i][j] * 2
                        self.board[i][j] = result_of_cell
                        self.board[i].pop(j - 1)
                        self.board[i].insert(0, 0)
                        self.points += result_of_cell
                    else:
                        result_of_cell = "G"
                        self.board[i][j] = result_of_cell
        self.board = [list(line) for line in zip(*self.board)]

    def move(self, key):
        is_empty_cells = self.check_empty_cells()
        if is_empty_cells:
            match key:
                case pygame.K_LEFT:
                    self.move_left()
                case pygame.K_RIGHT:
                    self.move_right()
                case pygame.K_UP:
                    self.move_up()
                case pygame.K_DOWN:
                    self.move_down()
            self.fill_random_cells()

    def get_cell(self, pos_x, pos_y):
        """Определение ячейки по координатам клика"""
        if (
                pos_x < 50
                or pos_x > 50 + self.cell_size * self.value + self.margin * (self.value + 1)
                or pos_y < 150
                or pos_y > 150 + self.cell_size * self.value + self.margin * (self.value + 1)
        ):
            return None
        return (
            (pos_y - 150) // (self.cell_size + self.margin),
            (pos_x - 50) // (self.cell_size + self.margin),
        )

    def get_click(self, pos_x, pos_y):
        """Определение клика"""
        cell = self.get_cell(int(pos_x), int(pos_y))
        return cell

    def update_settings_and_refresh(self, level):
        settings = funcs.generate_settings(level)

        self.level = level
        self.value = settings.get("value")
        self.cell_size = settings.get("cell_size")
        self.margin = settings.get("margin")
        self.board = [[0 for _ in range(self.value)] for _ in range(self.value)]
        self.ulta_delete_active = False

        # Шансы на выпадение чисел
        self.chances = {
            "2": settings.get("chance_for_spawn_2"),
            "4": settings.get("chance_for_spawn_4"),
            "G": settings.get("chance_for_spawn_G"),
        }

        self.points = 0
        self.steps = 0
        self.start_balance = funcs.gem_assist.get_balance()
        self.best_score = tables.Game.get_best_score(self.session)

    @staticmethod
    def is_lose(board):
        return all([el != 0 for line in board for el in line])

    @staticmethod
    def is_win(board):
        return any([el == 2048 for line in board for el in line])

    def game_page(self):

        width, height = self.screen_size

        self.screen.fill(style.BACKGROUND_COLOR)
        self.render_decoration(self.screen, True)

        ulta_red = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key in (
                            pygame.K_LEFT,
                            pygame.K_RIGHT,
                            pygame.K_UP,
                            pygame.K_DOWN,
                    ):
                        random.choice(self.move_sounds).play()
                        self.steps += 1
                        self.move(event.key)
                        if self.is_lose(self.board):
                            self.render_cells()
                            self.lose_page()
                        elif self.is_win(self.board):
                            self.render_cells()
                            self.win_page()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if 250 - 100 < x_pos < 250 + 100 and 596 - 25 < y_pos < 596 + 25:
                        self.click_sound.play()
                        self.choice_page()
                    if 90 < x_pos < 140 and 75 < y_pos < 125:
                        self.ulta_delete_active = True
                    elif self.ulta_delete_active:
                        cell = self.get_click(x_pos, y_pos)

                        if cell:
                            cell = list(map(int, cell))
                            if self.check_valid_cell(cell):
                                need_money = 10
                                if self.check_money_for_ulta(need_money):
                                    funcs.gem_assist.sell_balance(10)
                                    self.ulta_delete_active = False
                                    self.delete_cell(cell)
                        else:
                            self.ulta_delete_active = False

                if event.type == pygame.MOUSEMOTION:
                    x_pos, y_pos = event.pos

                    button_x = width // 2
                    button_y = height - height // 12
                    font = pygame.font.SysFont(
                        "spendthrift",
                        40,
                    )
                    text = font.render(
                        "Назад",
                        True,
                        style.S_BUTTON_TEXT,
                    )

                    button_x_text = width // 2 - text.get_width() // 2
                    button_y_text = height - height // 12 - text.get_height() // 2
                    if 150 < x_pos < 350 and 571 < y_pos < 621:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            (button_x - 100, button_y - 25, 200, 50),
                            0,
                            15,
                        )
                        self.screen.blit(
                            text,
                            (button_x_text, button_y_text),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            (button_x - 100, button_y - 25, 200, 50),
                            0,
                            15,
                        )
                        self.screen.blit(
                            text,
                            (button_x_text, button_y_text),
                        )
                    if 90 < x_pos < 140 and 75 < y_pos < 125:
                        ulta_red = True

                        pygame.draw.rect(
                            self.screen,
                            style.S_TABLE_SCORE,
                            (90, 125, 50, 20),
                            0,
                            5,
                        )
                        font = pygame.font.SysFont(
                            "spendthrift",
                            25,
                        )
                        text = font.render(
                            "10",
                            True,
                            style.S_TABLE_SCORE_TEXT,
                        )

                        button_x_text = 115 - text.get_width() // 2
                        button_y_text = 135 - text.get_height() // 2

                        self.screen.blit(
                            text,
                            (button_x_text, button_y_text),
                        )
                    else:
                        ulta_red = False

                        pygame.draw.rect(
                            self.screen,
                            style.BACKGROUND_COLOR,
                            (90, 125, 50, 20),
                            0,
                            5,
                        )

            self.render_decoration(draw_ulta_red=ulta_red)
            self.render_cells()
            pygame.display.flip()

    def lose_page(self):
        pygame.display.flip()
        width, height = self.screen_size
        screen_filename = datetime.datetime.now().strftime(
            "screen_save_%d_%m_%Y_%H_%M_%S.png",
        )
        screen_path = self.base_dir / "data" / "saves"
        screen_full_path = screen_path / screen_filename
        pygame.image.save(self.screen, screen_full_path)

        board_filename = datetime.datetime.now().strftime(
            "board_save_%d_%m_%Y_%H_%M_%S.png",
        )
        board_path = self.base_dir / "data" / "saves"
        board_full_path = board_path / board_filename

        funcs.crop_image(
            screen_full_path,
            (50, 150),
            (450, 550),
            board_full_path,
        )

        screen_full_path.unlink()

        self.screen.fill(style.BACKGROUND_COLOR)

        image = funcs.load_save(board_full_path)

        resized_image = pygame.transform.scale(image, (200, 200))

        self.screen.blit(resized_image, (150, 120))

        new_game = tables.Game(
            points=self.points,
            is_win=False,
            map=str(board_full_path),
            size=self.value,
            steps=self.steps,
        )
        self.session.add(new_game)
        self.session.commit()

        font = pygame.font.SysFont(
            "spendthrift",
            50,
        )
        text_label = font.render(
            "ВЫ ПРОИГРАЛИ!",
            True,
            style.S_TEXT,
        )

        button_x_text_label = width // 2 - text_label.get_width() // 2
        button_y_text_label = 70 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )

        # <НАЗАД>
        button_back_x = width // 2
        button_back_y = 600

        button_back_rect = pygame.Rect(
            button_back_x - 100,
            button_back_y - 25,
            200,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            button_back_rect,
            0,
            15,
        )

        font = pygame.font.SysFont(
            "spendthrift",
            40,
        )
        text_back = font.render(
            "Назад",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text = width // 2 - text_back.get_width() // 2
        button_y_text = 600 - text_back.get_height() // 2

        self.screen.blit(
            text_back,
            (button_x_text, button_y_text), )
        # Назад

        # Счет
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        text_label = font.render(
            "Счет:",
            True,
            style.S_TITLE,
        )

        button_x_text_label = 100
        button_y_text_label = 350 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )
        # Счет

        # Ходов
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        text_label = font.render(
            "Ходов:",
            True,
            style.S_TITLE,
        )

        button_x_text_label = 100
        button_y_text_label = 400 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )
        # Ходов

        # Заработано
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        text_label = font.render(
            "Заработано:",
            True,
            style.S_TITLE,
        )

        button_x_text_label = 100
        button_y_text_label = 450 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )
        # Заработано

        # Счет value
        font = pygame.font.SysFont("spendthrift", 35)
        text_label = font.render(
            str(self.points),
            True,
            style.S_TEXT,
        )

        button_x_text_label = 300
        button_y_text_label = 350 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )
        # Счет value

        # Ходов value
        font = pygame.font.SysFont("spendthrift", 35)
        text_label = font.render(
            str(self.steps),
            True,
            style.S_TEXT,
        )

        button_x_text_label = 300
        button_y_text_label = 400 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )
        # Ходов value

        # Заработано value
        font = pygame.font.SysFont("spendthrift", 35)
        g_fonted = funcs.gem_assist.get_balance() - self.start_balance
        text_label = font.render(
            str(g_fonted),
            True,
            style.S_TEXT,
        )

        button_x_text_label = 300
        button_y_text_label = 450 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )

        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        g_text = font.render(
            "G",
            True,
            style.S_TABLE_SCORE_TEXT_VALUE_G,
        )

        button_x_g_text = 300 + text_label.get_width() + 5
        button_y_g_text = button_y_text_label

        self.screen.blit(
            g_text,
            (button_x_g_text, button_y_g_text),
        )
        # Заработано value

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if button_back_rect.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.choice_page()
                elif event.type == pygame.MOUSEMOTION:
                    x_pos, y_pos = event.pos
                    if button_back_rect.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            button_back_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_back,
                            (button_x_text, button_y_text),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            button_back_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_back,
                            (button_x_text, button_y_text),
                        )

            pygame.display.flip()

    def win_page(self):
        pygame.display.flip()
        width, height = self.screen_size
        screen_filename = datetime.datetime.now().strftime(
            "screen_save_%d_%m_%Y_%H_%M_%S.png"
        )
        screen_path = self.base_dir / "data" / "saves"
        screen_full_path = screen_path / screen_filename
        pygame.image.save(self.screen, screen_full_path)

        board_filename = datetime.datetime.now().strftime(
            "board_save_%d_%m_%Y_%H_%M_%S.png",
        )
        board_path = self.base_dir / "data" / "saves"
        board_full_path = board_path / board_filename

        funcs.crop_image(
            screen_full_path,
            (50, 150),
            (450, 550),
            board_full_path,
        )

        screen_full_path.unlink()

        self.screen.fill(style.BACKGROUND_COLOR)

        image = funcs.load_save(board_full_path)

        resized_image = pygame.transform.scale(
            image,
            (200, 200),
        )

        self.screen.blit(
            resized_image,
            (150, 120),
        )

        new_game = tables.Game(
            points=self.points,
            is_win=True,
            map=str(board_full_path),
            size=self.value,
            steps=self.steps,
        )
        self.session.add(new_game)
        self.session.commit()

        font = pygame.font.SysFont(
            "spendthrift",
            50,
        )
        text_label = font.render(
            "ВЫ ВЫЙГРАЛИ!",
            True,
            style.S_TEXT,
        )

        button_x_text_label = width // 2 - text_label.get_width() // 2
        button_y_text_label = 70 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )

        # <НАЗАД>
        button_back_x = width // 2
        button_back_y = 600

        button_back_rect = pygame.Rect(
            button_back_x - 100,
            button_back_y - 25,
            200,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            button_back_rect,
            0,
            15,
        )

        font = pygame.font.SysFont(
            "spendthrift",
            40,
        )
        text_back = font.render(
            "Назад",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text = width // 2 - text_back.get_width() // 2
        button_y_text = 600 - text_back.get_height() // 2

        self.screen.blit(
            text_back,
            (button_x_text, button_y_text),
        )
        # Назад

        # Счет
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        text_label = font.render(
            "Счет:",
            True,
            style.S_TITLE,
        )

        button_x_text_label = 100
        button_y_text_label = 350 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )
        # Счет

        # Ходов
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        text_label = font.render(
            "Ходов:",
            True,
            style.S_TITLE,
        )

        button_x_text_label = 100
        button_y_text_label = 400 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),

        )
        # Ходов

        # Заработано
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        text_label = font.render(
            "Заработано:",
            True,
            style.S_TITLE,
        )

        button_x_text_label = 100
        button_y_text_label = 450 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )
        # Заработано

        # Счет value
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        text_label = font.render(
            str(self.points),
            True,
            style.S_TEXT,
        )

        button_x_text_label = 300
        button_y_text_label = 350 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )
        # Счет value

        # Ходов value
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        text_label = font.render(
            str(self.steps),
            True,
            style.S_TEXT,
        )

        button_x_text_label = 300
        button_y_text_label = 400 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )
        # Ходов value

        # Заработано value
        font = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        g_fonted = funcs.gem_assist.get_balance() - self.start_balance
        text_label = font.render(
            str(g_fonted),
            True,
            style.S_TEXT,
        )

        button_x_text_label = 300
        button_y_text_label = 450 - text_label.get_height() // 2

        self.screen.blit(
            text_label,
            (button_x_text_label, button_y_text_label),
        )

        font = pygame.font.SysFont("spendthrift", 35)
        g_text = font.render(
            "G",
            True,
            style.S_TABLE_SCORE_TEXT_VALUE_G,
        )

        button_x_g_text = 300 + text_label.get_width() + 5
        button_y_g_text = button_y_text_label

        self.screen.blit(
            g_text,
            (button_x_g_text, button_y_g_text),
        )
        # Заработано value

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if button_back_rect.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.choice_page()
                elif event.type == pygame.MOUSEMOTION:
                    x_pos, y_pos = event.pos
                    if button_back_rect.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            button_back_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_back,
                            (button_x_text, button_y_text),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            button_back_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_back,
                            (button_x_text, button_y_text),
                        )

            pygame.display.flip()

    def start_page(self):
        width, height = self.screen_size

        self.screen.fill(style.BACKGROUND_COLOR)

        # <==== Играть ====>
        button_x_1 = width // 2
        button_y_1 = height // 2

        play_button_rect = pygame.Rect(
            button_x_1 - 100,
            button_y_1 - 25,
            200,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            play_button_rect,
            0,
            15,
        )

        font = pygame.font.SysFont(
            "spendthrift",
            40,
        )
        text_play = font.render(
            "Играть",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text_1 = width // 2 - text_play.get_width() // 2
        button_y_text_1 = height // 2 - text_play.get_height() // 2

        self.screen.blit(
            text_play,
            (button_x_text_1, button_y_text_1),
        )
        # <==== Играть ====>

        # <==== Рекорды ====>
        button_x_2 = width // 2
        button_y_2 = height // 2 + 80

        records_button_rect = pygame.Rect(
            button_x_2 - 100,
            button_y_2 - 25,
            200,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            records_button_rect,
            0,
            15,
        )

        font = pygame.font.SysFont(
            "spendthrift",
            40,
        )
        text_records = font.render(
            "Рекорды",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text_2 = width // 2 - text_records.get_width() // 2
        button_y_text_2 = height // 2 + 80 - text_records.get_height() // 2

        self.screen.blit(
            text_records,
            (button_x_text_2, button_y_text_2),
        )
        # <==== Рекорды ====>

        # <==== Правила ====>
        button_x_3 = width // 2
        button_y_3 = height // 2 + 160

        rules_button_rect = pygame.Rect(
            button_x_3 - 100,
            button_y_3 - 25,
            200,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            rules_button_rect,
            0,
            15,
        )

        font = pygame.font.SysFont(
            "spendthrift",
            40,
        )
        text_rules = font.render(
            "Правила",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text_3 = width // 2 - text_rules.get_width() // 2
        button_y_text_3 = height // 2 + 160 - text_rules.get_height() // 2

        self.screen.blit(
            text_rules,
            (button_x_text_3, button_y_text_3),
        )
        # <==== Правила ====>

        while True:
            color_index = datetime.datetime.now().second % 7
            color = [
                (255, 0, 0),
                (255, 165, 0),
                (255, 255, 0),
                (0, 255, 0),
                (0, 0, 255),
                (75, 0, 130),
                (148, 0, 211),
            ][color_index]

            # Пересоздание текста с новым цветом
            font_title = pygame.font.SysFont(
                "spendthrift",
                150,
            )
            text_title = font_title.render(
                "2048",
                True,
                color,
            )
            text_x = width // 2 - text_title.get_width() // 2
            text_y = height // 3 - text_title.get_height() // 2

            self.screen.blit(
                text_title,
                (text_x, text_y),
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if play_button_rect.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.choice_page()
                    elif records_button_rect.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.records_page()
                    elif rules_button_rect.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.rules_page()
                if event.type == pygame.MOUSEMOTION:
                    x_pos, y_pos = event.pos
                    if play_button_rect.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            play_button_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_play,
                            (button_x_text_1, button_y_text_1),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            play_button_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_play,
                            (button_x_text_1, button_y_text_1),
                        )
                    if records_button_rect.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            records_button_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_records,
                            (button_x_text_2, button_y_text_2),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            records_button_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_records,
                            (button_x_text_2, button_y_text_2),
                        )
                    if rules_button_rect.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            rules_button_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_rules,
                            (button_x_text_3, button_y_text_3),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            rules_button_rect,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_rules,
                            (button_x_text_3, button_y_text_3),
                        )

            pygame.display.flip()

    def choice_page(self):
        width, height = self.screen_size

        self.screen.fill(style.BACKGROUND_COLOR)

        # <==== Надпись ====>
        font_title = pygame.font.SysFont(
            "spendthrift",
            60,
        )
        text_title = font_title.render(
            "Выбери размер поля",
            True,
            style.S_MAIN_TITLE,
        )

        text_x = width // 2 - text_title.get_width() // 2
        text_y = height // 8 - text_title.get_height() // 2

        self.screen.blit(
            text_title,
            (text_x, text_y),
        )
        # <==== Надпись ====>

        font = pygame.font.SysFont(
            "spendthrift",
            40,
        )

        # <==== 4 x 4 ====>
        button_x_1 = width // 2
        button_y_1 = height // 3

        button_4_x_4 = pygame.Rect(
            button_x_1 - 125,
            button_y_1 - 25,
            250,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            button_4_x_4,
            0,
            15,
        )

        text_4_x_4 = font.render(
            "4 x 4",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text_1 = width // 2 - text_4_x_4.get_width() // 2
        button_y_text_1 = height // 3 - text_4_x_4.get_height() // 2

        self.screen.blit(
            text_4_x_4,
            (button_x_text_1, button_y_text_1),
        )
        # <==== 4 x 4 ====>

        # <==== 6 x 6 ====>
        button_x_2 = width // 2
        button_y_2 = height // 3 + 100

        button_6_x_6 = pygame.Rect(
            button_x_2 - 125,
            button_y_2 - 25,
            250,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            button_6_x_6,
            0,
            15,
        )

        text_6_x_6 = font.render(
            "6 x 6",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text_2 = width // 2 - text_6_x_6.get_width() // 2
        button_y_text_2 = height // 3 + 100 - text_6_x_6.get_height() // 2

        self.screen.blit(
            text_6_x_6,
            (button_x_text_2, button_y_text_2),
        )
        # <==== 6 x 6 ====>

        # <==== Правила ====>
        button_x_3 = width // 2
        button_y_3 = height // 3 + 200

        button_8_x_8 = pygame.Rect(
            button_x_3 - 125,
            button_y_3 - 25,
            250,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            button_8_x_8,
            0,
            15,
        )

        text_8_x_8 = font.render(
            "8 x 8",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text_3 = width // 2 - text_8_x_8.get_width() // 2
        button_y_text_3 = height // 3 + 200 - text_8_x_8.get_height() // 2

        self.screen.blit(
            text_8_x_8,
            (button_x_text_3, button_y_text_3),
        )
        # <==== 8 x 8 ====>

        # <==== Назад ====>
        button_back_x = width // 2
        button_back_y = height - height // 8

        button_back = pygame.Rect(
            button_back_x - 100,
            button_back_y - 25,
            200,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            button_back,
            0,
            15,
        )

        text_back = font.render(
            "Назад",
            True,
            style.S_BUTTON_TEXT,
        )

        button_back_x_text = width // 2 - text_back.get_width() // 2
        button_back_y_text = height - height // 8 - text_back.get_height() // 2

        self.screen.blit(
            text_back,
            (button_back_x_text, button_back_y_text),
        )
        # <==== Назад ====>

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if button_4_x_4.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.update_settings_and_refresh(1)
                        self.game_page()
                    if button_6_x_6.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.update_settings_and_refresh(2)
                        self.game_page()
                    if button_8_x_8.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.update_settings_and_refresh(3)
                        self.game_page()
                    if button_back.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.start_page()
                if event.type == pygame.MOUSEMOTION:
                    x_pos, y_pos = event.pos
                    if button_4_x_4.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            button_4_x_4,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_4_x_4,
                            (button_x_text_1, button_y_text_1),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            button_4_x_4,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_4_x_4,
                            (button_x_text_1, button_y_text_1),
                        )

                    if button_6_x_6.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            button_6_x_6,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_6_x_6,
                            (button_x_text_2, button_y_text_2),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            button_6_x_6,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_6_x_6,
                            (button_x_text_2, button_y_text_2),
                        )

                    if button_8_x_8.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            button_8_x_8,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_8_x_8,
                            (button_x_text_3, button_y_text_3),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            button_8_x_8,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_8_x_8,
                            (button_x_text_3, button_y_text_3),
                        )
                    if button_back.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            button_back,
                            0,
                            15,
                        )

                        self.screen.blit(
                            text_back,
                            (button_back_x_text, button_back_y_text),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            button_back,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_back,
                            (button_back_x_text, button_back_y_text),
                        )

            pygame.display.flip()

    def records_page(self):
        width, height = self.screen_size

        self.screen.fill(style.BACKGROUND_COLOR)

        # <==== Надпись ====>
        font_title = pygame.font.SysFont(
            "spendthrift",
            60, )
        text_title = font_title.render(
            "Рекорды",
            True,
            style.S_MAIN_TITLE,
        )

        text_x = width // 2 - text_title.get_width() // 2
        text_y = height // 8 - text_title.get_height() // 2

        self.screen.blit(
            text_title,
            (text_x, text_y),
        )
        # <==== Надпись ====>

        font = pygame.font.SysFont(
            "spendthrift",
            40,
        )

        # <==== Назад ====>
        button_back_x = width // 2
        button_back_y = height - height // 8

        button_back = pygame.Rect(
            button_back_x - 100,
            button_back_y - 25,
            200,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            button_back,
            0,
            15,
        )

        text_back = font.render(
            "Назад",
            True,
            style.S_BUTTON_TEXT
        )

        btn_back_x_text = width // 2 - text_back.get_width() // 2
        btn_back_y_text = height - height // 8 - text_back.get_height() // 2

        self.screen.blit(
            text_back,
            (btn_back_x_text, btn_back_y_text)
        )
        # <==== Назад ====>

        top_games = tables.Game.get_top_3_games(self.session)

        if top_games:
            for index, game in enumerate(top_games, 1):
                image = funcs.load_save(game.map)

                resized_image = pygame.transform.scale(
                    image,
                    (100, 100),
                )

                self.screen.blit(
                    resized_image,
                    (60, 130 * index)
                )

                font = pygame.font.SysFont(
                    "spendthrift",
                    25,
                )

                # Счет
                text_label = font.render(
                    "Счет:",
                    True,
                    style.S_TITLE,
                )

                btn_x_text_label = 200
                btn_y_text_label = 15 + 130 * index - text_label.get_height() // 2

                self.screen.blit(
                    text_label,
                    (btn_x_text_label, btn_y_text_label),
                )

                text_label = font.render(
                    str(game.points),
                    True,
                    style.S_TEXT,
                )

                btn_x_text_label = 300

                self.screen.blit(
                    text_label,
                    (btn_x_text_label, btn_y_text_label),
                )
                # Счет

                # Ходов
                text_label = font.render(
                    "Ходов:",
                    True,
                    style.S_TITLE,
                )

                button_x_text_label = 200
                button_y_text_label = 40 + 130 * index - text_label.get_height() // 2

                self.screen.blit(
                    text_label,
                    (button_x_text_label, button_y_text_label),
                )

                text_label = font.render(
                    str(game.steps),
                    True,
                    style.S_TEXT,
                )

                button_x_text_label = 300
                button_y_text_label = button_y_text_label

                self.screen.blit(
                    text_label,
                    (button_x_text_label, button_y_text_label),
                )
                # Ходов

                # Результат
                text_label = font.render(
                    "Результат:",
                    True,
                    style.S_TITLE,
                )

                button_x_text_label = 200
                button_y_text_label = 65 + 130 * index - text_label.get_height() // 2

                self.screen.blit(
                    text_label,
                    (button_x_text_label, button_y_text_label),
                )

                text_label = font.render(
                    "Победа" if game.is_win else "Поражение",
                    True,
                    style.S_TEXT,
                )

                button_x_text_label = 300
                button_y_text_label = button_y_text_label

                self.screen.blit(
                    text_label,
                    (button_x_text_label, button_y_text_label),
                )
                # Результат

                # Когда
                text_label = font.render(
                    "Когда:",
                    True,
                    style.S_TITLE,
                )

                button_x_text_label = 200
                button_y_text_label = 90 + 130 * index - text_label.get_height() // 2

                self.screen.blit(
                    text_label,
                    (button_x_text_label, button_y_text_label),
                )

                text_label = font.render(
                    game.datetime.strftime("%d.%m.%Y %H:%M"),
                    True,
                    style.S_TEXT,
                )

                button_x_text_label = 300
                button_y_text_label = button_y_text_label

                self.screen.blit(
                    text_label,
                    (button_x_text_label, button_y_text_label),
                )
                # Когда
        else:
            # <==== Надпись ====>
            font_title = pygame.font.SysFont(
                "spendthrift",
                50,
            )
            text_title = font_title.render(
                "Увы, пока не было игр",
                True,
                style.S_TITLE,
            )

            text_x = width // 2 - text_title.get_width() // 2
            text_y = 300

            self.screen.blit(
                text_title,
                (text_x, text_y),
            )
            # <==== Надпись ====>

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if button_back.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.start_page()
                if event.type == pygame.MOUSEMOTION:
                    x_pos, y_pos = event.pos
                    if button_back.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            button_back,
                            0,
                            15,
                        )

                        self.screen.blit(
                            text_back, (btn_back_x_text, btn_back_y_text),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            button_back,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text_back,
                            (btn_back_x_text, btn_back_y_text),
                        )

            pygame.display.flip()

    def rules_page(self):
        width, height = self.screen_size

        self.screen.fill(style.BACKGROUND_COLOR)

        # <==== Надпись ====>
        font = pygame.font.SysFont(
            "spendthrift",
            60,
        )
        text = font.render(
            "Правила",
            True,
            style.S_MAIN_TITLE,
        )

        text_x = width // 2 - text.get_width() // 2
        text_y = height // 8 - text.get_height() // 2

        self.screen.blit(text, (text_x, text_y))
        # <==== Надпись ====>

        # <==== Правила игры ====>
        rule_font_title = pygame.font.SysFont(
            "spendthrift",
            35,
        )
        rule_font_text = pygame.font.SysFont(
            "spendthrift",
            15,
        )
        rule_text_1 = rule_font_title.render(
            "Цель игры:",
            True,
            style.S_TITLE,
        )
        rule_text_2 = rule_font_text.render(
            "Получить плитку со значением 2048.",
            True,
            style.S_TEXT,
        )
        rule_text_3 = rule_font_title.render(
            "Управление:",
            True,
            style.S_TITLE,
        )
        rule_text_4 = rule_font_text.render(
            "Используйте стрелки для перемещения всех плиток.",
            True,
            style.S_TEXT,
        )
        rule_text_5 = rule_font_text.render(
            "Плитки с одинаковыми значениями сливаются вместе.",
            True,
            style.S_TEXT,
        )
        rule_text_6 = rule_font_title.render(
            "Проигрыш:",
            True,
            style.S_TITLE,
        )
        rule_text_7 = rule_font_text.render(
            "Когда пустых клеток на поле не останется.",
            True,
            style.S_TEXT,
        )

        rule_text_y = height // 4

        self.screen.blit(
            rule_text_1,
            (width // 2 - rule_text_1.get_width() // 2, rule_text_y),
        )
        self.screen.blit(
            rule_text_2,
            (width // 2 - rule_text_2.get_width() // 2, rule_text_y + 40),
        )
        self.screen.blit(
            rule_text_3,
            (width // 2 - rule_text_3.get_width() // 2, rule_text_y + 100),
        )
        self.screen.blit(
            rule_text_4,
            (width // 2 - rule_text_4.get_width() // 2, rule_text_y + 140),
        )
        self.screen.blit(
            rule_text_5,
            (width // 2 - rule_text_5.get_width() // 2, rule_text_y + 180),
        )
        self.screen.blit(
            rule_text_6,
            (width // 2 - rule_text_6.get_width() // 2, rule_text_y + 240),
        )
        self.screen.blit(
            rule_text_7,
            (width // 2 - rule_text_7.get_width() // 2, rule_text_y + 280),
        )
        # <==== Правила игры ====>

        # <==== Назад ====>
        button_x_1 = width // 2
        button_y_1 = height - height // 8

        button_back = pygame.Rect(
            button_x_1 - 100,
            button_y_1 - 25,
            200,
            50,
        )

        pygame.draw.rect(
            self.screen,
            style.S_BUTTON,
            button_back,
            0,
            15,
        )

        font = pygame.font.SysFont(
            "spendthrift",
            40,
        )
        text = font.render(
            "Назад",
            True,
            style.S_BUTTON_TEXT,
        )

        button_x_text_1 = width // 2 - text.get_width() // 2
        button_y_text_1 = height - height // 8 - text.get_height() // 2

        self.screen.blit(
            text,
            (button_x_text_1, button_y_text_1),
        )
        # <==== Назад ====>

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_pos, y_pos = event.pos
                    if button_back.collidepoint(x_pos, y_pos):
                        self.click_sound.play()
                        self.start_page()
                if event.type == pygame.MOUSEMOTION:
                    x_pos, y_pos = event.pos
                    if button_back.collidepoint(x_pos, y_pos):
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON_HOVER,
                            button_back,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text,
                            (button_x_text_1, button_y_text_1),
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            style.S_BUTTON,
                            button_back,
                            0,
                            15,
                        )
                        self.screen.blit(
                            text,
                            (button_x_text_1, button_y_text_1),
                        )
            pygame.display.flip()

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

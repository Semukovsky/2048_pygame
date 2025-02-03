import pygame
from PIL import Image

import os
import sys
import json
import pathlib

import project.game.style as style
import project.db.config as config

base_dir = pathlib.Path(__file__).parent.parent.absolute()


def load_image(name, color=None):
    fullname = base_dir / "data" / "image" / name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color is not None:
        if color == -1:
            color = image.get_at((0, 0))
        image.set_colorkey(color)
    return image


def load_save(name):
    fullname = base_dir / "data" / "saves" / name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def get_color_cell(cell_value):
    settings = {
        0: style.CELL_COLOR_0,
        2: style.CELL_COLOR_2,
        4: style.CELL_COLOR_4,
        8: style.CELL_COLOR_8,
        16: style.CELL_COLOR_16,
        32: style.CELL_COLOR_32,
        64: style.CELL_COLOR_64,
        128: style.CELL_COLOR_128,
        256: style.CELL_COLOR_256,
        512: style.CELL_COLOR_512,
        1024: style.CELL_COLOR_1024,
        2048: style.CELL_COLOR_2048,
        "G": style.CELL_COLOR_G,
    }
    return settings.get(cell_value)


def get_color_fontsize_text(cell_value, level):
    match cell_value:
        case 2:
            return style.TEXT_COLOR_2, (
                80 if level == 1 else 60 if level == 2 else 40
            )
        case 4:
            return style.TEXT_COLOR_4, (
                80 if level == 1 else 60 if level == 2 else 40
            )
        case 8:
            return style.TEXT_COLOR_8, (
                80 if level == 1 else 60 if level == 2 else 60
            )
        case 16:
            return style.TEXT_COLOR_16, (
                75 if level == 1 else 60 if level == 2 else 40
            )
        case 32:
            return style.TEXT_COLOR_32, (
                75 if level == 1 else 60 if level == 2 else 40
            )
        case 64:
            return style.TEXT_COLOR_64, (
                75 if level == 1 else 60 if level == 2 else 40
            )
        case 128:
            return style.TEXT_COLOR_128, (
                65 if level == 1 else 45 if level == 2 else 35
            )
        case 256:
            return style.TEXT_COLOR_256, (
                65 if level == 1 else 45 if level == 2 else 35
            )
        case 512:
            return style.TEXT_COLOR_512, (
                65 if level == 1 else 45 if level == 2 else 35
            )
        case 1024:
            return style.TEXT_COLOR_1024, (
                55 if level == 1 else 35 if level == 2 else 25
            )
        case 2048:
            return style.TEXT_COLOR_2048, (
                55 if level == 1 else 35 if level == 2 else 25
            )
        case "G":
            return style.TEXT_COLOR_G, (
                80 if level == 1 else 60 if level == 2 else 60
            )


def generate_settings(level):
    """Функция, возвращающая настройки игры"""
    settings = {
        1: {
            "level": 1,
            "value": 4,
            "cell_size": 90,
            "margin": 8,
            "left": 50,
            "top": 150,

        },
        2: {
            "level": 2,
            "value": 6,
            "cell_size": 57.33,
            "margin": 8,
            "left": 50,
            "top": 150,
        },
        3: {
            "level": 3,
            "value": 8,
            "cell_size": 41,
            "margin": 8,
            "left": 50,
            "top": 150,
        },
    }
    return settings[level] | config.settings.SETTINGS_GAME


def load_setting():
    with open(base_dir / "values" / "profile_values.json", "r", encoding="utf-8") as f:
        user_setting = json.load(f)
        return user_setting

def dump_setting(setting):
    with open(base_dir / "values" / "profile_values.json", "w", encoding="utf-8") as f:
        json.dump(setting, f, indent=4)

def crop_image(image_path, pos_1, pos_2, output_path):
    image = Image.open(image_path)

    cropped_image = image.crop((*pos_1, *pos_2))

    cropped_image.save(output_path)


class GemAssist:
    def __init__(self):
        self.user_setting = load_setting()

    def sell_balance(self, value):
        self.user_setting["balance"] -= value
        dump_setting(self.user_setting)

    def update_balance(self, value):
        self.user_setting["balance"] += value
        dump_setting(self.user_setting)

    def get_balance(self):
        return self.user_setting["balance"]

gem_assist = GemAssist()
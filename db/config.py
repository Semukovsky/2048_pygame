import pydantic_settings

import json


class Settings(pydantic_settings.BaseSettings):

    chance_for_spawn_2: int
    chance_for_spawn_4: int
    chance_for_spawn_G: int

    @property
    def DATABASE_URL(self):
        return f"sqlite:///database.db"

    @property
    def SETTINGS_GAME(self):
        return {
            "chance_for_spawn_2": self.chance_for_spawn_2,
            "chance_for_spawn_4": self.chance_for_spawn_4,
            "chance_for_spawn_G": self.chance_for_spawn_G,
        }

    model_config = pydantic_settings.SettingsConfigDict(env_file="../.env")


with open("user_setting.json", "r") as file:
    json_data = json.load(file)
settings = Settings(**json_data)

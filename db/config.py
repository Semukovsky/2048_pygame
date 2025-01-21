import pydantic_settings

import json


class Settings(pydantic_settings.BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    chance_for_spawn_2: int
    chance_for_spawn_4: int
    chance_for_spawn_G: int

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

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

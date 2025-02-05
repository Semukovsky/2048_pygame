import json
import os
import pathlib

import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    chance_for_spawn_2: int
    chance_for_spawn_4: int
    chance_for_spawn_g: int

    @property
    def DATABASE_URL(self):
        return (
                f"postgresql+psycopg2://"
                f"{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/"
                f"{self.DB_NAME}"
        )

    @property
    def SETTINGS_GAME(self):
        return {
            "chance_for_spawn_2": self.chance_for_spawn_2,
            "chance_for_spawn_4": self.chance_for_spawn_4,
            "chance_for_spawn_G": self.chance_for_spawn_g,
        }

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=pathlib.Path(__file__).parent.parent.parent.absolute() / ".env"
    )


base_dir = pathlib.Path(__file__).parent.parent.absolute()
path = os.path.join(base_dir, "game", "user_setting.json")
with open(path, "r") as file:
    json_data = json.load(file)
settings = Settings(**json_data)

import pygame

import game.app as app
import db.connect as connect


def main():
    pygame.init()
    screen_size = (500, 650)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("2048")

    session = connect.SessionLocal()

    app.App(screen, session)


if __name__ == "__main__":
    main()

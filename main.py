import pygame

from game import Game
from settings import GameSettings


def main():
    pygame.init()

    size = (GameSettings.WINDOW_WIDTH, GameSettings.WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(GameSettings.CAPTION)

    done = False
    clock = pygame.time.Clock()

    game = Game()

    while not done:
        done = game.process_events()

        game.run_logic()

        game.display_frame(screen)

        clock.tick(GameSettings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

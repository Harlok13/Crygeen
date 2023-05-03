import pygame
from pygame import QUIT, KEYDOWN, KEYUP, Surface
from pygame.time import Clock

from crygeen import audio
from crygeen.menu import Menu, State

from crygeen.settings import settings


class Game:
    def __init__(self):
        # general setup
        pygame.mixer.pre_init(*audio.MIXER_SETTINGS)
        pygame.init()
        self.screen: Surface = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
            settings.FLAGS,
            settings.BIT_PER_PIXEL
        )
        pygame.display.set_caption(settings.GAME_TITLE)

        self.clock: Clock = pygame.time.Clock()
        self.state = State.SCREENSAVER

        self.menu: Menu = Menu()

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    def __display_menu_buttons(self):
        """
        Displays menu buttons on the screen based on the application state.
        If the application state is 'State.MAIN_MENU', the method starts the menu
        animation and displays all menu buttons. If the mouse is hovering
        over a button, it "fades in" using the 'fade_in_hover' method,
        otherwise it returns to its original value.
        :return:
        """
        if self.state == State.MAIN_MENU:
            self.menu.dropdown_menu_effect()
            for button in self.menu.buttons_list:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.fade_in_hover()
                else:
                    if button.alpha > button.default_alpha:
                        button.alpha -= button.opacity_offset
                        button.surf.set_alpha(button.alpha)
                self.screen.blit(button.surf, button.rect)

    def __event_loop(self):
        """
        Main pygame event loop. Toggle states.
        :return:
        """
        for event in pygame.event.get():
            # TODO create event data (dict)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and self.state == State.SCREENSAVER:
                self.state = State.MAIN_MENU
                # start dropdown menu effect
                self.menu.start_time = pygame.time.get_ticks()

    def run(self):
        while True:
            dt: float = self.clock.tick(settings.FPS) / 1000
            self.__event_loop()

            # set menu
            self.menu.display(self.state, dt)
            self.menu.toggle_music(True)
            self.__display_menu_buttons()

            pygame.display.update()

            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()

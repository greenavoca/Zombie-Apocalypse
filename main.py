import pygame, sys
from level import Level


# main game class
class Game:

    # general setup
    def __init__(self):
        pygame.init()
        self.width = 1280
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.icon = pygame.image.load('graphics/zombie.png')
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption('Zombie Apocalypse')
        self.clock = pygame.time.Clock()
        self.level = Level()

    # time in game
    def game_time(self):
        self.time = int(pygame.time.get_ticks() / 1000) - self.start_time
        font = pygame.font.Font('freesansbold.ttf', 30)
        time_surf = font.render(f'{self.time}', False, 'white').convert_alpha()
        time_rect = time_surf.get_rect(center=(600, 50))
        self.screen.blit(time_surf, time_rect)

    # start the game
    def run(self):

        self.run = True
        self.game_active = False

        while self.run:

            if self.game_active:
                #events
                self.level.event_handler()

                # game over
                if self.level.player_health() <= 0:
                    self.game_active = False

                # window
                self.screen.fill('black')
                dt = self.clock.tick() / 1000
                self.level.run(dt)
                self.game_time()

            else:

                # start and restart
                self.screen.fill('black')
                font = pygame.font.Font('freesansbold.ttf', 30)
                play_surf = font.render(f'Press fire (space) to play', False, 'white').convert_alpha()
                play_rect = play_surf.get_rect(center=(640, 384))
                self.screen.blit(play_surf, play_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and self.game_active == False:
                            self.level.game_restart()
                            self.level.create_player()
                            self.start_time = int(pygame.time.get_ticks() / 1000)
                            self.level.events_timer()
                            self.game_active = True

            pygame.display.update()


if __name__ == '__main__':
    my_game = Game()
    my_game.run()
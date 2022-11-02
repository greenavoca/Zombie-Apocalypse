import pygame, sys
from player import Player
from enemy import Enemy, BigEnemy
from tiles import Tile
from supply import Medkit, Speedbooster, Sharpshooter, Cleaner
from random import randint, choice


# this class has access to all sprites and can manipulate them
class Level:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.map_tiles()

        # player
        self.player = pygame.sprite.GroupSingle()
        self.create_player()

        # enemy
        self.enemy = pygame.sprite.Group()
        self.enemy_pos = ['left', 'right', 'up', 'down']
        self.fast_enemy = pygame.sprite.Group()
        self.big_enemy = pygame.sprite.Group()
        self.enemy_collide_group = pygame.sprite.Group()
        self.enemy_amount = 2
        self.fast_enemy_amount = 1
        self.big_enemy_amount = 1
        self.max_enemy = 15
        self.max_big_enemy = 5
        self.max_fast_enemy = 7

        # supply
        self.supply = pygame.sprite.GroupSingle()
        self.supply_available = ['Medkit', 'Speedbooster', 'Sharpshooter', 'Cleaner']

        # events
        self.enemy_spawn = pygame.USEREVENT + 1
        self.big_enemy_spawn = pygame.USEREVENT + 2
        self.fast_enemy_spawn = pygame.USEREVENT + 3
        self.supply_spawn = pygame.USEREVENT + 4
        self.events_timer()

    # level background
    def map_tiles(self):
        self.tiles = pygame.sprite.Group()
        pos_x = 0
        pos_y = 0
        for tile in range(15):
            self.tiles.add(Tile((pos_x, pos_y)))
            pos_x += 256
            if tile in (4, 9):
                pos_x = 0
                pos_y += 256


    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.enemy_spawn:
                if len(self.enemy) < self.max_enemy:
                    for enemy in range(int(self.enemy_amount)):
                        self.create_enemy(1, choice(self.enemy_pos))
                    self.enemy_amount += 0.5
                    if self.enemy_amount > self.max_enemy:
                        self.enemy_amount = self.max_enemy
            if event.type == self.fast_enemy_spawn:
                if len(self.fast_enemy) < self.max_fast_enemy:
                    for fast_enemy in range(int(self.fast_enemy_amount)):
                        self.create_fast_enemy(1, choice(self.enemy_pos), speed=3)
                    self.fast_enemy_amount += 0.25
                    if self.fast_enemy_amount > self.max_fast_enemy:
                        self.fast_enemy_amount = self.max_fast_enemy
            if event.type == self.big_enemy_spawn:
                if len(self.big_enemy) < self.max_big_enemy:
                    for big_enemy in range(int(self.big_enemy_amount)):
                        self.create_big_enemy(int(self.big_enemy_amount))
                    self.big_enemy_amount += 0.25
                    if self.big_enemy_amount > self.max_big_enemy:
                        self.big_enemy_amount = self.max_big_enemy
            if event.type == self.supply_spawn:
                sup = choice(self.supply_available)
                pos_x = randint(20, 1200)
                pos_y = randint(20, 700)
                match sup:
                    case 'Medkit':
                        self.supply.add(Medkit(self, (pos_x, pos_y), self.player.sprite, sup, (40, 30), 8000))
                    case 'Speedbooster':
                        self.supply.add(Speedbooster(self, (pos_x, pos_y), self.player.sprite, sup, (40, 30), 8000))
                    case 'Sharpshooter':
                        self.supply.add(Sharpshooter(self, (pos_x, pos_y), self.player.sprite, sup, (30, 40), 8000))
                    case 'Cleaner':
                        self.supply.add(Cleaner(self, (pos_x, pos_y), self.player.sprite, sup, (40, 40), 8000))


    def events_timer(self):
        pygame.time.set_timer(self.enemy_spawn, 15000)
        pygame.time.set_timer(self.big_enemy_spawn, 60000)
        pygame.time.set_timer(self.fast_enemy_spawn, 30000)
        pygame.time.set_timer(self.supply_spawn, 20000)


    def create_player(self):
        self.player.add(Player((600, 700)))


    def player_health(self) -> int:
        return self.player.sprite.health


    def game_restart(self):
        for enemy in self.enemy:
            enemy.kill()
        for fast_enemy in self.fast_enemy:
            fast_enemy.kill()
        for big_enemy in self.big_enemy:
            big_enemy.kill()
        self.player.sprite.health = 100
        self.enemy_amount = 2
        self.fast_enemy_amount = 1
        self.big_enemy_amount = 1


    def create_enemy(self, number, pos, speed=1):
        for enemy in range(number):
            match pos:
                case 'up':
                    self.enemy.add(Enemy(self, (randint(0, 1248), -100), self.player.sprite, speed))
                case 'down':
                    self.enemy.add(Enemy(self, (randint(0, 1248), 850), self.player.sprite, speed))
                case 'left':
                    self.enemy.add(Enemy(self, (-100, randint(0, 736)), self.player.sprite, speed))
                case 'right':
                    self.enemy.add(Enemy(self, (1400, randint(0, 736)), self.player.sprite, speed))


    def create_fast_enemy(self, number, pos, speed=3):
        for enemy in range(number):
            match pos:
                case 'up':
                    self.enemy.add(Enemy(self, (randint(0, 1248), -100), self.player.sprite, speed))
                case 'down':
                    self.enemy.add(Enemy(self, (randint(0, 1248), 850), self.player.sprite, speed))
                case 'left':
                    self.enemy.add(Enemy(self, (-100, randint(0, 736)), self.player.sprite, speed))
                case 'right':
                    self.enemy.add(Enemy(self, (1400, randint(0, 736)), self.player.sprite, speed))


    def create_big_enemy(self, number, speed=1):
        for enemy in range(number):
            self.big_enemy.add(BigEnemy(self, (1312, randint(0, 736)), self.player.sprite, speed, 500))


    def run(self, dt):
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.player.update(dt)
        self.enemy.draw(self.display_surface)
        self.enemy.update(dt)
        self.fast_enemy.draw(self.display_surface)
        self.fast_enemy.update(dt)
        self.big_enemy.draw(self.display_surface)
        self.big_enemy.update(dt)
        self.supply.draw(self.display_surface)
        self.supply.update()

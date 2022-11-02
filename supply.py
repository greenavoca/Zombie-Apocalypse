import pygame


# abstract class
class Supply(pygame.sprite.Sprite):

    def __init__(self, game, pos, player, img: str, size: tuple, end_time: int):
        super().__init__()
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load('graphics/supply/' + img + '.png').convert_alpha(), size)
        self.rect = self.image.get_rect(center=pos)
        self.player = player
        self.end = pygame.time.get_ticks() + end_time

    def action(self):
        pass

    def disappear(self):
        if pygame.time.get_ticks() >= self.end:
            self.kill()

    def update(self):
        self.action()
        self.disappear()


# adds player hp
class Medkit(Supply):

    def action(self):
        if self.rect.colliderect(self.player):
            med_sound = pygame.mixer.Sound('audio/heal.wav')
            med_sound.play()
            self.player.health += 60
            if self.player.health >= 100:
                self.player.health = 100
            self.kill()


# increases player speed
class Speedbooster(Supply):

    def action(self):
        if self.rect.colliderect(self.player):
            speed_sound = pygame.mixer.Sound('audio/speed_up.wav')
            speed_sound.play()
            self.player.speed += 20
            self.kill()


# increases bullet speed
class Sharpshooter(Supply):

    def action(self):
        if self.rect.colliderect(self.player):
            reload_sound = pygame.mixer.Sound('audio/reload.wav')
            reload_sound.play()
            self.player.bullet_speed += 20
            self.kill()


# removes all enemies
class Cleaner(Supply):

    def action(self):
        if self.rect.colliderect(self.game.player.sprite):
            explo_sound = pygame.mixer.Sound('audio/cleaner_explo.flac')
            explo_sound.play()
            for enemy in self.game.enemy.sprites():
                enemy.kill()
            for f_enemy in self.game.fast_enemy.sprites():
                f_enemy.kill()
            for b_enemy in self.game.big_enemy.sprites():
                b_enemy.kill()
            self.kill()
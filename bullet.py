import pygame
from support import import_folder


class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos, direction, speed, angle):
        super().__init__()
        self.direction = direction
        self.angle = angle
        self.pic = pygame.image.load('graphics/bomb.png').convert_alpha()
        self.image = pygame.transform.rotate(self.pic, self.angle)
        self.rect = self.image.get_rect(midbottom=pos)
        self.state = 'fire'
        self.speed = speed
        self.pos = pygame.math.Vector2(self.rect.center)

        # explosion
        self.explosion = import_folder('graphics/explosion/', (64, 64))
        self.frame_index = 0
        self.animation_speed = 15
        self.explosion_sound = True


    def animate(self, dt):
        # bullet animation
        if self.state == 'fire':
            self.image = self.image

        # explosion animation
        if self.state == 'explosion':
            self.direction.x = 0
            self.direction.y = 0

            self.frame_index += self.animation_speed * dt
            if self.frame_index >= 11:
                self.frame_index = 0
                self.kill()
            image = self.explosion[int(self.frame_index)]
            self.image = image
            if round(self.frame_index) == 1 and self.explosion_sound:
                explo = pygame.mixer.Sound('audio/explosion01.wav')
                explo.play()
                self.explosion_sound = False


    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

        # boundary
        if self.rect.y <= -64:
                self.kill()
        if self.rect.y >= 864:
                self.kill()
        if self.rect.x <= -64:
                self.kill()
        if self.rect.x >= 1264:
                self.kill()


    def update(self, dt):
        self.animate(dt)
        self.move(dt)

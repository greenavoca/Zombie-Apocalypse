import pygame, math
from bullet import Bullet
from support import import_folder


class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.surface = pygame.display.get_surface()
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.status = 'idle'
        self.direction = pygame.math.Vector2(0, -1)
        self.pos = pygame.math.Vector2(pos)
        self.speed = 120
        self.movement = 0
        self.health = 100
        self.damage = 100

        # bullet
        self.bullet = pygame.sprite.GroupSingle()
        self.bullet_speed = 300


    def display_hp(self):
        font = pygame.font.Font('freesansbold.ttf', 30)
        hp_surf = font.render(f'HP: {self.health}', False, 'white').convert_alpha()
        hp_rect = hp_surf.get_rect(center=(100, 50))
        self.surface.blit(hp_surf, hp_rect)


    def import_player_assets(self):
        player_path = 'graphics/player/'
        self.animations = {'idle': [], 'move': [], 'reload': [], 'shoot': []}

        for animation in self.animations.keys():
            full_path = player_path + animation
            self.animations[animation] = import_folder(full_path, (64, 64))


    def animate(self, dt):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        self.image = image


    def get_input(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.rotate_ip(dt * -360)

        if keys[pygame.K_RIGHT]:
            self.direction.rotate_ip(dt * 360)

        self.angle = self.direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if keys[pygame.K_UP]:
            self.movement = 1
            self.status = 'move'
        else:
            self.movement = 0
            self.status = 'idle'

        if keys[pygame.K_DOWN]:
            self.movement = -1
            self.status = 'move'

        if keys[pygame.K_SPACE] and not self.bullet.sprites():
            self.create_bullet()
            shoot = pygame.mixer.Sound('audio/rumble.flac')
            shoot.play()


    def move(self, speed, dt):
        movement_v = self.direction * self.movement
        if movement_v.length() > 0:
            movement_v.normalize_ip()
            self.pos += movement_v * dt * speed
            self.rect = self.image.get_rect(center=self.pos)

        # boundary
        if self.pos.x <= 32:
            self.pos.x = 32
        if self.pos.x >= 1236:
            self.pos.x = 1236
        if self.pos.y <= 32:
            self.pos.y = 32
        if self.pos.y >= 736:
            self.pos.y = 736


    def create_bullet(self):
        x = 15
        y = -10

        # keeps bullet starting point on proper position
        if self.angle <= -10 and self.angle > -15:
            x = 18
        elif self.angle <= -15 and self.angle > -20:
            x = 22
        elif self.angle <= -20 and self.angle > -25:
            x = 24
        elif self.angle <= -25 and self.angle > -30:
            x = 26
        elif self.angle <= -30 and self.angle > -40:
            x = 27
        elif self.angle <= -40 and self.angle > -50:
            x = 29
        elif self.angle <= -50 and self.angle > -60:
            x = 30
            y = -22
        elif self.angle <= -60 and self.angle > -70:
            x = 28
            y = -22
        elif self.angle <= -70 and self.angle > -80:
            x = 28
            y = -26
        elif self.angle <= -80 and self.angle > -90:
            x = 26
            y = -26
        elif self.angle <= -80 and self.angle > -90:
            x = 26
            y = -28
        elif self.angle <= -90 and self.angle > -110:
            x = 28
            y = -30
        elif self.angle <= -110 and self.angle > -120:
            x = 26
            y = -32
        elif self.angle <= -120 and self.angle > -130:
            x = 26
            y = -36
        elif self.angle <= -120 and self.angle > -160:
            x = 25
            y = -40
        elif self.angle <= -160 and self.angle > -170:
            x = 20
            y = -38
        elif self.angle <= -170 and self.angle > -180:
            x = 18
            y = -42
        elif self.angle <= -180 and self.angle > -200:
            y = -50
        elif self.angle <= -200 and self.angle > -220:
            x = 6
            y = -50
        elif self.angle <= -220 and self.angle > -240:
            x = 4
            y = -45
        elif self.angle <= -240 and self.angle > -260:
            x = 3
            y = -35
        elif self.angle <= -260 and self.angle > -270:
            x = 4
            y = -35
        elif self.angle <= 90 and self.angle > 70:
            x = 4
            y = -35
        elif self.angle <= 70 and self.angle > 50:
            x = 4
            y = -25
        elif self.angle <= 50 and self.angle > 30:
            x = 4
            y = -18
        elif self.angle <= 30 and self.angle > 10:
            x = 10
            y = -15

        offset = pygame.math.Vector2(x, y)
        radians = math.radians(-self.angle)
        ax, ay = offset.rotate_rad(radians)
        pos = pygame.math.Vector2(self.rect.center)
        self.bullet.add(Bullet((pos.x+ax, pos.y+ay), self.direction.normalize(), self.bullet_speed, self.angle))


    def update(self, dt):
        self.bullet.draw(self.surface)
        self.bullet.update(dt)
        self.animate(dt)
        self.display_hp()
        self.get_input(dt)
        self.move(self.speed, dt)

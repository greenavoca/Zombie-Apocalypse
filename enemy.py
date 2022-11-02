import pygame, random
from support import import_folder, import_audio


class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, pos, player, speed, hp=100):
        super().__init__()
        self.game = game
        self.import_enemy_assets()
        self.import_enemy_audio()
        self.frame_index = 0
        self.animation_speed = 15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.status = 'idle'
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = speed
        self.player = player
        self.health = hp
        self.cooldown = 0
        self.blood = pygame.sprite.GroupSingle()
        self.surf = pygame.display.get_surface()


    def import_enemy_assets(self):
        enemy_path = 'graphics/enemy/'
        self.animations = {'idle': [], 'move': [], 'attack': []}

        for animation in self.animations.keys():
            full_path = enemy_path + animation
            self.animations[animation] = import_folder(full_path, (64, 64))


    def import_enemy_audio(self):
        audio_path = 'audio/dead/'
        self.dead_audio = import_audio(audio_path)


    def animate(self, dt):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animation):
            self.frame_index = 0

        if self.health > 0:
            if self.direction.x != 0 or self.direction.y != 0:
                self.status = 'move'
            else:
                self.status = 'idle'

            if self.rect.colliderect(self.player):
                self.status = 'attack'

        image = animation[int(self.frame_index)]

        # image rotation
        target_distance = self.player.pos - self.pos
        self.angle = target_distance.angle_to(pygame.math.Vector2(1,0))
        self.image = pygame.transform.rotate(image, self.angle)

        # death
        if self.health <= 0:
            dead_sound = random.choice(self.dead_audio)
            dead_sound.play()
            self.kill()


    def move(self, dt):

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

        # move toward player
            # horizontal
        if self.rect.x < self.player.rect.x - 31:
            self.direction.x = 60
        elif self.rect.x > self.player.rect.x + 31:
            self.direction.x = -60
        else:
            self.direction.x = 0

        #     # vertical
        if self.rect.y < self.player.rect.y - 31:
            self.direction.y = 60
        elif self.rect.y > self.player.rect.y + 31:
            self.direction.y = -60
        else:
            self.direction.y = 0


    def collision_with_bullet(self):

        if self.player.bullet.sprite is not None:
            if self.rect.colliderect(self.player.bullet.sprite.rect):
                if self.player.bullet.sprite.state == 'fire':
                    self.health -= self.player.damage
                self.player.bullet.sprite.state = 'explosion'


    def attack(self):
        if self.status == 'attack':
            self.cooldown += 1
            if self.cooldown == 80:
                self.player.health -= 20
                self.cooldown = 0


    def collision_enemies(self):
        for enemy in self.game.enemy:
            if enemy != self:
                distance = self.pos - enemy.pos
                if 0 < distance.length() < 50:
                    self.pos += distance.normalize()

        for enemy in self.game.fast_enemy:
            if enemy != self:
                distance = self.pos - enemy.pos
                if 0 < distance.length() < 50:
                    self.pos += distance.normalize()

        for enemy in self.game.big_enemy:
            if enemy != self:
                distance = self.pos - enemy.pos
                if 0 < distance.length() < 50:
                    self.pos += distance.normalize()


    def update(self, dt):
        self.attack()
        self.move(dt)
        self.collision_with_bullet()
        self.collision_enemies()
        self.animate(dt)


class BigEnemy(Enemy):

    # overwriting method to get image 128x128 px
    def import_enemy_assets(self):
        enemy_path = 'graphics/enemy/'
        self.animations = {'idle': [], 'move': [], 'attack': []}

        for animation in self.animations.keys():
            full_path = enemy_path + animation
            self.animations[animation] = import_folder(full_path, (128, 128))


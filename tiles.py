import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('graphics/tile.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
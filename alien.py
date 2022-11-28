import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Класс, представляющий одного пришельца """

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # Загружаем изображение врага и создаем приямоугольник
        self.image = pygame.image.load('images/star_fighter.bmp')
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется в вехнем левом углу
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Сохранение точной горизонтальной позиции
        self.x = float(self.rect.x)

    def check_edges(self):
        """ Возвращает True при достижении края экрана """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """ Перемещение позиции вражеского корабля вправо и влево """
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x


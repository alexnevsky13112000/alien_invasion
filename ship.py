import pygame


class Ship():
    """ Класс для управления кораблем """
    def __init__(self, ai_game):
        """ Инициализация корабля и его начальной координаты """
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images\\сокол.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        # Сохранение вещественной координаты
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # Флаги перемещения
        self.moving_right_flag = False
        self.moving_left_flag = False
        self.moving_up_flag = False
        self.moving_down_flag = False

    def update(self):
        """ Обновляет позицию корабля с учетом флага """
        if self.moving_right_flag and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left_flag and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up_flag and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down_flag and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        # Обновление атрибута rect исходя из self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blit_me(self):
        """ Рисует корабль """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


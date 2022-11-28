class Settings():
    """ Класс для хранения всех настроек игры Alien Invasion """

    def __init__(self):
        """ Иницилизирует настройки игры """
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 600
        # self.bg_color = (41, 41, 61)
        self.bg_color = (0, 0, 0)
        # Парметры корабля
        # self.ship_speed = 1.0
        self.ship_limit = 3
        # Параметры выстрела
        self.bullets_color = (0, 255, 0)
        self.bullet_speed = 1.75
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allow = 10
        # Параметры вражеских кораблей
        # self.alien_speed = 0.35
        self.fleet_drop_speed = 7.5
        # Повышение сложности игры
        self.speed_scale = 1.15
        self.score_scale = 1.5
        # fleet_direction = 1 обозначает движение вправо, а -1 - влево
        self.fleet_direction = 1
        # Стоимость пришельца
        # self.alien_points = 50
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Инициализация настроек, изменяющихся во время игры """
        self.ship_speed = 1.0
        self.bullet_speed = 1.5
        self.alien_speed = 0.35
        self.alien_points = 50

    def increase_speed(self):
        """ Увеличение настройки скорости """
        self.ship_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale
        self.alien_speed *= self.speed_scale
        self.alien_points = int(self.alien_points * self.score_scale)






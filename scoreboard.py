import pygame.font
from lives import Lives
from pygame.sprite import Group
import json


class ScoreBoard():
    """ Класс для вывода текущей информации о игре """
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats
        # Настройки шрифта для вывода счета
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 28)
        # Подготовка исходного изображения
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_lives(self):
        """ Отображает количетсво оставшихся жизней """
        self.lives = Group()
        for live_number in range(self.stats.ships_left):
            live = Lives(self.ai_game)
            live.rect.x = 10 + live_number * live.rect.width
            live.rect.y = 10
            self.lives.add(live)

    def prep_level(self):
        level_str = "Wave:  " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_score(self):
        """ Преобразование текущего счета в картинку """
        rounded_score = round(self.stats.score, -1)
        score_str = "Current Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        # Вывод счета в правом верхнем углу
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ Преобразование текущего рекорда в картинку """
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: {:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        # Рекорд выравниваем по середине экрана и на высоте текущего счета
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """ Проверка рекорда """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
        with open("highest_score.json", 'w') as f:
            json.dump(self.stats.high_score, f)

    def show_score(self):
        """ Вывод игровой статистики """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.lives.draw(self.screen)
import json


class GameStats():
    """ Отсеживание статистики игры """
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        with open('highest_score.json') as f:
            h_s = json.load(f)
        self.high_score = h_s

    def reset_stats(self):
        """ Инициализирует статистику, изменяющуюся в ходе игры """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

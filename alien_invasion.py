import sys,pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button
from game_stats import GameStats
from scoreboard import ScoreBoard


class AlienInvasion:
    """ Класс для управления ресурсами и поведением игры """
    def __init__(self):
        """ Инициализирует игру и создает игровые ресурсы """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        self.screen_picture = pygame.image.load('images/star_sky#2.jpg')
        self.screen_picture_rect = self.screen_picture.get_rect()
        # Полноэкранный режим
        """self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height"""
        pygame.display.set_caption('Alien Invasion. Enter "Q" to exit. Enter "P" to start the game.')
        # Создание экземпляра для хранения игровой статистики и панели результатов
        self.stats = GameStats(self)
        self.score_board = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, 'Play', self.screen_rect.centerx, self.screen_rect.centery)
        quit_position = self.play_button.rect.y + 100
        self.quit_button = Button(self, 'Quit', self.screen_rect.centerx, quit_position)

    def check_events(self):
        """ Обрабатывает нажатия клавиш и события мыши """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)
                self.check_quit_button(mouse_pos)

    def check_keydown_events(self, event):
        """ Реагирует на нажатие клавиш - стрелок """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right_flag = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left_flag = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up_flag = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down_flag = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullets()
        elif event.key == pygame.K_p:
            # self.stats.game_active = True
            self.start_game()
        elif event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right_flag = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left_flag = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up_flag = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down_flag = False

    def fire_bullets(self):
        """ Создание нового снаряда и включение его в группу bullets """
        if len(self.bullets) < self.settings.bullets_allow:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def check_play_button(self, mouse_pos):
        """ Запускает новую игру при нажатии кнопки Play """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.start_game()

    def check_quit_button(self, mouse_pos):
        button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            sys.exit()

    def start_game(self):
        # Сброс игровой статистики
        self.stats.reset_stats()
        self.stats.game_active = True
        self.score_board.prep_score()
        self.score_board.prep_level()
        self.score_board.prep_lives()
        # Очистка списков пришельцев и снарядов
        self.aliens.empty()
        self.bullets.empty()
        self.settings.initialize_dynamic_settings()
        # Создание нового флота
        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)

    def _create_fleet(self):
        """ Создание флота пришельца """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Определение количества кораблей по длине экрана
        available_space_x = self.settings.screen_width - (2 * alien_width)
        numbers_aliens_x = available_space_x // (2 * alien_width)
        # Определение количества рядов кораблей по высоте экрана
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        numbers_rows = available_space_y // (2 * alien_height)
        # Создание флота пришельцев
        for row_number in range(numbers_rows):
            for alien_number in range(numbers_aliens_x):
                self.create_alien(alien_number, row_number)

    def create_alien(self, alien_number, number_row):
        """ Создание пришельца и размещение его в ряду """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien.rect.height +
                        2 * alien.rect.height * number_row)
        self.aliens.add(alien)

    def update_aliens(self):
        """ Обновление позиций кораблей вражеского флота и проверка достижения края """
        self.check_fleet_edges()
        self.aliens.update()
        # Проверка коллизий врага и корабля
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        self.check_aliens_bottom()

    def change_fleet_direction(self):
        """ Опускает флот вниз и меняет направление """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_fleet_edges(self):
        """ Реакция на достижение кораблем края экрана """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_aliens_bottom(self):
        """ Отслеживание прикосновения пришельца нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def update_bullets(self):
        """ Обновляет позици снаряюов и уничтожает старые снаряды """
        # Обновление позиции снарядов
        self.bullets.update()
        # Удаление снарядов вышедших за экран
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        # Поиск коллизий снарядов и вражеских кораблей
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        # Обновление счета
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.score_board.prep_score()
            self.score_board.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.score_board.prep_level()

    def ship_hit(self):
        """ Обработка столкновений корабля с врагом """
        if self.stats.ships_left - 1 > 0:
            self.stats.ships_left -= 1
            self.score_board.prep_lives()
            # Сброс списков флота и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()
            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def update_screen(self):
        """ Обновление экрана """
        # self.screen.fill(self.settings.bg_color)  # При каждом проходе цикла перерисовывается экран
        self.screen.blit(self.screen_picture, self.screen_picture_rect)
        self.ship.blit_me()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.score_board.show_score()
        # Кнопка Play отображается в том случае если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.quit_button.draw_button()
        pygame.display.flip()  # Отслеживание последнего прорисованного экрана

    def run_game(self):
        """ Запуск основного цикла событий игры """
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()


if __name__ == '__main__':
    """ Создание экземпляра класса и запуск игры """
    ai = AlienInvasion()
    ai.run_game()
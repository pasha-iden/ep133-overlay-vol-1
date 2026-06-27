import pygame
from data import config


class SquareRenderer:
    def __init__(self, font):
        self.font = font

    def get_square_color(self, active):
        """Возвращает цвет квадратика в зависимости от active (1 = красный, 0 = серый)"""
        if active == 1:
            return config.SQUARE_COLOR_WHITE
        else:
            return config.SQUARE_COLOR_GRAY

    def draw_square(self, surface, x, y, active, scale_factor=1.0):
        """Рисует один квадратик на указанной поверхности в позиции (x, y)"""
        color = self.get_square_color(active)

        # Ширина с учётом масштаба
        square_width = int(config.SQUARE_WIDTH * scale_factor)
        square_height = config.SQUARE_HEIGHT

        # Применяем смещение из конфига
        x_pos = x + config.SQUARE_OFFSET_X
        y_pos = y + config.SQUARE_OFFSET_Y

        square_rect = pygame.Rect(x_pos, y_pos, square_width, square_height)
        pygame.draw.rect(surface, color, square_rect)

    def draw_squares_at_positions(self, surface, positions_data, scale_factor=1.0):
        """
        Рисует квадратики в указанных позициях

        positions_data: список словарей с ключами:
            - 'x', 'y': координаты левого верхнего угла ячейки
            - 'active': 1 или 0 (красный или серый)
        scale_factor: коэффициент масштабирования (из config.SEQUENCE_SCALE)
        """
        for data in positions_data:
            self.draw_square(surface, data['x'], data['y'], data['active'], scale_factor)
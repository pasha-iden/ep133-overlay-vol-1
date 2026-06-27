import pygame
from data import config
from data.sequence_events import SQUARE_EVENTS
from core.square_renderer import SquareRenderer


class SequenceRenderer:
    def __init__(self, font):
        self.font = font
        font_size = font.get_height()
        self.bold_font = pygame.font.SysFont('Courier New', font_size, bold=True)
        self.char_width = self.get_max_char_width()
        self.square_renderer = SquareRenderer(font)
        self.star_positions = {}

    def get_max_char_width(self):
        test_chars = ['[', ']', '|', 'I', ' ', '(', ')', '{', '}', '·']
        max_width = 0
        for char in test_chars:
            surface = self.bold_font.render(char, True, config.COLOR_DARK)
            max_width = max(max_width, surface.get_width())
        return max_width + 1

    def process_lines(self, sequence_lines):
        """
        1. Находит самую длинную строку
        2. Продлевает все строки до её длины пробелами
        3. Проходит по каждому НЕЧЁТНОМУ символу (индексы 0, 2, 4...)
           и если это пробел - заменяет на '·'
        """
        max_length = max(len(line) for line in sequence_lines)
        processed_lines = []

        for line in sequence_lines:
            if len(line) < max_length:
                line = line + ' ' * (max_length - len(line))

            chars = list(line)
            for i in range(0, len(chars), 2):
                if chars[i] == ' ':
                    chars[i] = '·'

            processed_lines.append(''.join(chars))

        return processed_lines

    def render_extra_bold(self, char_surface, color):
        w = char_surface.get_width() + 2
        h = char_surface.get_height() + 2
        extra_bold_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        offsets = [(-1, -1), (-1, 0), (0, -1)]
        for dx, dy in offsets:
            extra_bold_surface.blit(char_surface, (dx + 1, dy + 1))
        return extra_bold_surface

    def convert_and_get_style(self, char):
        """Все символы жирные"""
        if char == '*':
            return None

        if char == '·':
            return ('·', config.COLOR_LIGHT, True)

        if char == '{':
            return ('[', config.COLOR_LIGHT, True)
        elif char == '}':
            return (']', config.COLOR_LIGHT, True)
        elif char == '/' or char == '\\':
            return ('|', config.COLOR_LIGHT, True)
        elif char == 'I':
            return ('I', config.COLOR_DARK, True)
        elif char == '[':
            return ('[', config.COLOR_DARK, True)
        elif char == ']':
            return (']', config.COLOR_DARK, True)
        elif char == '|':
            return ('|', config.COLOR_DARK, True)
        else:
            return (char, config.COLOR_DARK, True)

    def get_active_squares(self, current_time):
        active_squares = []
        for event in SQUARE_EVENTS:
            if event['start'] <= current_time <= event['end']:
                active_squares.append({
                    'line': event['line'],
                    'place': event['place'],
                    'active': event['active']
                })
        return active_squares

    def render_sequence(self, sequence_lines, current_time):
        # Обрабатываем строки (дополняем и расставляем точки)
        processed_lines = self.process_lines(sequence_lines)
        raw_surface = self._render_raw(processed_lines, current_time)

        if config.SEQUENCE_SCALE != 1.0:
            new_width = max(1, int(raw_surface.get_width() * config.SEQUENCE_SCALE))
            new_height = raw_surface.get_height()
            scaled_surface = pygame.transform.smoothscale(raw_surface, (new_width, new_height))
            return scaled_surface
        return raw_surface

    def _render_raw(self, sequence_lines, current_time):
        max_line_length = 0
        for line in sequence_lines:
            line_length = sum(1 for char in line if char != '*')
            max_line_length = max(max_line_length, line_length)

        total_width = max_line_length * self.char_width
        total_height = len(sequence_lines) * (self.font.get_height() + 5)

        surface = pygame.Surface((total_width + 100, total_height + 100), pygame.SRCALPHA)
        y_offset = 0
        line_height = self.font.get_height()

        active_squares = self.get_active_squares(current_time)
        square_map = {(sq['line'], sq['place']): sq['active'] for sq in active_squares}
        self.star_positions = {}

        for line_idx, line in enumerate(sequence_lines):
            x_offset = 0
            place_counter = 0

            for char_idx, char in enumerate(line):
                style_result = self.convert_and_get_style(char)

                if style_result is None:
                    place_counter += 1
                    self.star_positions[(line_idx, char_idx)] = {
                        'x': x_offset,
                        'y': y_offset,
                        'place': place_counter
                    }
                    empty_surface = pygame.Surface((self.char_width, line_height), pygame.SRCALPHA)
                    surface.blit(empty_surface, (x_offset, y_offset))
                    x_offset += self.char_width
                else:
                    display_char, color, use_bold = style_result

                    if use_bold:
                        char_surface = self.bold_font.render(display_char, True, color)
                        char_surface = self.render_extra_bold(char_surface, color)
                    else:
                        char_surface = self.font.render(display_char, True, color)

                    cell_surface = pygame.Surface((self.char_width, char_surface.get_height()), pygame.SRCALPHA)
                    x_centered = (self.char_width - char_surface.get_width()) // 2
                    cell_surface.blit(char_surface, (x_centered, 0))

                    if display_char == 'I':
                        surface.blit(cell_surface, (x_offset, y_offset + 1))
                    else:
                        surface.blit(cell_surface, (x_offset, y_offset))

                    x_offset += self.char_width

            y_offset += line_height + 5

        squares_to_draw = []
        for (line_idx, char_idx), pos_data in self.star_positions.items():
            place_num = pos_data['place']
            if (line_idx, place_num) in square_map:
                squares_to_draw.append({
                    'x': pos_data['x'],
                    'y': pos_data['y'],
                    'active': square_map[(line_idx, place_num)]
                })

        if squares_to_draw:
            self.square_renderer.draw_squares_at_positions(surface, squares_to_draw, config.SEQUENCE_SCALE)

        return surface
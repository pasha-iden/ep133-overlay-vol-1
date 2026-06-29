import pygame
from data import config
from data import sequence


class SequenceLoader:
    def __init__(self, font):
        self.font = font
        font_size = font.get_height()
        self.bold_font = pygame.font.SysFont('Courier New', font_size, bold=True)
        self.char_width = self.get_max_char_width()
        self.star_positions = {}

    def get_max_char_width(self):
        test_chars = ['[', ']', '|', 'I', ' ', '(', ')', '{', '}', '·']
        max_width = 0
        for char in test_chars:
            surface = self.bold_font.render(char, True, config.COLOR_DARK)
            max_width = max(max_width, surface.get_width())
        return max_width + 1

    def process_lines(self, sequence_lines):
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

    def is_inside_brackets(self, line, char_index):
        char = line[char_index]

        if char in '[{':
            return True

        if char in ']}':
            depth = 0
            for i, ch in enumerate(line):
                if ch in '[{':
                    depth += 1
                elif ch in ']}':
                    depth -= 1
                if i == char_index:
                    return depth == 0
            return False

        depth = 0
        for i, ch in enumerate(line):
            if i == char_index:
                return depth > 0
            if ch in '[{':
                depth += 1
            elif ch in ']}':
                depth -= 1
        return False

    def get_char_weight(self, line, char_index, slow_speed=0.3):
        if self.is_inside_brackets(line, char_index):
            return slow_speed
        return 1.0

    def get_visible_length(self, line, progress, slow_speed=0.3):
        if progress <= 0:
            return 0
        if progress >= 1.0:
            return len(line)

        total_weight = 0
        for i in range(len(line)):
            total_weight += self.get_char_weight(line, i, slow_speed)

        target_weight = total_weight * progress

        current_weight = 0
        visible = 0
        for i in range(len(line)):
            current_weight += self.get_char_weight(line, i, slow_speed)
            if current_weight <= target_weight:
                visible += 1
            else:
                break

        return visible

    def render_loading_sequence(self, sequence_lines, current_time, pos_x, pos_y, scale_factor=1.0):
        if current_time < config.LOADER_START_TIME:
            return None

        if current_time > config.LOADER_END_TIME:
            return None

        total_duration = config.LOADER_FINISH_TIME - config.LOADER_START_TIME
        if total_duration <= 0:
            progress = 1.0
        else:
            progress = min((current_time - config.LOADER_START_TIME) / total_duration, 1.0)

        processed_lines = self.process_lines(sequence_lines)
        raw_surface = self._render_raw_with_progress(processed_lines, progress)

        if scale_factor != 1.0:
            new_width = max(1, int(raw_surface.get_width() * scale_factor))
            new_height = raw_surface.get_height()
            scaled_surface = pygame.transform.smoothscale(raw_surface, (new_width, new_height))
            return scaled_surface

        return raw_surface

    def _render_raw_with_progress(self, sequence_lines, progress):
        max_line_length = 0
        for line in sequence_lines:
            line_length = sum(1 for char in line if char != '*')
            max_line_length = max(max_line_length, line_length)

        total_width = max_line_length * self.char_width
        total_height = len(sequence_lines) * (self.font.get_height() + 5)

        surface = pygame.Surface((total_width + 100, total_height + 100), pygame.SRCALPHA)
        y_offset = 0
        line_height = self.font.get_height()

        slow_speed = config.BRACKET_LOAD_SPEED

        for line_idx, line in enumerate(sequence_lines):
            line_progress = min(progress, 1.0)

            visible_chars = self.get_visible_length(line, line_progress, slow_speed)
            visible_line = line[:visible_chars]

            x_offset = 0
            for char in visible_line:
                style_result = self.convert_and_get_style(char)

                if style_result is None:
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

        return surface
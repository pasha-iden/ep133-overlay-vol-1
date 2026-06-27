import pygame
from data import config
from data.text_script import ASCII_TEXT, INFO_LINES, START_LOGS


def render_ascii_animation(screen, current_time, window_x, window_y, window_width, window_height):
    """
    Рендерит ASCII-арт, INFO-строки и логи.
    Возвращает True, если анимация активна.
    """
    if current_time < config.ASCII_APPEAR_TIME:
        return False

    font_size = config.FONT_SIZE_SEQUENCE
    font = pygame.font.SysFont(config.FONT_NAME, font_size)
    line_height = font_size + 2

    surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    surface.fill(config.BACKGROUND_COLOR)

    y_offset = 20

    total_ascii_lines = len(ASCII_TEXT)
    total_info_lines = len(INFO_LINES)
    total_logs = len(START_LOGS)

    # ===== ASCII-арт =====
    for i, line in enumerate(ASCII_TEXT):
        appear_time = config.ASCII_APPEAR_TIME + i * config.LINE_INTERVAL
        if current_time >= appear_time:
            disappear_time = config.ASCII_DISAPPEAR_TIME + i * config.LINE_INTERVAL
            if current_time < disappear_time:
                text_surface = font.render(line, True, config.COLOR_DARK)
                surface.blit(text_surface, (20, y_offset))
        y_offset += line_height

    y_offset += 20

    # ===== INFO-строки =====
    info_start_time = config.ASCII_APPEAR_TIME + total_ascii_lines * config.LINE_INTERVAL + 0.5

    for i, line in enumerate(INFO_LINES):
        appear_time = info_start_time + i * config.LINE_INTERVAL
        if current_time >= appear_time:
            disappear_time = config.ASCII_DISAPPEAR_TIME + i * config.LINE_INTERVAL
            if current_time < disappear_time:
                text_surface = font.render(line, True, config.COLOR_DARK)
                surface.blit(text_surface, (20, y_offset))
        y_offset += line_height

    # ===== ОТСТУП МЕЖДУ INFO И ЛОГАМИ =====
    y_offset += 40

    # ===== Логи (бегущая строка) =====
    logs_start_time = config.LOGS_START_TIME

    if current_time >= logs_start_time:
        elapsed = current_time - logs_start_time

        # Определяем, какой лог должен показываться
        current_log_index = int(elapsed // config.LOGS_INTERVAL)

        # Если все логи уже показаны — переходим в финальное состояние
        if current_log_index >= total_logs:
            # Финальное состояние
            status_text = "Status: Ready."
            play_text = "PRESS PLAY"
            status_surface = font.render(status_text, True, config.COLOR_DARK)
            play_surface = font.render(play_text, True, config.COLOR_DARK)

            play_x = (window_width - play_surface.get_width()) // 2
            play_y = (window_height - play_surface.get_height()) // 2
            status_x = (window_width - status_surface.get_width()) // 2
            status_y = play_y - status_surface.get_height() - 20

            surface.blit(status_surface, (status_x, status_y))
            surface.blit(play_surface, (play_x, play_y))

            screen.blit(surface, (window_x, window_y))

            animation_end_time = config.ASCII_DISAPPEAR_TIME + total_logs * config.LOGS_INTERVAL + 0.25
            if current_time > animation_end_time:
                return False

            return True

        # Показываем LOGS_VISIBLE_COUNT строк (только если ещё есть логи)
        if current_log_index < total_logs:
            for j in range(config.LOGS_VISIBLE_COUNT):
                log_index = current_log_index - j
                if log_index >= 0 and log_index < total_logs:
                    text_surface = font.render(START_LOGS[log_index], True, config.COLOR_DARK)
                    surface.blit(text_surface, (20, y_offset - j * line_height))

    screen.blit(surface, (window_x, window_y))

    # Проверяем, что анимация полностью завершена (включая PRESS PLAY)
    animation_end_time = config.ASCII_DISAPPEAR_TIME + total_logs * config.LOGS_INTERVAL + 0.25
    if current_time > animation_end_time:
        return False

    return True
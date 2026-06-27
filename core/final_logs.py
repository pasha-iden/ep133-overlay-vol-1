import pygame
from data import config
from data.text_script import FINAL_LOGS


def render_final_logs(screen, current_time, window_x, window_y, window_width, window_height, font_size=None,
                      offset_x=None, offset_y=None):
    """
    Рендерит финальные логи построчно с интервалом LINE_INTERVAL
    Появляются построчно, исчезают построчно
    Центрирование по вертикали от ПОЛНОГО блока (всех строк), а не от видимых
    """
    if current_time < config.FINAL_LOGS_APPEAR_TIME:
        return False

    if font_size is None:
        font_size = config.FONT_SIZE_SEQUENCE

    if offset_x is None:
        offset_x = 20
    if offset_y is None:
        offset_y = 20

    font = pygame.font.SysFont(config.FONT_NAME, font_size)
    line_height = font_size + 2

    # Создаём поверхность
    surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    surface.fill(config.BACKGROUND_COLOR)

    total_logs = len(FINAL_LOGS)

    # ===== ПОЯВЛЕНИЕ (используем LINE_INTERVAL) =====
    elapsed = current_time - config.FINAL_LOGS_APPEAR_TIME
    appear_count = min(int(elapsed // config.LINE_INTERVAL) + 1, total_logs)

    # ===== ИСЧЕЗНОВЕНИЕ (используем LINE_INTERVAL) =====
    disappear_elapsed = current_time - config.FINAL_LOGS_DISAPPEAR_TIME
    disappear_count = 0
    if disappear_elapsed > 0:
        disappear_count = min(int(disappear_elapsed // config.LINE_INTERVAL) + 1, total_logs)

    # Определяем, какие строки видимы
    visible_indices = []
    for i in range(total_logs):
        if i < appear_count and i < total_logs - disappear_count:
            visible_indices.append(i)

    # ===== ВЫЧИСЛЯЕМ РАЗМЕР ПОЛНОГО БЛОКА (всех строк) =====
    full_block_height = total_logs * line_height
    full_block_width = 0
    for i in range(total_logs):
        text_surface = font.render(FINAL_LOGS[i], True, config.COLOR_DARK)
        full_block_width = max(full_block_width, text_surface.get_width())

    # Центрируем ПОЛНЫЙ блок
    x_center = (window_width - full_block_width) // 2
    y_center = (window_height - full_block_height) // 2

    # Рисуем только видимые строки, но с фиксированными позициями
    for i in visible_indices:
        text_surface = font.render(FINAL_LOGS[i], True, config.COLOR_DARK)
        x_pos = x_center
        y_pos = y_center + i * line_height
        surface.blit(text_surface, (x_pos, y_pos))

    screen.blit(surface, (window_x, window_y))
    return True
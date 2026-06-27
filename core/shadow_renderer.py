import pygame

def create_shadow(width, height, radius, blur=10, spread=0, alpha=100):
    """
    Создаёт тень как в CSS box-shadow
    width, height - размеры элемента
    radius - border-radius скругление
    blur - blur-radius (размытие)
    spread - spread-radius (растяжение)
    alpha - прозрачность тени
    """
    # Размер тени с учётом spread и blur
    shadow_size = blur + spread
    shadow_w = width + shadow_size * 2
    shadow_h = height + shadow_size * 2

    shadow_surface = pygame.Surface((shadow_w, shadow_h), pygame.SRCALPHA)

    # Рисуем несколько слоёв для имитации Gaussian blur
    for i in range(blur, 0, -1):
        # Прозрачность уменьшается от центра к краям
        # как при Gaussian blur
        layer_alpha = int(alpha * (i / blur))

        layer = pygame.Surface((width + (blur - i) * 2, height + (blur - i) * 2), pygame.SRCALPHA)
        layer_rect = layer.get_rect()

        # Рисуем слой тени
        pygame.draw.rect(layer, (0, 0, 0, layer_alpha), layer_rect, border_radius=radius + (blur - i))

        # Накладываем слой
        shadow_surface.blit(layer, (i, i))

    return shadow_surface
"""Игра «Изгиб Питона» (Змейка на ООП).

Финальный проект спринта «ООП и другие полезные вещи» (Яндекс Практикум).
"""

from typing import Tuple, Optional

# Константы игрового поля
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета (RGB)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Скорость обновления кадров
SPEED = 20


class GameObject:
    """Базовый класс для всех игровых объектов на поле."""

    def __init__(
        self,
        position: Optional[Tuple[int, int]] = None,
        body_color: Optional[Tuple[int, int, int]] = None
    ) -> None:
        """Инициализирует позицию и цвет игрового объекта."""
        if position is None:
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Абстрактный метод отрисовки объекта. Переопределяется в подклассах."""
        pass

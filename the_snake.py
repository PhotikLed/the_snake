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


class Apple(GameObject):
    """Класс яблока на игровом поле."""

    def __init__(self, occupied_positions: Optional[list] = None) -> None:
        """Инициализирует яблоко красным цветом и задает случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions: Optional[list] = None) -> None:
        """Устанавливает случайное положение яблока вне тела змейки."""
        import random

        occupied = set(occupied_positions) if occupied_positions else set()
        while True:
            new_pos = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_pos not in occupied:
                self.position = new_pos
                break

    def draw(self, surface) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        import pygame

        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, управляющий движением, ростом и коллизиями."""

    def __init__(self) -> None:
        """Инициализирует змейку в центре экрана с движением вправо."""
        super().__init__(
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=SNAKE_COLOR
        )
        self.reset()

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self) -> None:
        """Обновляет направление движения на следующее заданное игроком."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки с циклическим переходом сквозь границы экрана."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        # Телепортация через границы поля
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface) -> None:
        """Отрисовывает тело змейки и стирает след от хвоста."""
        import pygame

        # Отрисовка головы и тела
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Затирание хвостового сегмента
        if self.last:
            last_rect = pygame.Rect(self.last[0], self.last[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

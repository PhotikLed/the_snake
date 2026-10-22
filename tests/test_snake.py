"""Модульные тесты логики игры «Змейка»."""

import os
import pygame
import pytest

from the_snake import (
    GameObject,
    Apple,
    Snake,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GRID_SIZE,
    UP,
    DOWN,
    RIGHT,
    APPLE_COLOR,
    SNAKE_COLOR,
)

os.environ['SDL_VIDEODRIVER'] = 'dummy'


@pytest.fixture(scope='session', autouse=True)
def init_pygame():
    """Инициализация pygame для тестирования методов отрисовки."""
    pygame.init()
    yield
    pygame.quit()


def test_game_object():
    """Проверка базового класса GameObject."""
    obj = GameObject((100, 100), (255, 255, 255))
    assert obj.position == (100, 100)
    assert obj.body_color == (255, 255, 255)

    default_obj = GameObject()
    assert default_obj.position == (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Метод draw в базовом классе не должен выбрасывать исключений
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    obj.draw(surface)


def test_apple_randomize_position():
    """Проверка генерации позиции яблока вне тела змейки."""
    apple = Apple()
    assert apple.body_color == APPLE_COLOR

    # Проверка выравнивания по сетке
    x, y = apple.position
    assert x % GRID_SIZE == 0
    assert y % GRID_SIZE == 0
    assert 0 <= x < SCREEN_WIDTH
    assert 0 <= y < SCREEN_HEIGHT

    # Проверка исключения занятых клеток
    occupied = [
        (cell_x, cell_y)
        for cell_x in range(0, SCREEN_WIDTH, GRID_SIZE)
        for cell_y in range(0, SCREEN_HEIGHT, GRID_SIZE)
    ]
    # Оставим только одну свободную клетку (0, 0)
    occupied.remove((0, 0))

    apple.randomize_position(occupied)
    assert apple.position == (0, 0)


def test_snake_initial_state():
    """Проверка стартового состояния змейки."""
    snake = Snake()
    assert snake.length == 1
    assert snake.positions == [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    assert snake.direction == RIGHT
    assert snake.body_color == SNAKE_COLOR
    assert snake.get_head_position() == (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


def test_snake_move():
    """Проверка перемещения змейки по полю."""
    snake = Snake()
    start_x, start_y = snake.get_head_position()

    # Движение вправо по умолчанию
    snake.move()
    assert snake.get_head_position() == (start_x + GRID_SIZE, start_y)
    assert len(snake.positions) == 1

    # Поворот вниз
    snake.next_direction = DOWN
    snake.update_direction()
    snake.move()
    assert snake.get_head_position() == (start_x + GRID_SIZE, start_y + GRID_SIZE)


def test_snake_wraparound():
    """Проверка телепортации сквозь границы экрана."""
    snake = Snake()

    # Движемся сквозь правую границу
    snake.positions = [(SCREEN_WIDTH - GRID_SIZE, 100)]
    snake.direction = RIGHT
    snake.move()
    assert snake.get_head_position() == (0, 100)

    # Движемся сквозь верхнюю границу
    snake.positions = [(100, 0)]
    snake.direction = UP
    snake.move()
    assert snake.get_head_position() == (100, SCREEN_HEIGHT - GRID_SIZE)


def test_snake_growth_and_reset():
    """Проверка роста змейки и сброса при коллизии."""
    snake = Snake()
    snake.length = 3
    snake.positions = [(100, 100), (80, 100), (60, 100)]

    snake.move()
    assert len(snake.positions) == 3

    # Сброс
    snake.reset()
    assert snake.length == 1
    assert snake.positions == [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    assert snake.direction == RIGHT

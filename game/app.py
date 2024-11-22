from typing import List, Tuple

from game.constants import StatusEnum
from game.utils import get_ray_direction, random_coordinate


class CoordinateGenerator:
    """Класс для генерации случайных координат."""
    @staticmethod
    def generate(size: int) -> Tuple[int, int]:
        return random_coordinate(size), random_coordinate(size)


class GameGrid:
    """Класс для представления игрового поля."""
    def __init__(self, size: int, atoms_count: int):
        self.size = size
        self.atoms_count = atoms_count
        self.grid: List[List[int]] = [[0 for _ in range(size)] for _ in range(size)]

    def place_atoms(self, coordinate_generator: CoordinateGenerator) -> None:
        """Генерация атомов на игровом поле."""
        for _ in range(self.atoms_count):
            while True:
                x, y = coordinate_generator.generate(self.size)
                if self.grid[x][y] == 0:
                    self.grid[x][y] = 1
                    break

    def is_atom(self, x: int, y: int) -> bool:
        return self.grid[x][y] == 1

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size


class RayTracer:
    """Класс для обработки логики движения луча."""
    def __init__(self, grid: GameGrid):
        self.grid = grid

    def trace_ray(self, direction: Tuple[int, int], x: int, y: int) -> StatusEnum:
        dx, dy = direction

        while self.grid.is_within_bounds(x, y):
            if self.grid.is_atom(x, y):
                return StatusEnum.ABSORBED

            if self._is_reflected(x, y, dx, dy):
                dx, dy = -dx, -dy
                return StatusEnum.REFLECTED

            x += dx
            y += dy

        return StatusEnum.ESCAPED

    def _is_reflected(self, x: int, y: int, dx: int, dy: int) -> bool:
        """Проверяет, отражается ли луч."""
        next_x, next_y = x + dx, y + dy
        if self.grid.is_within_bounds(next_x, y) and self.grid.is_atom(next_x, y):
            return True
        if self.grid.is_within_bounds(x, next_y) and self.grid.is_atom(x, next_y):
            return True
        return False


class GameInterface:
    """Основной класс игры."""
    def __init__(self, grid_size: int = 9, atoms_count: int = 5):
        self.grid: GameGrid = GameGrid(grid_size, atoms_count)
        self.score: int = 0
        self.found_atoms: int = 0
        self.grid.place_atoms(CoordinateGenerator())
        self.ray_tracer: RayTracer = RayTracer(self.grid)

    def play(self, ray: int) -> str:
        try:
            direction, x, y = get_ray_direction(ray)
        except ValueError as e:
            return str(e)

        result = self.ray_tracer.trace_ray(direction, x, y)

        if result == StatusEnum.ABSORBED:
            self.score += 1

        return result.value

my_game = GameInterface()

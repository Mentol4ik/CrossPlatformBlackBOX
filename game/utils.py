import random


# Функция для создания случайной координаты
def random_coordinate(num: int) -> int:
    return random.randint(0, num - 1)


# Функция для получения направления луча в зависимости от выбранной грани
def get_ray_direction(ray: int) -> tuple[tuple[int, int], int, int]:
    if 1 <= ray <= 8:
        return (0, 1), ray, 0  # Левая сторона (X=0)
    elif 9 <= ray <= 16:
        return (1, 0), 9, ray - 8  # Нижняя сторона (Y=9)
    elif 17 <= ray <= 24:
        return (0, -1), 9 - (ray - 16), 9  # Правая сторона (X=9)
    elif 25 <= ray <= 32:
        return (-1, 0), 0, 33 - ray  # Верхняя сторона (Y=0)
    else:
        raise ValueError(f"Invalid ray: {ray}")

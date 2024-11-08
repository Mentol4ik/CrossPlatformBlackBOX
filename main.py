import random


# Функция для создания случайной координаты
def random_coordinate():
    return random.randint(1, 8)


# Функция для получения направления луча в зависимости от выбранной грани
def get_ray_direction(ray):
    if 1 <= ray <= 8:
        return (0, 1), ray, 0  # Левая сторона (X=0)
    elif 9 <= ray <= 16:
        return (1, 0), 9, ray - 8  # Нижняя сторона (Y=9)
    elif 17 <= ray <= 24:
        return (0, -1), 9 - (ray - 16), 9  # Правая сторона (X=9)
    elif 25 <= ray <= 32:
        return (-1, 0), 0, 33 - ray  # Верхняя сторона (Y=0)


# Основной цикл игры
def play_blackbox():
    print("Welcome to BLACKBOX!")
    print("Place your atoms and fire rays to find their positions.")

    # Генерация сетки и размещение атомов
    grid_size = 9
    atoms_count = int(input("Enter the number of atoms: "))
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Размещение атомов
    for _ in range(atoms_count):
        while True:
            x, y = random_coordinate(), random_coordinate()
            if grid[x][y] == 0:
                grid[x][y] = 1
                break

    score = 0
    found_atoms = 0

    # Основной игровой цикл
    while True:
        # Получаем от пользователя луч для запуска
        try:
            ray = int(input("Enter the ray number (1-32) or 0 to guess atoms: "))
        except ValueError:
            continue

        if ray == 0:
            break  # Переходим к угадыванию атомов

        # Получаем направление луча и его начальные координаты
        direction, x, y = get_ray_direction(ray)
        dx, dy = direction

        # Прогоняем луч по сетке
        while 0 <= x < grid_size and 0 <= y < grid_size:
            if grid[x][y] == 1:
                print("ABSORBED!")
                score += 1
                break
            # Проверяем соседние клетки для отражения
            if (
                0 <= x + dx < grid_size
                and 0 <= y + dy < grid_size
                and (grid[x + dx][y] == 1 or grid[x][y + dy] == 1)
            ):
                dx, dy = -dx, -dy  # Меняем направление луча
                print("REFLECTED!")
            else:
                x += dx
                y += dy

        if not (0 <= x < grid_size and 0 <= y < grid_size):
            print("ESCAPED!")

    # Угадывание местоположения атомов
    print("Now tell me, where do you think the atoms are? (in row, column format)")
    for i in range(1, atoms_count + 1):
        guess_x = int(input(f"Guess the row for atom #{i}: "))
        guess_y = int(input(f"Guess the column for atom #{i}: "))

        if grid[guess_x][guess_y] == 1:
            print("Correct!")
            found_atoms += 1
        else:
            print("Incorrect!")
            score += 5  # За неправильное предположение добавляем штраф

    # Вывод итогов
    print(f"You found {found_atoms} out of {atoms_count} atoms.")
    print(f"Your final score is {score} points.")
    play_again = input("Care to try again? (Y/N): ").upper()

    if play_again == "Y":
        play_blackbox()


# Запускаем игру
if __name__ == "__main__":
    play_blackbox()

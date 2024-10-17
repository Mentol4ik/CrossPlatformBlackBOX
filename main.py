import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WINDOW_SIZE = 500
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // (GRID_SIZE + 2)  # 2 дополнительных клетки для рамок

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Инициализация окна
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Blackbox Game")

# Шрифт для текста
font = pygame.font.Font(None, 36)


# Создание игрового поля
def create_board():
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return board


# Размещение атомов
def place_atoms(board, num_atoms):
    placed_atoms = 0
    while placed_atoms < num_atoms:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if board[x][y] == 0:
            board[x][y] = 1
            placed_atoms += 2
    return board


# Рисование сетки
def draw_grid():
    for i in range(1, GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, CELL_SIZE), (i * CELL_SIZE, WINDOW_SIZE - CELL_SIZE), 2)
        pygame.draw.line(screen, BLACK, (CELL_SIZE, i * CELL_SIZE), (WINDOW_SIZE - CELL_SIZE, i * CELL_SIZE), 2)


# Рисование атомов (для отладки)
def draw_atoms(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 1:
                pygame.draw.circle(screen, RED,
                                   ((i + 1) * CELL_SIZE + CELL_SIZE // 2, (j + 1) * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 3)


# Рисование интерфейса
def draw_interface(result_message, guessed_atoms_message):
    screen.fill(WHITE)
    draw_grid()

    # Отображение результата на экране
    text = font.render(result_message, True, BLUE)
    screen.blit(text, (WINDOW_SIZE // 2 - text.get_width() // 2, 10))

    # Отображение сообщения с угаданными атомами
    guess_text = font.render(guessed_atoms_message, True, RED)
    screen.blit(guess_text, (WINDOW_SIZE // 2 - guess_text.get_width() // 2, 50))


# Проверка, куда попал луч
def shoot_ray(board, ray_position, direction):
    x, y = ray_position

    # Если попали в атом
    if board[x][y] == 1:
        return "ABSORBED"

    # Для упрощения логики: если это левая сторона, луч всегда "ESCAPED" (просто для демонстрации)
    if direction == "LEFT" or direction == "RIGHT":
        return "ESCAPED"
    elif direction == "TOP" or direction == "BOTTOM":
        return "ESCAPED"

    # Добавьте логику для реальной симуляции отражения и поглощения


# Определение направления луча
def get_ray_direction(mouse_pos):
    x, y = mouse_pos
    if x < CELL_SIZE:  # Левая сторона
        return (0, y // CELL_SIZE - 1), "LEFT"
    elif x > WINDOW_SIZE - CELL_SIZE:  # Правая сторона
        return (GRID_SIZE - 1, y // CELL_SIZE - 1), "RIGHT"
    elif y < CELL_SIZE:  # Верхняя сторона
        return (x // CELL_SIZE - 1, 0), "TOP"
    elif y > WINDOW_SIZE - CELL_SIZE:  # Нижняя сторона
        return (x // CELL_SIZE - 1, GRID_SIZE - 1), "BOTTOM"
    else:
        return None, None


# Проверка догадки игрока о местоположении атомов
def check_guess(board, guess):
    x, y = guess
    if board[x][y] == 1:
        return True
    else:
        return False


# Главный цикл игры
def main():
    board = create_board()
    board = place_atoms(board, 5)

    running = True
    result_message = ""
    guessed_atoms_message = ""
    guessed_atoms = []  # Хранение догадок игрока

    while running:
        # Перерисовываем интерфейс после каждого цикла
        draw_interface(result_message, guessed_atoms_message)

        # Рисуем атомы (для проверки)
        # draw_atoms(board)  # Отключите это для реальной игры

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                ray_position, direction = get_ray_direction(mouse_pos)

                if ray_position and direction:
                    # Стреляем лучом в указанное направление
                    result_message = shoot_ray(board, ray_position, direction)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Ввод координат атома (нажатием Enter)
                    # Например, игрок вводит предполагаемую координату (3, 4)
                    guess_x = int(input("Введите координату X атома (0-8): "))
                    guess_y = int(input("Введите координату Y атома (0-8): "))

                    guess = (guess_x, guess_y)

                    if guess not in guessed_atoms:  # Чтобы не угадывать ту же клетку повторно
                        guessed_atoms.append(guess)
                        if check_guess(board, guess):
                            guessed_atoms_message = f"ATOM FOUND at ({guess_x}, {guess_y})!"
                        else:
                            guessed_atoms_message = f"No atom at ({guess_x}, {guess_y})"

        # Обновляем экран
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
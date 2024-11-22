from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Убедитесь, что используете безопасный ключ

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

# Главная страница игры
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'grid' not in session:
            session['grid'] = [[0 for _ in range(9)] for _ in range(9)]
            session['score'] = 0
            session['found_atoms'] = 0
            session['atoms_count'] = int(request.form['atoms_count'])
            # Размещение атомов
            for _ in range(session['atoms_count']):
                while True:
                    x, y = random_coordinate(), random_coordinate()
                    if session['grid'][x][y] == 0:
                        session['grid'][x][y] = 1
                        break
        return redirect(url_for("play"))
    return render_template("index.html")

# Игровой процесс
@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "POST":
        ray = int(request.form['ray'])
        grid = session['grid']
        score = session['score']
        found_atoms = session['found_atoms']

        if ray == 0:
            # Угадывание атомов
            return redirect(url_for("guess_atoms"))

        # Получаем направление луча и его начальные координаты
        direction, x, y = get_ray_direction(ray)
        dx, dy = direction

        # Прогоняем луч по сетке
        while 0 <= x < 9 and 0 <= y < 9:
            if grid[x][y] == 1:
                score += 1
                session['score'] = score
                return render_template("play.html", grid=grid, score=score, message="ABSORBED!")
            if 0 <= x + dx < 9 and 0 <= y + dy < 9 and (grid[x + dx][y] == 1 or grid[x][y + dy] == 1):
                dx, dy = -dx, -dy  # Меняем направление луча
                return render_template("play.html", grid=grid, score=score, message="REFLECTED!")
            else:
                x += dx
                y += dy

        return render_template("play.html", grid=grid, score=score, message="ESCAPED!")

    return render_template("play.html", grid=session['grid'], score=session['score'])

# Угадывание местоположения атомов
@app.route("/guess_atoms", methods=["GET", "POST"])
def guess_atoms():
    if request.method == "POST":
        grid = session['grid']
        atoms_count = session['atoms_count']
        found_atoms = session['found_atoms']
        score = session['score']

        for i in range(1, atoms_count + 1):
            guess_x = int(request.form[f"guess_x_{i}"])
            guess_y = int(request.form[f"guess_y_{i}"])

            if grid[guess_x][guess_y] == 1:
                found_atoms += 1
            else:
                score += 5

        session['found_atoms'] = found_atoms
        session['score'] = score
        return render_template("result.html", found_atoms=found_atoms, score=score)

    return render_template("guess_atoms.html", atoms_count=session['atoms_count'])

# Страница результата
@app.route("/result")
def result():
    return render_template("result.html", found_atoms=session['found_atoms'], score=session['score'])

if __name__ == "__main__":
    app.run(debug=True)
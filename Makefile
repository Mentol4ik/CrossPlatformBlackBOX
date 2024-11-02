# Makefile для игры BLACKBOX

# Определяем интерпретатор Python
PYTHON ?= python3

# Определяем файл исходного кода
SRC = main.py

# Определяем имя виртуального окружения
VENV = venv

# Цель по умолчанию
all: run

# Создаем виртуальное окружение и устанавливаем зависимости
venv:
	$(PYTHON) -m venv $(VENV)
	@echo "Устанавливаем зависимости..."
	$(VENV)/bin/$(PYTHON) -m pip install --upgrade pip

run: venv
	@echo "Запуск BLACKBOX..."
	$(VENV)/bin/$(PYTHON) $(SRC)

# Очистка виртуального окружения
clean:
	rm -rf $(VENV)

.PHONY: all venv run clean
# 🧪 Примеры использования Pytest

Полный набор примеров команд и описание всех возможностей pytest, используемых в этом проекте.

## 📦 Установка

```bash
# Создать виртуальное окружение
python3 -m venv venv

# Активировать окружение
source venv/bin/activate          # На Linux/Mac
# или
venv\Scripts\activate             # На Windows

# Установить pytest
pip install pytest
```

## 🏃 Запуск приложения

```bash
# Полный демо-скрипт с примерами
python3 -m src.todo_app
```

**Вывод:**
```
==================================================
📋 TODO Application Demo
==================================================

1️⃣  Adding tasks with different priorities...
   ✅ Added: Prepare presentation for meeting (Priority: 3)
   ...

✨ Demo completed!
==================================================
```

## 🧪 Запуск тестов

### Основные команды

```bash
# Запустить все тесты
pytest test/

# Запустить с подробным выводом (verbose)
pytest test/ -v

# Запустить с очень подробным выводом
pytest test/ -vv

# Краткий формат вывода
pytest test/ -q

# Запустить конкретный файл
pytest test/test_todo_app.py

# Запустить конкретный класс тестов
pytest test/test_todo_app.py::TestBasicAssertions

# Запустить конкретный тест
pytest test/test_todo_app.py::TestBasicAssertions::test_add_task_basic
```

### Результат базового запуска

```bash
$ pytest test/ -v

test/test_todo_app.py::TestBasicAssertions::test_add_task_basic PASSED
test/test_todo_app.py::TestBasicAssertions::test_task_equality PASSED
...
===== 41 passed in 0.22s =====
```

## 🎯 Использование маркеров

### Запуск только критических тестов

```bash
pytest test/ -m "critical" -v
```

**Результат:**
```
test/test_todo_app.py::TestBasicAssertions::test_add_task_basic PASSED
test/test_todo_app.py::TestWithFixtures::test_complete_task PASSED
test/test_todo_app.py::TestMarkers::test_persistence_across_instances PASSED

===== 3 passed, 38 deselected in 0.04s =====
```

### Запуск всех тестов КРОМЕ медленных

```bash
pytest test/ -m "not slow" -v
```

### Запуск критических ИЛИ интеграционных тестов

```bash
pytest test/ -m "critical or integration" -v
```

### Запуск интеграционных, но не медленных тестов

```bash
pytest test/ -m "integration and not slow" -v
```

### Список доступных маркеров

```bash
pytest --markers
```

**Вывод:**
```
@pytest.mark.slow: marks tests as slow
@pytest.mark.critical: marks tests as critical functionality
@pytest.mark.integration: marks tests as integration tests
```

## 🔍 Поиск и фильтрация тестов

### Запуск тестов по названию (keyword)

```bash
# Все тесты с "add" в названии
pytest test/ -k "add" -v

# Все тесты с "task" в названии
pytest test/ -k "task" -v

# Все тесты начинающиеся на "test_add"
pytest test/ -k "test_add" -v

# Исключить определённые тесты
pytest test/ -k "not slow" -v
```

### Сбор информации о тестах (без запуска)

```bash
# Показать все тесты, которые будут запущены
pytest test/ --collect-only

# Краткий формат
pytest test/ -co -q

# Только количество
pytest test/ -co -q | wc -l

# С указанием маркеров
pytest test/ --collect-only -q | grep "integration"
```

## 📊 Форматирование вывода

### Различные форматы traceback

```bash
# По умолчанию (долгий)
pytest test/ --tb=long

# Краткий формат
pytest test/ --tb=short

# Без traceback
pytest test/ --tb=no

# Строка traceback
pytest test/ --tb=line

# Встроенный (inline) формат
pytest test/ --tb=native
```

### Пример с ошибкой (--tb=short)

```bash
$ pytest test/test_todo_app.py::TestExceptions::test_add_empty_task -v --tb=short

PASSED test/test_todo_app.py::TestExceptions::test_add_empty_task
```

## ⏸️ Управление выполнением

```bash
# Остановиться на первой ошибке
pytest test/ -x

# Остановиться после N ошибок
pytest test/ --maxfail=2

# Запустить последние N неудачных тестов
pytest test/ --lf

# Запустить только неудачные тесты
pytest test/ --failed-first

# Остановиться, если файл был изменён
pytest test/ -x --tb=short
```

## 🖨️ Вывод print() и логирование

```bash
# Показать весь вывод (print)
pytest test/ -s

# Показать вывод только для неудачных тестов
pytest test/ -vv -s

# Установить уровень логирования
pytest test/ -s --log-cli-level=DEBUG
```

## 📈 Дополнительные опции

```bash
# Очень подробный вывод с информацией о fixtures
pytest test/ -v --setup-show

# Тихий режим (только результаты)
pytest test/ -q

# Очень тихий режим
pytest test/ -qq

# Показать локальные переменные при ошибке
pytest test/ -l

# Показать самые медленные тесты
pytest test/ --durations=5

# Случайный порядок выполнения
pytest test/ --random-order
# (требует: pip install pytest-randomly)
```

## 🎓 Примеры из проекта

### 1. Базовые Assertions

```python
# test/test_todo_app.py
def test_add_task_basic(todo_app):
    task = todo_app.add_task("Learn pytest")
    
    assert task.title == "Learn pytest"          # Проверка значения
    assert task.done is False                    # Проверка булева
    assert len(todo_app.get_all_tasks()) == 1    # Проверка длины
```

**Команда:**
```bash
pytest test/test_todo_app.py::TestBasicAssertions::test_add_task_basic -v
```

### 2. Тестирование исключений

```python
def test_add_empty_task(todo_app):
    with pytest.raises(ValueError, match="cannot be empty"):
        todo_app.add_task("")
```

**Команда:**
```bash
pytest test/test_todo_app.py::TestExceptions -v
```

**Результат:**
```
test_add_empty_task PASSED
test_add_whitespace_only_task PASSED
test_add_task_too_long PASSED
test_invalid_priority PASSED
...
===== 8 passed =====
```

### 3. Fixtures

```python
# test/conftest.py
@pytest.fixture
def todo_app(storage_file: Path) -> TodoApp:
    return TodoApp(storage_file)

@pytest.fixture
def app_with_tasks(todo_app: TodoApp) -> TodoApp:
    todo_app.add_task("Task 1", priority=1)
    todo_app.add_task("Task 2", priority=2)
    return todo_app
```

**Команда с информацией о fixtures:**
```bash
pytest test/test_todo_app.py::TestWithFixtures -v --setup-show
```

### 4. Параметризация

```python
@pytest.mark.parametrize("title,priority,expected_priority", [
    ("Low priority task", 1, 1),
    ("Medium priority task", 2, 2),
    ("High priority task", 3, 3),
])
def test_add_task_with_different_priorities(
    todo_app, title, priority, expected_priority
):
    task = todo_app.add_task(title, priority=priority)
    assert task.priority == expected_priority
```

**Команда:**
```bash
pytest test/test_todo_app.py::TestParametrization -v
```

**Результат:**
```
test_add_task_with_different_priorities[Low priority task-1-1] PASSED
test_add_task_with_different_priorities[Medium priority task-2-2] PASSED
test_add_task_with_different_priorities[High priority task-3-3] PASSED
```

### 5. Маркеры

```python
@pytest.mark.critical
def test_persistence_across_instances(todo_app):
    todo_app.add_task("Persistent task")
    new_app = TodoApp(todo_app.storage)
    assert new_app.active_tasks_count() == 1

@pytest.mark.slow
def test_many_tasks(todo_app):
    for i in range(100):
        todo_app.add_task(f"Task {i}")
    assert todo_app.active_tasks_count() == 100

@pytest.mark.integration
def test_complete_workflow(todo_app):
    # полный workflow теста
    ...
```

**Команды:**
```bash
# Только критические
pytest test/ -m "critical" -v

# Только интеграционные
pytest test/ -m "integration" -v

# Исключить медленные
pytest test/ -m "not slow" -q

# Критические И интеграционные
pytest test/ -m "critical and integration" -v
```

## 🔧 Полезные комбинации

### Быстрая проверка (без медленных тестов)

```bash
pytest test/ -m "not slow" -q
```

### Полный запуск с отчётом о времени

```bash
pytest test/ -v --durations=10
```

### Запуск критических тестов с подробностью

```bash
pytest test/ -m "critical" -vv --tb=short
```

### Развитие: запуск при изменении файлов

```bash
pip install pytest-watch
ptw test/ -- -m "not slow"
```

### Интеграционные тесты с логированием

```bash
pytest test/ -m "integration" -v -s --log-cli-level=INFO
```

## 📊 Статистика

### Получить информацию о покрытии

```bash
pip install pytest-cov
pytest test/ --cov=src --cov-report=html
```

### Распределение тестов по типам

```bash
$ pytest test/ -m "critical" -co -q | wc -l
# 3 критических теста

$ pytest test/ -m "slow" -co -q | wc -l
# 1 медленный тест

$ pytest test/ -m "integration" -co -q | wc -l
# 3 интеграционных теста
```

## 🎯 Лучшие практики

### 1. Использовать маркеры для организации

```bash
# Хорошо: организовано по типам
pytest test/ -m "critical" -x

# Плохо: запускать всё подряд
pytest test/
```

### 2. Использовать -x для быстрой отладки

```bash
pytest test/ -x --tb=short -s
```

### 3. Использовать -k для быстрого поиска

```bash
pytest test/ -k "test_add" -v
```

### 4. Использовать --collect-only для проверки

```bash
pytest test/ --collect-only -q | grep "test_"
```

## 🚀 Продвинутые возможности

### Пользовательские hooks (в conftest.py)

```python
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "critical: marks tests as critical"
    )

@pytest.fixture(scope="session")
def session_info():
    return {"test_suite": "TODO App"}
```

### Условное пропускание тестов

```python
@pytest.mark.skipif(
    sys.version_info < (3, 9),
    reason="requires python 3.9+"
)
def test_requires_python39(todo_app):
    pass
```

---

**Документация:** https://docs.pytest.org/  
**Этот проект:** Обучающий пример использования pytest

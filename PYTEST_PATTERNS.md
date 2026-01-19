# 📚 Дополнительные примеры и паттерны тестирования

Этот файл содержит примеры различных паттернов и подходов тестирования, которые вы можете использовать и адаптировать для своих проектов.

## 📖 Содержание

1. [Базовые паттерны](#базовые-паттерны)
2. [Продвинутые техники](#продвинутые-техники)
3. [Организация тестов](#организация-тестов)
4. [Обработка ошибок](#обработка-ошибок)
5. [Лучшие практики](#лучшие-практики)

## 🎯 Базовые паттерны

### Паттерн Arrange-Act-Assert (AAA)

```python
def test_complete_task_aaa_pattern(todo_app):
    # ARRANGE - подготовка данных
    todo_app.add_task("Test task")
    
    # ACT - выполнение действия
    task = todo_app.complete_task("Test task")
    
    # ASSERT - проверка результата
    assert task.done is True
    assert task.completed_at is not None
    assert todo_app.active_tasks_count() == 0
```

**Преимущества:**
- Ясная структура теста
- Легко читать и понимать
- Легко поддерживать

### Использование Multiple Assertions

```python
def test_multiple_assertions(todo_app):
    """Проверка нескольких связанных условий."""
    task = todo_app.add_task("Complex task", priority=3)
    
    # Все эти проверки логически связаны
    assert task.title == "Complex task"
    assert task.priority == 3
    assert task.done is False
    assert task.created_at is not None
```

### Проверка коллекций

```python
def test_collection_assertions(app_with_tasks):
    """Различные способы проверки коллекций."""
    tasks = app_with_tasks.get_all_tasks()
    
    # Длина
    assert len(tasks) == 3
    
    # Наличие элемента
    titles = [t.title for t in tasks]
    assert "Task 1" in titles
    
    # Все элементы удовлетворяют условию
    assert all(t.created_at for t in tasks)
    
    # Хотя бы один элемент удовлетворяет условию
    assert any(t.priority == 3 for t in tasks)
```

## 🚀 Продвинутые техники

### Контекстные менеджеры для исключений

```python
def test_exception_message_details(todo_app):
    """Проверка деталей исключения."""
    with pytest.raises(TaskNotFoundError) as exc_info:
        todo_app.complete_task("Nonexistent")
    
    # Доступ к исключению
    assert "Nonexistent" in str(exc_info.value)
    assert exc_info.type is TaskNotFoundError
```

### Параметризированные тесты с IDs

```python
@pytest.mark.parametrize(
    "title,priority",
    [
        ("Low", 1),
        ("Medium", 2),
        ("High", 3),
    ],
    ids=["low_priority", "medium_priority", "high_priority"]
)
def test_with_custom_ids(todo_app, title, priority):
    """Параметризация с пользовательскими ID."""
    task = todo_app.add_task(title, priority=priority)
    assert task.priority == priority
```

**Результат:**
```
test_with_custom_ids[low_priority] PASSED
test_with_custom_ids[medium_priority] PASSED
test_with_custom_ids[high_priority] PASSED
```

### Indirect параметризация

```python
@pytest.fixture
def app_with_n_tasks(todo_app, request):
    """Fixture, которая создаёт N задач."""
    for i in range(request.param):
        todo_app.add_task(f"Task {i+1}")
    return todo_app

@pytest.mark.parametrize("app_with_n_tasks", [1, 5, 10], indirect=True)
def test_with_different_task_counts(app_with_n_tasks):
    """Тестирование с разным количеством задач."""
    assert app_with_n_tasks.active_tasks_count() == app_with_n_tasks.__dict__
```

### Fixtures с параметрами

```python
@pytest.fixture(params=[1, 2, 3])
def priority_level(request):
    """Fixture с параметрами."""
    return request.param

def test_each_priority_level(todo_app, priority_level):
    """Автоматически запускается для каждого приоритета."""
    task = todo_app.add_task(f"Task {priority_level}", priority=priority_level)
    assert task.priority == priority_level
```

## 🗂️ Организация тестов

### Группировка с классами

```python
class TestAddTask:
    """Все тесты для добавления задач."""
    
    def test_add_simple_task(self, todo_app):
        task = todo_app.add_task("Simple")
        assert task.title == "Simple"
    
    def test_add_with_priority(self, todo_app):
        task = todo_app.add_task("Priority", priority=3)
        assert task.priority == 3


class TestCompleteTask:
    """Все тесты для завершения задач."""
    
    def test_complete_existing(self, todo_app):
        todo_app.add_task("Task")
        task = todo_app.complete_task("Task")
        assert task.done is True
    
    def test_complete_nonexistent(self, todo_app):
        with pytest.raises(TaskNotFoundError):
            todo_app.complete_task("Nonexistent")
```

### Вложенные классы

```python
class TestTodoApp:
    """Главный класс для тестирования TodoApp."""
    
    class TestAddition:
        """Тесты для добавления."""
        
        def test_add_task(self, todo_app):
            task = todo_app.add_task("Test")
            assert len(todo_app.get_all_tasks()) == 1
    
    class TestCompletion:
        """Тесты для завершения."""
        
        def test_complete_task(self, todo_app):
            todo_app.add_task("Test")
            task = todo_app.complete_task("Test")
            assert task.done is True
```

## ❌ Обработка ошибок

### Различные типы исключений

```python
def test_various_exceptions(todo_app):
    """Проверка различных типов исключений."""
    
    # ValueError - неверный ввод
    with pytest.raises(ValueError):
        todo_app.add_task("")
    
    # TaskNotFoundError - не найдено
    with pytest.raises(TaskNotFoundError):
        todo_app.complete_task("Nonexistent")
    
    # ValueError - для собственного исключения приложения
    with pytest.raises(ValueError):
        todo_app.add_task("Title", priority=5)
```

### Проверка сообщений об ошибках

```python
def test_error_messages(todo_app):
    """Проверка, что сообщения об ошибках информативны."""
    
    with pytest.raises(ValueError, match="cannot be empty"):
        todo_app.add_task("")
    
    with pytest.raises(ValueError, match="cannot exceed 200"):
        todo_app.add_task("a" * 201)
    
    with pytest.raises(ValueError, match="Priority must be"):
        todo_app.add_task("Task", priority=5)
```

### Использование match с регулярными выражениями

```python
def test_regex_matching(todo_app):
    """Использование регулярных выражений в match."""
    
    with pytest.raises(TaskNotFoundError, match=r".+ not found"):
        todo_app.complete_task("Missing")
    
    with pytest.raises(ValueError, match=r"Priority must be \d"):
        todo_app.add_task("Task", priority=99)
```

## 💡 Лучшие практики

### 1. Один тест = одна идея

✅ **Хорошо:**
```python
def test_add_task_returns_task_object(todo_app):
    """Проверка, что add_task возвращает объект Task."""
    task = todo_app.add_task("Test")
    assert isinstance(task, Task)

def test_add_task_increments_count(todo_app):
    """Проверка, что add_task увеличивает счётчик."""
    assert todo_app.active_tasks_count() == 0
    todo_app.add_task("Test")
    assert todo_app.active_tasks_count() == 1
```

❌ **Плохо:**
```python
def test_add_task(todo_app):
    # Слишком много проверок в одном тесте
    task = todo_app.add_task("Test")
    assert isinstance(task, Task)
    assert todo_app.active_tasks_count() == 1
    assert task.title == "Test"
```

### 2. Описательные имена тестов

✅ **Хорошо:**
```python
def test_add_task_with_empty_string_raises_value_error(todo_app):
    with pytest.raises(ValueError):
        todo_app.add_task("")
```

❌ **Плохо:**
```python
def test_add(todo_app):
    with pytest.raises(ValueError):
        todo_app.add_task("")
```

### 3. Используйте docstrings

✅ **Хорошо:**
```python
def test_persistence_across_instances(todo_app):
    """
    Verify that tasks persist across different app instances.
    
    This is a critical functionality for a file-based storage system.
    """
    todo_app.add_task("Persistent task")
    new_app = TodoApp(todo_app.storage)
    assert new_app.active_tasks_count() == 1
```

### 4. Избегайте дублирования с fixtures

✅ **Хорошо:**
```python
@pytest.fixture
def app_with_sample_tasks(todo_app):
    """Create an app with pre-populated sample tasks."""
    todo_app.add_task("Task 1", priority=1)
    todo_app.add_task("Task 2", priority=2)
    return todo_app

def test_filter_by_priority_1(app_with_sample_tasks):
    assert len(app_with_sample_tasks.get_tasks_by_priority(1)) == 1

def test_filter_by_priority_2(app_with_sample_tasks):
    assert len(app_with_sample_tasks.get_tasks_by_priority(2)) == 1
```

### 5. Правильное использование маркеров

✅ **Хорошо:**
```python
@pytest.mark.critical
def test_core_functionality(todo_app):
    """This is essential functionality."""
    ...

@pytest.mark.slow
def test_performance_with_1000_tasks(todo_app):
    """This test takes time."""
    ...

@pytest.mark.integration
def test_full_workflow(todo_app):
    """This tests multiple components."""
    ...
```

### 6. Используйте assert с полезными сообщениями

✅ **Хорошо:**
```python
def test_task_counts(app_with_tasks):
    tasks = app_with_tasks.get_all_tasks()
    assert len(tasks) == 3, f"Expected 3 tasks, got {len(tasks)}"
    
    # Или используйте pytest assertions
    assert len(tasks) == 3
    # pytest сам покажет подробное сообщение
```

## 🔍 Debugging тестов

### Использование -s флага для вывода

```bash
pytest test/test_todo_app.py -s -v
```

### Добавление print() для отладки

```python
def test_with_debug_output(todo_app):
    task = todo_app.add_task("Test")
    print(f"Task created: {task}")
    print(f"Task done: {task.done}")
    assert task.title == "Test"
```

### Использование pdb для интерактивной отладки

```python
def test_with_debugger(todo_app):
    task = todo_app.add_task("Test")
    import pdb; pdb.set_trace()  # Остановка здесь
    assert task.title == "Test"
```

**Запуск:**
```bash
pytest test/test_todo_app.py --pdb
```

### Просмотр локальных переменных при ошибке

```bash
pytest test/ -l  # --showlocals
```

---

**Дополнительные материалы:**
- [Pytest документация](https://docs.pytest.org/)
- [Pytest best practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)

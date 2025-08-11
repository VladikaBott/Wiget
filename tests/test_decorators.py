import os

import pytest

from src.decorators import log


# Фикстура для очистки файлов перед тестами
@pytest.fixture
def clean_logs():
    yield
    if os.path.exists("test.log"):
        os.remove("test.log")


# Тест логирования в консоль (успешный случай)
def test_console_logging_success(capsys):
    @log()
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    captured = capsys.readouterr()
    assert "Calling add with args=(2, 3), kwargs={}" in captured.out
    assert "add returned 5" in captured.out


# Тест логирования в консоль (ошибка)
def test_console_logging_error(capsys):
    @log()
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    captured = capsys.readouterr()
    assert "Calling div with args=(1, 0), kwargs={}" in captured.out
    assert "div raised ZeroDivisionError" in captured.out


# Тест логирования в файл (успешный случай)
def test_file_logging_success(clean_logs):
    @log(filename="test.log")
    def multiply(a, b):
        return a * b

    assert multiply(3, 4) == 12

    with open("test.log") as f:
        content = f.read()
        assert "Calling multiply with args=(3, 4), kwargs={}" in content
        assert "multiply returned 12" in content


# Тест логирования в файл (ошибка)
def test_file_logging_error(clean_logs):
    @log(filename="test.log")
    def fail():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        fail()

    with open("test.log") as f:
        content = f.read()
        assert "Calling fail with args=(), kwargs={}" in content
        assert "fail raised ValueError: Test error" in content


def test_kwargs_handling(capsys):
    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    assert greet("Alice") == "Hello, Alice!"
    captured = capsys.readouterr()
    assert "Calling greet with args=('Alice',), kwargs={}" in captured.out
    assert "greet returned 'Hello, Alice!'" in captured.out

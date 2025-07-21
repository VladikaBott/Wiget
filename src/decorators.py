from functools import wraps
from datetime import datetime
def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - Calling {func.__name__} with args={args}, kwargs={kwargs}\n"

            if filename:
                with open(filename, 'a') as f:
                    f.write(log_entry)
            else:
                print(log_entry.strip())

            try:
                result = func(*args, **kwargs)
                # Добавляем repr() для сохранения кавычек в строковых результатах
                success_msg = f"{timestamp} - {func.__name__} returned {repr(result)}\n"

                if filename:
                    with open(filename, 'a') as f:
                        f.write(success_msg)
                else:
                    print(success_msg.strip())

                return result

            except Exception as e:
                error_msg = f"{timestamp} - {func.__name__} raised {type(e).__name__}: {str(e)}. Input: args={args}, kwargs={kwargs}\n"

                if filename:
                    with open(filename, 'a') as f:
                        f.write(error_msg)
                else:
                    print(error_msg.strip())
                raise

        return wrapper

    return decorator
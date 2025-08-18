import json
import random


def generator_users(first_names: list[str], last_names: list[str], cities:list[str]) -> dict:
    """Функция которая генерирует пользователей в json формате"""
    while True:
        user = {
            'first_name' : random.choice(first_names),
            'last_name' : random.choice(last_names),
            'age' : random.randint(18,56),
            'city': random.choice(cities)
        }
        yield user

if __name__ == '__main__':
    cities = ['Moscow', 'Piter', 'Kazan', 'Barnaul']
    last_names = ['Bott', 'Gan', 'For']
    first_names = ['Vova', 'Dima', 'Antonio']

    users = generator_users(first_names, last_names, cities)
    user_group = [next(users) for i in range(3)]
    user_group_2 = [next(users) for i in range(6)]
    print("1 Группа")
    print(json.dumps(user_group))
    print(type(user_group))
    print("2 Группа")
    print(json.dumps(user_group_2))
    print(type(user_group_2))
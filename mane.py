import random
import json


def generate_users(first_names, last_names, cities):
    """Генератор случайный пользователей

    Аргументы:
         first_names - список имен
         last_names - список фамилий
         cities - список городов

     Возвращает:
         Генератор, который выдает словари с данными пользователей:
         {
             "first_name": случайное имя,
             "last_name": случайная фамилия,
             "age": случайный возраст (18-65),
             "city": случайный город
         }
     """
    while True:
        yield {
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'age': random.randint(18, 65),
            'city': random.choice(cities)
        }
if __name__ == "__main__":
    first_names = ['Василий', 'rosa', 'genad']
    last_names = ['gandon', 'xuesos']
    cities = ['moscow', 'novosib']

    user_gen = generate_users(first_names, last_names, cities)
    user = [next(user_gen) for i in range(5)]
    print(json.dumps(user, indent=2, ensure_ascii=False))
# 1. Создайте функцию, которая запрашивает числовые данные от
# пользователя до тех пор, пока он не введёт целое или вещественное число.
# Обрабатывайте не числовые данные как исключения.

def get_numeric_input():
    while True:
        try:
            user_input = input("Введите числовое значение: ")
            numeric_value = float(user_input)
            return numeric_value
        except ValueError:
            print("Ошибка! Введите целое или вещественное число.")

numeric_input = get_numeric_input()
print("Вы ввели:", numeric_input)

# ------------------------------------------------
# 2. Создайте функцию аналог get для словаря.
# Помимо самого словаря функция принимает ключ и значение по умолчанию.
# При обращении к несуществующему ключу функция должна возвращать дефолтное значение.
# Реализуйте работу через обработку исключений.


def get_value_from_dict(dictionary, key, def_value=None):
    try:
        value = dictionary[key]
    except KeyError:
        value = def_value
    return value


my_dict = {"a": 1, "b": 2, "c": 3}

key_to_check = "b"
default_value = -1

result = get_value_from_dict(my_dict, key_to_check, default_value)
print(f"Значение для ключа '{key_to_check}': {result}")

key_to_check = "d"
result = get_value_from_dict(my_dict, key_to_check, default_value)
print(f"Значение для ключа '{key_to_check}': {result}")

# ------------------------------------------------------------------------
# 3. Создайте класс с базовым исключением и дочерние классы-исключения:
#     ○ ошибка уровня,
#     ○ ошибка доступа.


class CustomException(Exception):
    pass

class LevelError(CustomException):
    pass

class AccessError(CustomException):
    pass


try:
    raise LevelError("Произошла ошибка уровня!")
except LevelError as le:
    print("Поймано исключение уровня:", le)

try:
    raise AccessError("Произошла ошибка доступа!")
except AccessError as ae:
    print("Поймано исключение доступа:", ae)

# -------------------------------------------------------------------
# 4. Вспоминаем задачу из семинара 8 про сериализацию данных,
# где в бесконечном цикле запрашивали имя, личный
# идентификатор и уровень доступа (от 1 до 7) сохраняя информацию в JSON файл.
# Напишите класс пользователя, который хранит эти данные в свойствах экземпляра.
# Отдельно напишите функцию, которая считывает информацию
# из JSON файла и формирует множество пользователей.

import json


class User:
    def __init__(self, name, id, access_level):
        self.name = name
        self.id = id
        self.access_level = access_level

    def to_dict(self):
        return {"name": self.name, "id": self.id, "access_level": self.access_level}

    def __str__(self):
        return f"User(name={self.name}, id={self.id}, access_level={self.access_level})"


def save_to_json(users):
    user_data = [user.to_dict() for user in users]
    with open("users.json", "w") as file:
        json.dump(user_data, file, indent=4)


def read_from_json():
    users = []
    try:
        with open("users.json", "r") as file:
            user_data = json.load(file)
            for user_info in user_data:
                users.append(User(user_info["name"], user_info["id"], user_info["access_level"]))
    except FileNotFoundError:
        pass
    return users


users = []

while True:
    name = input("Введите имя пользователя (или 'exit' для завершения): ")
    if name == 'exit':
        break
    id = input("Введите личный идентификатор: ")
    access_level = int(input("Введите уровень доступа (от 1 до 7): "))
    users.append(User(name, id, access_level))

save_to_json(users)
print("Данные сохранены в users.json")

loaded_users = read_from_json()
print("Загруженные пользователи:")
for user in loaded_users:
    print(user)

# ---------------------------------------------------------------------
# Доработаем задачи 3 и 4. Создайте класс проекта, который имеет следующие методы:
# загрузка данных (функция из задания 4)
# вход в систему - требует указать имя и id пользователя. Для
# проверки наличия пользователя в множестве используйте
#  магический метод проверки на равенство пользователей.
#  Если такого пользователя нет, вызывайте исключение
#  доступа. А если пользователь есть, получите его уровень из
#  множества пользователей.
# добавление пользователя. Если уровень пользователя
# меньше, чем ваш уровень, вызывайте исключение уровня доступа.


import json


class User:
    def __init__(self, name, id, access_level):
        self.name = name
        self.id = id
        self.access_level = access_level

    def to_dict(self):
        return {"name": self.name, "id": self.id, "access_level": self.access_level}

    def __str__(self):
        return f"User(name={self.name}, id={self.id}, access_level={self.access_level})"

    def __eq__(self, other):
        return self.name == other.name and self.id == other.id


class Project:
    def __init__(self, owner_level):
        self.owner_level = owner_level
        self.users = set()

    def load_users_from_json(self):
        try:
            with open("users.json", "r") as file:
                user_data = json.load(file)
                for user_info in user_data:
                    user = User(user_info["name"], user_info["id"], user_info["access_level"])
                    self.users.add(user)
        except FileNotFoundError:
            pass

    def login(self, name, id):
        user = User(name, id, 0)
        if user in self.users:
            user = next(u for u in self.users if u == user)
            if user.access_level < self.owner_level:
                raise AccessError("У вас недостаточный уровень доступа.")
            return user.access_level
        else:
            raise AccessError("Пользователь не найден.")

    def add_user(self, user):
        if user.access_level < self.owner_level:
            raise LevelError("Уровень доступа ниже необходимого.")
        self.users.add(user)
        print(f"Пользователь {user.name} добавлен.")


class CustomException(Exception):
    pass


class LevelError(CustomException):
    pass


class AccessError(CustomException):
    pass


project = Project(owner_level=5)
project.load_users_from_json()

try:
    while True:
        name = input("Введите имя пользователя (или 'exit' для завершения): ")
        if name == 'exit':
            break
        id = input("Введите личный идентификатор: ")
        access_level = int(input("Введите уровень доступа (от 1 до 7): "))
        user = User(name, id, access_level)
        project.add_user(user)
except LevelError as le:
    print("Ошибка уровня:", le)
except AccessError as ae:
    print("Ошибка доступа:", ae)

# ---------------------------------------------------------------------------
# 6. Доработайте классы исключения так, чтобы они выдали подробную информацию об ошибках.
# Передавайте необходимые данные из основного кода проекта.


import json

class User:
    def __init__(self, name, id, access_level):
        self.name = name
        self.id = id
        self.access_level = access_level

    def to_dict(self):
        return {"name": self.name, "id": self.id, "access_level": self.access_level}

    def __str__(self):
        return f"User(name={self.name}, id={self.id}, access_level={self.access_level})"

    def __eq__(self, other):
        return self.name == other.name and self.id == other.id

class CustomException(Exception):
    pass

class LevelError(CustomException):
    def __init__(self, message="Ошибка уровня доступа"):
        super().__init__(message)

    def __str__(self):
        return f"Ошибка уровня доступа: {self.message}"

class AccessError(CustomException):
    def __init__(self, message="Ошибка доступа"):
        super().__init__(message)

    def __str__(self):
        return f"Ошибка доступа: {self.message}"

class Project:
    def __init__(self, owner_level):
        self.owner_level = owner_level
        self.users = set()

    def load_users_from_json(self):
        try:
            with open("users.json", "r") as file:
                user_data = json.load(file)
                for user_info in user_data:
                    user = User(user_info["name"], user_info["id"], user_info["access_level"])
                    self.users.add(user)
        except FileNotFoundError:
            pass

    def login(self, name, id):
        user = User(name, id, 0)
        if user in self.users:
            user = next(u for u in self.users if u == user)
            if user.access_level < self.owner_level:
                raise AccessError(f"Доступ к проекту запрещен. Ваш уровень доступа: {user.access_level}")
            return user.access_level
        else:
            raise AccessError(f"Пользователь {name} с ID {id} не найден.")

    def add_user(self, user):
        if user.access_level < self.owner_level:
            raise LevelError("Недостаточный уровень доступа для добавления пользователя.")
        self.users.add(user)
        print(f"Пользователь {user.name} добавлен.")

project = Project(owner_level=5)
project.load_users_from_json()

try:
    while True:
        name = input("Введите имя пользователя (или 'exit' для завершения): ")
        if name == 'exit':
            break
        id = input("Введите личный идентификатор: ")
        access_level = int(input("Введите уровень доступа (от 1 до 7): "))
        user = User(name, id, access_level)
        project.add_user(user)
except LevelError as le:
    print(le)
except AccessError as ae:
    print(ae)


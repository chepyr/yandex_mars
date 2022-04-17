from requests import get, post, delete

# Корректные запросы на получение
print(get('http://localhost:5000/api/v2/users').json())
print(get('http://localhost:5000/api/v2/users/4').json())
# Пользователь не существует
print(get('http://localhost:5000/api/v2/users/10000').json())
print(get('http://localhost:5000/api/v2/users/hdg').json())

# Корректный запрос на добавление нового пользователя
print(post('http://localhost:5000/api/v2/users',
           json={'id': 8,
                 'name': 'Имя',
                 'surname': 'Какая-то фамилия',
                 'age': 10,
                 'position': 'позиция',
                 'speciality': 'какая-то специальность',
                 'address': 'какой-то адресс',
                 'email': 'какая-то почта'}).json())
# Указаны не все обязательные поля
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Имя',
                 'surname': 'Какая-то фамилия'}).json())

# Корректный запрос на удаление
print(delete('http://localhost:5000/api/v2/users/8'))
# Пользователя с таким id t ceotcndetn
print(delete('http://localhost:5000/api/v2/users/800'))

#
# # некорректный: Пустой запрос, не переданы никакие параметры
# print(post('http://localhost:5000/api/v2/users').json())
#
# # некорректный: В запросе не хватает обызательного параметра 'work_size'
# print(post('http://localhost:5000/api/v2/users',
#            json={'id': 11,
#                  'job': 'Работа',
#                  'team_leader': 2}).json())
#
# # некорректный: Работа с таким 'id' уже существует
# print(post('http://localhost:5000/api/v2/users',
#            json={'id': 1,
#                  'job': 'Работа',
#                  'collaborators': '1, 5',
#                  'work_size': 92839,
#                  'is_finished': False,
#                  'team_leader': 2}).json())
#
# print(get('http://localhost:5000/api/v2/users').json())

from requests import get, post, put

# Корректный запрос
print(put('http://localhost:5000/api/jobs/1',
          json={
              'is_finished': False
          }).json())

# Работа с таким id уже существует
print(put('http://localhost:5000/api/jobs/1',
          json={
              'id': 2
          }).json())

# Пустой запрос
print(put('http://localhost:5000/api/jobs/1').json())

# Работа с таким id не существует
print(put('http://localhost:5000/api/jobs/30',
          json={
              'collaborators': '1, 2'
          }).json())

print(get('http://localhost:5000/api/jobs').json())

import requests

# response = requests.post('http://127.0.0.1:5000/user/',
#                          json={
#                              'username': 'Yuliya',
#                              'password': '!!!password',
#                              'email': 'my_email'
#                          })

# response = requests.get('http://127.0.0.1:5000/user/1')

# response = requests.delete('http://127.0.0.1:5000/post/1')

# response = requests.post('http://127.0.0.1:5000/post/',
#                          json = {
#                              'creator': 1,
#                              'post_header': 'Первый пост',
#                              'post_text': 'Начинаю писать что-то..'
#                          })

response = requests.patch('http://127.0.0.1:5000/post/1',
                         json = {
                             'header': 'Пробуем новое',
                             'text': 'Ля-ля_фа....'
                         })

print(response.status_code)
print(response.json())




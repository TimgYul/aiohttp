import requests

import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        response = await session.post('http://127.0.0.1:5000/posts/',
                                      json={
                                          'creator_id': 1,
                                          'post_header': ' мой',
                                          'post_text': ' текст',
                                          
                                      })
        response = await session.get('http://127.0.0.1:5000/posts/1')
        data = await response.json()
        print(data)
        
    async with aiohttp.ClientSession() as session:
        response = await session.post('http://127.0.0.1:5000/users/',
                                      json={
                                'username': 'Yuliya',
                                'password': '!!!password',
                                'email': 'my_email'      
                                      })
        data = await response.json()
        print(data)
        
asyncio.run(main())

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

# response = requests.patch('http://127.0.0.1:5000/post/1',
#                          json = {
#                              'header': 'Пробуем новое',
#                              'text': 'Ля-ля_фа....'
#                          })

print(response.status_code)
print(response.json())




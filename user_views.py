import json
from aiohttp import web
from bcrypt import hashpw, gensalt
from sqlalchemy.exc import IntegrityError

from models import User


def hash_password(password):
    password = password.encode()
    password = hashpw(password, salt=gensalt())
    password = password.decode()
    return password
    

async def get_user(user_id, session):
    user = await session.get(User, user_id)
    if user is None:
        raise web.HTTPNotFound(
            text=json.dumps({'error': 'user not found'}),
            content_type='application/json'
        )
    return user

class UserView(web.View):
    
    
    @property
    def session(self):
        return self.request['session']
    
    @property
    def user_id(self):
        return int(self.request.match_info['user_id'])
    
    
    async def get(self):
        user = await get_user(self.user_id, self.session)
        return web.json_response({
            'id': user.id,
            'username': user.username
        })
    
    async def post(self):
        json_data = await self.request.json()
        json_data['password'] = hash_password(json_data['password'])
        user = User(**json_data)
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as err:
            raise web.HTTPConflict(
                text=json.dumps({'error': 'user already exists'}),
                content_type='application/json'
            )
        return web.json_response({
            'id':user.id,
            'username': user.username,
            'email': user.email
            })
    
    async def patch(self):
        user = await get_user(self.user_id, self.session)
        json_data = await self.request.json()
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password'])
        for field, value in json_data.items():
            setattr(user, field, value)
        await self.session.commit()
        return web.json_response({'status': 'success'})
                
    
    async def delete(self):
        user = await get_user(self.user_id, self.session)
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({'status': 'success'})
import json
from aiohttp import web

from models import UserPost



async def get_post(post_id, sesion):
    post = await sesion.get(UserPost, post_id)
    if post is None:
        raise web.HTTPNotFound(
            text=json.dumps({'error': 'post not found'},),
            content_type='application/json'
        )
    return post


class PostView(web.View):
    @property
    def post_id(self):
        return int(self.request.match_info['post_id'])
        
    @property
    def session(self):
        return self.request['session']
        
        
    async def get(self):
        post = await get_post(self.post_id, self.session)
        return web.json_response({
            'id': post.id,
            'post_header': post.post_header,
            'post_text': post.post_text,
            'creator': post.creator_id,
            'created_at': str(post.created_at)
        })
    
    async def post(self):
        json_data = await self.request.json()
        post = UserPost(**json_data)
        self.session.add(post)
        await self.session.commit()
        return web.json_response({
            'id': post.id,
            'post_header': post.post_header,
            'post_text': post.post_text,
            'creator': post.creator_id,
            'created_at': str(post.created_at)
            })
    
    async def patch(self):
        post = await get_post(self.post_id, self.session)
        json_data = await self.request.json()
        for field, value in json_data.items():
            setattr(post, field, value)
        await self.session.commit()
        return web.json_response({
            'id': post.id,
            'post_header': post.post_header,
            'post_text': post.post_text,
            'creator': post.creator_id,
            'created_at': str(post.created_at)
        })
    
    async def delete(self):
        post = await get_post(self.post_id, self.session)
        await self.session.delete(post)
        await self.sesssion.commit()
        return web.json_response({'status': 'success'})
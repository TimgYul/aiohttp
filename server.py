from aiohttp import web

from models import Session, orm_context
from app_creation import app
from user_views import UserView
from post_views import PostView


@web.middleware
async def session_middleware(request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
        return response
    

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

    
app.add_routes([
 web.post('/users/', UserView),
 web.get('/users/{user_id:\d+}', UserView),
 web.patch('/users/{user_id:\d+}', UserView),
 web.delete('/users/{user_id:\d+}', UserView),
 web.post('/posts/', PostView),
 web.get('/posts/{post_id:\d+}', PostView),
 web.patch('/posts/{post_id:\d+}', PostView),
 web.delete('/posts/{post_id:\d+}', PostView) 
])


if '__main__' == __name__:
    web.run_app(app)
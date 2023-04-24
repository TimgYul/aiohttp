from flask import Flask, jsonify, request
from flask.views import MethodView
from typing import Type
from models import Session, User, UserPost
from hashlib import md5
from pydantic import ValidationError
from schema import CreateUser
from sqlalchemy.exc import IntegrityError

app = Flask('app')

class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'message': error.message})
    response.status_code = error.status_code
    return response


def get_user(user_id: int, session: Session):
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, message='User not found')
    return user

def validate_user(json_data: dict, model_class: Type[CreateUser]):
    try:
        model_item = model_class(**json_data)
        return model_item.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, err.errors()[0]['msg'])

class UserView(MethodView):
    
    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'rank': 'User' if user.is_admin == False else 'Admin'
            })
    
    def post(self):
        json_data = validate_user(request.json, CreateUser)
        json_data['password'] = md5(json_data['password'].encode()).hexdigest()
        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try: 
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, 'User already exists')
            return jsonify({
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email
            })
            
    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
            return jsonify({
                'status': 'success'
            })
            
def get_post(post_id: int, session: Session):
    post = session.get(UserPost, post_id)
    if post is None:
        raise HttpError(404, 'Not found')
    return post
    
    
class PostView(MethodView):
    
    def get(self, post_id: int):
        with Session() as session:
            post = get_post(post_id, session)
            return jsonify({
                'id': post.id,
                'autor': post.creator,
                'header': post.post_header,
                'text': post.post_text,
                'created_at': post.created_at            
            })
        
    def post(self):
        json_data = request.json
        with Session() as session:
            new_post = UserPost(**json_data)
            session.add(new_post)
            session.commit()
            return jsonify({
                'id': new_post.id,
                'creator': new_post.creator,
                'post_header': new_post.post_header,
                'post_text': new_post.post_text,
                'created_at': new_post.created_at 
            })
    
    def patch(self, post_id: int):
        json_data = request.json
        with Session() as session:
            post = get_post(post_id, session)
            for param, value in json_data.items():
                setattr(post, param, value)
            session.commit()
            return jsonify({
                'status': 'success'
            })
            
    
    def delete(self, post_id: int):
        with Session() as session:
            post = get_post(post_id, session)
            session.delete(post)
            session.commit()
            return jsonify({
                'status': 'Изменения применены'
            })
            

app.add_url_rule('/user/<int:user_id>/', 
                 view_func=UserView.as_view('user_existed'), 
                 methods=['GET', 'DELETE', ])
app.add_url_rule('/user/',
                 view_func=UserView.as_view('user'),
                 methods=['POST', ])
app.add_url_rule('/post/<int:post_id>/',
                 view_func=PostView.as_view('post_existed'),
                 methods=['GET', 'PATCH', 'DELETE', ])
app.add_url_rule('/post/',
                 view_func=PostView.as_view('post'),
                 methods=['POST', ])

if __name__ == '__main__':
    app.run()
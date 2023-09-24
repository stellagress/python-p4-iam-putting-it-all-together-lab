#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError



from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        data = request.get_json()

        if not data.get('username'):
            return {'message' : 'username not found'}, 422

        user = User(
            username = data.get('username'),
            image_url = data.get('image_url'),
            bio = data.get('bio'),
            
            # password_hash = data['password']
        )
        user.password_hash = data.get('password')

        if not user:
            return {'message' : 'invalid password'}, 422

        db.session.add(user)
        db.session.commit()
        session['user_id'] =  user.id

        return user.to_dict(), 201




class CheckSession(Resource):
    def get(self):

        user = User.query.filter(User.id ==  session.get('user_id')). first()

        if user:
            return user.to_dict(), 200
        else:
            return {}, 401



class Login(Resource):
    def post(self):

        user = User.query.filter(User.username == request.get_json().get('username')).first()
        if user and user.authenticate(request.get_json()['password']):
            session['user_id'] = user.id
            return user.to_dict()
        
        return {}, 401
            

class Logout(Resource):
    def delete(self):
        session['user_id'] = None 
        
        return {}, 401

class RecipeIndex(Resource):

    def get(self):

        user = User.query.filter(User.id == session.get('user_id')).first()

        if user:
            recipes = [recipe.to_dict() for recipe in Recipe.query.all()]
            return (recipes), 200
        else:
            return {"message": "unauthorized"}, 401

    def post(self):
        user = User.query.filter(User.id == session.get('user_id')).first()

        if user:
            json = request.get_json()

            try:
                recipe = Recipe(
                    title = json['title'],
                    instructions = json['instructions'],
                    minutes_to_complete = json['minutes_to_complete'],
                    user_id = session['user_id']
                )
                db.session.add(recipe)
                db.session.commit()
            except IntegrityError:
                return {"message": "failed"}, 422  

            return {
                "title" : recipe.title,
                "instructions" : recipe.instructions,
                "minutes_to_complete" : recipe.minutes_to_complete,
                "user_id" : recipe.user_id       
            }, 201
        else:
            return {"message": "unauthorized"}, 401




api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

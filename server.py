#добавить, получить одну или все, удалить книгу
#получить данные о пользователе - username


#!/usr/bin/python
# -*- coding: utf-8 -*-

from database import USERS, BOOKS
from flask import Flask, render_template, request, redirect, session, jsonify,make_response
from flask_restful import reqparse, abort, Api, Resource

PORT = 8055

app = Flask(__name__)
api = Api(app)
app.config['JSON_AS_ASCII'] = False


def abort_if_user_not_found(username):
    if not USERS.get(username):
        abort(404, message="User {} not found".format(username))


class User(Resource):
    def get(self):
        args = parser.parse_args()
        abort_if_user_not_found(args['login'])
        user = USERS.get(args['login'])
        if not user:
            return jsonify({'success': 'BAD'})

        if(user[2] == args['password']):
            return jsonify({'success': 'OK'})
        else:
            return jsonify({'success': 'BAD'})

def abort_if_book_not_found(bookid):
    if not BOOKS.get(bookid):
        abort(404, message="Book {} not found".format(bookid))

class ListOfBooks(Resource):
    def get(self):
        books = BOOKS.get_all()
        return  jsonify({'books': books})

    def post(self):
        args = parser.parse_args()
        booktitle = args['booktitle']
        author = args['author']
        text = args['text']
        BOOKS.insert(booktitle, author, text)
        return jsonify({'success': 'OK'})



class OneBook(Resource):
    def get(self, id):
        abort_if_book_not_found(id)
        book = BOOKS.get(id)
        return  jsonify({'book': book})

    def delete(self, id):
        abort_if_book_not_found(id)
        BOOKS.delete(id)
        return jsonify({'success': 'OK'})

parser = reqparse.RequestParser()
parser.add_argument('login', required=False)
parser.add_argument('password', required=False)
parser.add_argument('booktitle', required=False)
parser.add_argument('author', required=False)
parser.add_argument('text', required=False)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error404.html'), 404

api.add_resource(User,'/user')
api.add_resource(OneBook, '/books/<int:id>')
api.add_resource(ListOfBooks, '/books')

DEBUG = True
if DEBUG:
    if __name__ == '__main__':
        app.run(port=PORT, host='127.0.0.1')
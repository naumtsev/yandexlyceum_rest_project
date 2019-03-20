#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, session
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField, FileField
from wtforms.widgets import TextArea, TextInput
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
import random
from requests import get, post, delete, put
import time
from database import BOOKS, USERS
from convert_img import resize_image

server_url = 'http://127.0.0.1:8055'
def getURL(suffix):
    print(server_url + suffix)
    return server_url + suffix


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e70lIUUoXRKlXc5VUBmiJ9Hdi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/', methods=['POST', 'GET'])
def index():
    all_books = get(getURL('/books')).json()['books']

    cnt = 0
    buffer = [[]]


    for i in all_books:
        cnt += 1;
        buffer[-1].append((i[0], i[1], i[2]))
        if cnt == 3:
            cnt = 0
            buffer.append([])
    return render_template('books.html', BOOKS = buffer, session=session)

class AddBookForm(FlaskForm):
    booktitle = StringField('Название книги:', validators=[DataRequired()], widget=TextInput())
    author = StringField('Автор:', validators=[DataRequired()], widget=TextInput())
    content = TextAreaField('Содержание книги:', validators=[DataRequired()],widget=TextArea())
    image = FileField('Обложка:')
    submit = SubmitField('Отправить')

@app.route('/add_new_book', methods=['POST', 'GET'])
def add_new_book():
    if not 'username' in session:
        return redirect('/')

    form = AddBookForm()
    if form.validate_on_submit():
        booktitle = form.booktitle.data
        author = form.author.data
        content = form.content.data
        image = request.files['file']
        post(getURL('/books'), json={'booktitle': booktitle, 'text': content, 'author': author}).json()
        all = get(getURL('/books')).json()['books']
        gg = ''
        if(all):
            image.save('static/images/{}b.jpg'.format(all[-1][0]))
            gg = 'static/images/{}b.jpg'.format(all[-1][0])
        else:
            image.save('static/images/1b.jpg')
            gg ='static/images/1b.jpg'

        resize_image(input_image_path= gg,
                         output_image_path=gg.replace('b', ''),
                         size=(2 * 300, 2 * 456))
        os.remove(gg)


        return redirect('/')
    return render_template('add_new_book.html', form=form, session=session)



@app.route('/book/<id>', methods=['POST', 'GET'])
def readbook(id):
    now_book = get(getURL('/books/{}').format(id)).json()['book']

    if not now_book:
       return redirect('/')
    return render_template('readbook.html', id=now_book[0], booktitle=now_book[1], author=now_book[2], text=now_book[3])


@app.route('/delete/<id>', methods=['POST', 'GET'])
def deletebook(id):
    if not 'username' in session:
        return redirect('/')

    now_book = get(getURL('/books/{}').format(id)).json()['book']
    if not now_book:
       return redirect('/')
    delete(getURL('/books/{}'.format(id)))
    os.remove("static/images/{}.jpg".format(id))
    return redirect('/')



class LoginForm(FlaskForm):
    username = StringField('Login:', validators=[DataRequired()], widget=TextInput())
    password = StringField('Password:', validators=[DataRequired()], widget=TextInput())
    submit = SubmitField('Отправить')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect('/')
    form = LoginForm()

    if form.validate_on_submit():
        login = form.username.data
        password = form.password.data
        user = get(getURL('/user'), json={'login': login, 'password':password}).json()
        if('success' in user ):
            if user['success'] == 'OK':
                session['username'] = login
                return redirect('/')
            else:
                return render_template('login.html', session=session, form=form, status=1)
        else:
            return render_template('login.html', session=session, form=form, status=1)
    return render_template('login.html', session=session, form=form, status=0)

@app.route('/logout')
def logout():
    session.pop('username',0)
    print(1)
    return redirect('/')

@app.route('/error')
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error404.html', session=session), 404
	
	
DEBUG = True
if DEBUG:
    if __name__ == '__main__':
        app.run(port=8080, host='127.0.0.1')
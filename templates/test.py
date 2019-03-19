from requests import get, post, delete, put
url = 'http://127.0.0.1:8055'

def getURL(suffix):
    print(url + suffix)
    return url + suffix


print(get(getURL('/books/88')).json())

print(get(getURL('/books')).json())
print(get(getURL('/books/88')).json())
print(post(getURL('/books'), json={'booktitle':'Курочка', 'text': 'asdadds', 'author':'Антон'}).json())
print(delete(getURL('/books/90')).json())
print(get(getURL('/user'), json={'login':'admin', 'password':'dasdsad'}).json())
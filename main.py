from flask import Flask, request, jsonify
import json
import sqlite3
app = Flask(__name__)

book_list=[
    {
    "id":0,
    "author":"Chinua Achebe",
    "language":"English",
    "title":"THings Fall Apart"
    },
    {
    "id":1,
    "author":"Chinua Achebe",
    "language":"English",
    "title":"THings Fall Apart"
    },
]

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    
    return conn

@app.route('/books', methods=['GET','POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method== 'GET':
        cursor= conn.execute("SELECT * FROM book")
        books=[
            dict(id=row[0],author=row[1],language=row[2],title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book (author,language,title) VALUES (?,?,?)"""
        cursor= cur.execute(sql,(new_author,new_lang,new_title))
        conn.commit()
        return jsonify(f"book with the id {cursor.lastrowid} is created"),201
    
@app.route('/book/<int:id>',methods=['GET','PUT','DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id=?",(id,))
        rows = cursor.fetchall()
        for r in rows:
            book == r
        if book is not None:
            return jsonify(book),200
        else:
            "Something wrong happened",404

    if request.method == 'PUT':
        for book in book_list:
            if book['id']== id:
                book['authhor'] = request.form['author']
                book['language']=request.form['language']
                book['title'] = request.form['title']
                updated_book = {
                    'id':id,
                    'author':book['author'],
                    'language':book['language'],
                    'title':book['title']
                }
                sql = """UPDATE book SET title=?,author=?,language=? WHERE id=?"""
                conn.execute(sql,(book['author'],book['language'],book['title'],id))
                conn.commit()
                return jsonify(updated_book)
    if request.method == 'DELETE':
        sql = """DELETE FROM book WHERE id=?"""
        conn.execute(sql,(id))
        conn.commit()
        return "The book with id :{} has been deleted ".format(id),200
            

if __name__ == '__main__':
    app.run()
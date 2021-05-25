import sqlite3
from flask import Flask, request, session, g, redirect, render_template, flash
import requests


#############
# Using g to handle request
# #################

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = 'the random string' 

def connect_db():
    con = sqlite3.connect('user_books.db', check_same_thread=False)

    cur = con.cursor()
    cur.execute("CREATE TABLE if not exists users (id INTEGER PRIMARY KEY, email TEXT, password TEXT);")
    cur.execute("CREATE TABLE if not exists  booksOwned (id INTEGER PRIMARY KEY, isbn TEXT, user_id integer, author text, pagecount integer, rating text, image text, title text, googleLink text);")
    return con


@app.teardown_appcontext
def close_db(Exception):
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()

@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email  = request.form['email']
        password = request.form['password']
        user = g.db.execute("SELECT * FROM users where email = ? and password = ?", [email, password])
        user_fetch = user.fetchall()
        print(len(user_fetch), user_fetch)
        if len(user_fetch) < 1 :
            g.db.execute("Insert into users (email, password) values(?, ?)" , [email, password])
            g.db.commit()
        user = g.db.execute("SELECT * FROM users where email = ? and password = ?", [email, password])
        user_fetch = user.fetchall()
        session["username"] = email 
        session["id"] = user_fetch[0][0]
        if session['username'] != email:
            return render_template('/login.html', title="Login")
        else:
            return redirect("/")
    return render_template('/login.html', title="Login")
    

@app.route("/")
def view_home():
    print(session)
    try:
        if session['username'] is None or session['id'] is None:
            return redirect("/login")
        else:
            books_saved = g.db.execute("SELECT * FROM booksOwned where user_id=?", [session["id"]])
            books_saved_fetch = books_saved.fetchall()
            arr = []
            total = 0
            print(books_saved_fetch, "home")
            if len(books_saved_fetch) < 1:
                arr = None
            else:
                arr = books_saved_fetch
                total= len(books_saved_fetch)
                # for i in books_saved_fetch:
                #     req = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{i[1]}')
                #     for j in req.json()['items']:
                #         j['volumeInfo']['isbn'] = i[1]
                #         j['volumeInfo']['user_book_id'] = i[0]
                #         arr.append(j['volumeInfo'])
            return render_template("index.html", title="Home", session=session['username'], user_books = arr, total=total)
    except:
        return redirect("/login")
    

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('id', None)
   return redirect('/login')

@app.route("/getbook", methods=["POST", "GET"])
def view_getBooks():
    if request.method == 'POST':
        isbn  = request.form['isbn']
    elif request.method == 'GET':
        isbn = request.args.get('isbn')
    req = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
    lis=""
    if 'items' in req.json():
        lis = list(req.json()['items'])
    else:
        return redirect("/error")
    return render_template("index.html", title="Your Results", book=lis, isbn=isbn)

@app.route("/getbooktitle", methods=["POST", "GET"])
def view_getBooksTitle():
    if request.method == 'POST':
        title  = request.form['title']
    elif request.method == 'GET':
        title = request.args.get('title')
    req = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=title={title}')
    if 'items' in req.json():
        lis = list(req.json()['items'])
    else:
        return redirect("/error")
    books_saved = g.db.execute("SELECT * FROM booksOwned where user_id=?", [session["id"]])
    books_saved_fetch = books_saved.fetchall()
    if len(books_saved_fetch) > 0:
        for i in books_saved_fetch:
            title_filter = i[7]
            lis = list(filter(lambda x: x['volumeInfo']['title'] != title_filter, lis))
                    
    return render_template("index.html", title="Your Results", book=lis, isbn=None, bookTitle=title)

@app.route("/savebook", methods=["POST"])
def saveBooks():
    isbn = request.args.get('isbn')
    author = request.args.get('author')
    pageCount = request.args.get('pageCount')
    rating = request.args.get('rating')
    image = request.args.get('image')
    title = request.args.get('title')
    googleLink = request.args.get('googleLink')
    print("------------------------------------------------")
    flash(f'{title} has been saved')
    if googleLink is None:
        googleLink = '/'
    if image is None:
        image = '#'
    g.db.execute("insert into booksOwned (user_id, isbn, author, pagecount, rating, image, title, googleLink) values(?, ?, ?, ?, ?, ?, ?, ?)", 
    [session["id"], isbn, author, pageCount, rating, image.replace('>>', '&'), title, googleLink.replace('>>', '&')])
    g.db.commit()
    books_saved = g.db.execute("SELECT * FROM booksOwned where user_id=?", [session["id"]])
    books_saved_fetch = books_saved.fetchall()
    print(books_saved_fetch, "test")
    return redirect('/')

@app.route("/deletebook", methods=["Get"])
def deleteBooks():
    if request.method == 'GET':
        id = request.args.get('id')
    g.db.execute("delete from booksOwned where user_id=? and id=?", [session["id"], id])
    g.db.commit()
    return redirect('/')

@app.route("/error", methods=["Get"])
def view_error():
    return render_template("index.html", title="Error", session=session['username'])


     

if __name__=='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5003)
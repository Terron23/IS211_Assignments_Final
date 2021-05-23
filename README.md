# IS211_Assignments_Final

## pythonanywhere: http://tmj.pythonanywhere.com/

The application uses an email and passcode to login.<br />
The isbn field should only contain the <b>isbn number</b>

Otherwise application should be straightforward. Homepage contains books saved and the ability to delete books. All extra credit features have been added (I think). 
Furthermore App is built in the form of an SPA so all front end logic with the exception of the login page can be found on the index.html page.

## Database
The database contains two tables users and booksOwned. Table schemas can be found below:
CREATE TABLE if not exists users (id INTEGER PRIMARY KEY, email TEXT, password TEXT
CREATE TABLE if not exists  booksOwned (id INTEGER PRIMARY KEY, isbn TEXT, user_id integer, author text, pagecount integer, rating text, image text, title text




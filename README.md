# IS211_Assignments_Final

## pythonanywhere: http://tmj.pythonanywhere.com/

The application uses an email and passcode to login.<br />
The isbn field should only contain the <b>isbn number</b>

Otherwise application should be straightforward. Homepage contains books saved and the ability to delete books. All extra credit features have been added (I think). 
Furthermore App is built in the form of an SPA so all front end logic with the exception of the login page can be found on the index.html page.

## Database
The database contains two tables (users and booksOwned). Table schemas can be found below:<br />
CREATE TABLE if not exists users (id INTEGER PRIMARY KEY, email TEXT, password TEXT<br />
CREATE TABLE if not exists  booksOwned (id INTEGER PRIMARY KEY, isbn TEXT, user_id integer, author text, pagecount integer, rating text, image text, title text<br />
<b>Note:</b> The rating field = averageRating if the selected item has an averageRating key in the api. If averaRating is missing from the api the maturityRating gets added instead.

## Application startup
If running from the commandline use python app.py or python3.app.py<br />
<b>Note</b>: In the event of an issue delete the db and restart the app 

## PythonAnywhere 
I have encountered server overload issues. Most likely this will be fixed by refreshing your screen
<b>Note:</b> There are slight difference between the master branch and what exists on pythonanywhere. There is a slight change to the table schema and additional button added to the home page of the pythonanywhere code. To view the changes for the python anywhere code check the branch <b>pythonanywhere</b>




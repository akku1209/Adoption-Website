![alt text](https://i.postimg.cc/15w1ftps/pawdoptionslogo.jpg)
# PAWDOPTIONS
## Animal Adoption System
A user-friendly platform for animal adoptions for all the adopters and pet owners all over Pune.  
The user will be able to upload listings, view listings, sort them according to his/her preferred animal and location.
He/She can comment on listings and also bid for the number of the days he/she can foster the animal.
This system also uses a recommendation system which recommends useful articles & blogs to the user based on his prefered category of animal.

Recommendation system uses TFIDF Vectorizer Algorithm. This algorithm is applied on Category. Links of the articles are displayed at execution of this part of the system.

## Technologies
Django : Micro-web framework for Python

Sqlite3 : Database at the backend

HTML, CSS, Bootstrap : For user interface
## Installations
1. Download the code above and unzip it.
2. In your terminal with the path set to the unzipped folder, cd into Pawdoptions directory.
3. Run `python manage.py makemigrations auctions` to make migrations to the auctions app.
4. Run `python manage.py migrate` to apply migrations to your database.
5. Run `python manage.py runserver` 
OR  Run local server on broswer `127.0.0.1:8000`




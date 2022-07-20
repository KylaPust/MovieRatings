"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import Rating, connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():

    return render_template("homepage.html")

@app.route('/movies')
def all_movies():

    movies = crud.get_all_movies()

    return render_template("all_movies.html", movies=movies)

@app.route('/movies/<movie_id>')
def movie_details(movie_id):
    
    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route('/users')
def all_users():

    users = crud.get_all_users()
    return render_template("all_users.html", users=users)

@app.route('/users', methods=["POST"])
def create_account():
   
    email = request.form.get("email")
    password = request.form.get("password")
    existing_user = crud.get_user_by_email(email)

    if existing_user:
        flash("This user already exists!")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Yay! Your account was created, you can login!")
    
    return redirect("/")

@app.route('/login', methods=['POST'])
def user_login():

    email = request.form.get("email") 
    password = request.form.get("password")
    login_user = crud.get_user_by_email(email)  
    
    if login_user:
        if login_user.password != password:
            flash("Your password is wrong, try again")
        else:
            session['email'] = email
            flash(f"{login_user.email}, you're are all set!")
    else:
        flash("Invalid Email. Try again.")
    return redirect('/')

@app.route('/users/<user_id>')
def user_profile(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

@app.route('/new_rating/<movie_id>', methods=['POST'])
def new_rating(movie_id):


    score = request.form.get('rating')
    movie_id = crud.get_movie_by_id(movie_id)

    if 'email' in session:
        email = session.get('email')
    else:
        flash("Please Login to make a rating!")
        return redirect('/')

    
    for rating in movie_id.ratings:
        if rating.user.email == session['email']:

            flash("You've already rated this movie")
            return redirect(f"/users/{rating.user.user_id}")

    user = crud.get_user_by_email(email)
    new_rating = crud.create_rating(user, movie_id, score)
    db.session.add(new_rating)
    db.session.commit()

    flash("Rating Stored!")
    return redirect("/movies")


@app.route('/update_rating/<rating_id>', methods=["POST"])
def update_rating(rating_id):

    
    rating = crud.get_rating_by_id(rating_id)
    prev_score = rating.score
    score = request.form.get('update_rating')
  
    Rating.score = score
    db.session.commit()

    return f'prev_rating: {prev_score} new_rating: {rating.score}'

    


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

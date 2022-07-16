"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")
model.connect_to_db(server.app)
model.db.create_all()


# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title = movie["title"]
    overview = movie["overview"]
    poster_path = movie["poster_path"]
    release_string = movie["release_date"]
    release_date = datetime.strptime(release_string, "%Y-%m-%d")

    movie = crud.create_movie(title, overview, release_date, poster_path)

    """add movie to DB list"""
    movies_in_db.append(movie)

model.db.session.add_all(movies_in_db)
# model.db.session.commit()


for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        movie = choice(movies_in_db)
        score = randint(0,6)

        user_rating = crud.create_rating(user, movie, score)

        model.db.session.add(user_rating)


model.db.session.commit()


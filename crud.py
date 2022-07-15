"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email2, password2):
    """Create and return a new user."""

    user = User(email=email2, password=password2)

    return user


def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(
        title=title, 
        overview=overview, 
        release_date=release_date, 
        poster_path=poster_path)

    return movie

def create_rating(user, movie, score):

    rating = Rating(score=score,
                    user=user,
                    movie=movie)
    
    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
from flask import jsonify,url_for, make_response, abort 
from flask import request
from app.models import Movies
from app.database import db_session
from app.api_1_0 import api

@api.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movies.query.get(id)
    return jsonify(movie.to_json())
	
@api.route('/movies/', methods=['GET'])
def get_movies():
    movies = Movies.query.all()
    return jsonify({'movies': [movie.to_json() for movie in movies]})
	
	#page = request.args.get('page', 1, type=int)
    #per_page = min(request.args.get('per_page', 10, type=int), 100)
    #data = Movie.to_collection_dict(Movie.query, page, per_page, 'api.get_movies')    
    #return jsonify(data)
	
@api.route('/movies/', methods=['POST'])
#@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    movie = Movies.from_json(request.json)
    
    if movie.year > 2100:
        abort(make_response(jsonify({"status":400,
        "reason":"Field 'year' should be less then 2100"}), 400))
    if movie.title is None:
        abort (make_response(jsonify({"status":400,
        "reason":"Field 'title' is required"}), 400))
    db_session.add(movie)
    db_session.commit()
    return (jsonify(movie.to_json()), 200,
	{'Location': url_for('api.get_movie', id=movie.id, _external=True)})
	
@api.route('/movies/<int:id>', methods=['PUT'])
def edit_movie(id):
    movie = Movies.query.get(id)
    if movie is None:
        movie = Movies.from_json(request.json)   
    movie.director = request.json.get('director', movie.director)
    movie.year = request.json.get('year', movie.year)
    movie.title = request.json.get('title', movie.title)
    movie.length = request.json.get('length', movie.length)
    movie.rating = request.json.get('rating', movie.rating)
    db_session.add(movie)
    db_session.commit()
    return(jsonify(movie.to_json()), 200, 
    {'Location': url_for('api.get_movie', id=movie.id, _external=True)})
    
@api.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movies.query.get(id)
    db_session.delete(movie)
    db_session.commit()
    return (jsonify(movie.to_json()), 200,
    {'Location': url_for('api.get_movie', id=movie.id, _external=True)})
	
@api.errorhandler(404)
def not_found(error):
    return (make_response(jsonify({"status":404,
	"reason":"Not found"}), 404))
	
@api.errorhandler(500)
def internal_error(error):
    return (make_response(jsonify({"status":500,
	"reason":"Invalid request.Check record number"}), 500))
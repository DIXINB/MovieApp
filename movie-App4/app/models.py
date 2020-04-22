from sqlalchemy import Column, Integer, String
from app.database import Base


class Movies(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True)
    year = Column(Integer)
    director = Column(String(22))
    length = Column(String(8))
    rating = Column(Integer)
    
	
    def __init__(self, id=None, title=None, year=None, director=None,
        	     length=None, rating=None):
        self.id = id
        self.title = title
        self.year = year
        self.director = director
        self.length = length
        self.rating = rating
		
                
    def __repr__(self):
        return ('{: ^4}{: ^30}{:4}{: ^22}{:8}{: >2}'.format(self.id,
                self.title,self.year,self.director,self.length,self.rating))
		
        		
    def to_json(self):
        json_movie = {
            'id':self.id,
            'title':self.title,
            'year':self.year,
            'director':self.director,
            'length':self.length,
            'rating': self.rating
        }
        return json_movie
	
    @staticmethod
    def from_json(json_movie):	
        id = json_movie.get('id')
        title = json_movie.get('title')
        year = json_movie.get('year')
        director = json_movie.get('director')
        length = json_movie.get('length')
        rating = json_movie.get('rating')
				       
        return Movies(id=id, title=title, year=year, director=director, 
		              length=length, rating=rating)
		
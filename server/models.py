from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name field is required.")
        author = db.session.query(Author.id).filter_by(name = name).first()
        print(author)
        if author is not None:
            raise ValueError("Name must be unique.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError('Number must be 10 digits')
        return number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('content', 'summary')
    def validate_content(self, key, string):
        if(key == 'content'):
            if len(string) < 250:
                raise ValueError("Post content must be greater than or equal 250 characters long.")
            return string
        elif(key == 'summary'):
            if len(string) > 250:
                raise ValueError("summary must be less then 250 charachters")
            return string
        
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title")
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(s in title for s in clickbait):
            raise ValueError("Title must include clickbait")
        return title
    
    @validates('category')
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("Category must be either fiction or non fiction")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

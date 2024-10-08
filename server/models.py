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
    def validate_name(self, key,name):
        if not  name:
            raise ValueError("Author name cannot be empty")
        
         # Check for uniqueness
        if Author.query.filter_by(name=name).first() is not None:
            raise ValueError('An author with this name already exists.')
        return name

    
   
    
    @validates('phone_number')
    def validate_phonenumber(self,key,phone_number):
        if not phone_number.isdigit() or len(phone_number)!=10:
            raise ValueError("phone numbers are exactly ten digits")
        return phone_number
    
    

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
    @validates('content')
    def validates_content(self,key,content):
        if len(content)<250:
            raise ValueError("Post Content is atleast 250 characters long")
        return content
    
    @validates('summary')
    def validates_summary(self,key,summary):
        if len(summary)>250:
            raise ValueError("Post summary is a maximum of 250 characters")
        return summary
    
    @validates('category')
    def validates_category(self,key,category):
        if category not in['Fiction','Non-Fiction']:
            raise ValueError("Post category is either Fiction or Non-Fiction.")
        return category
    
    @validates('title')
    def validates_title(self,key,title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Post title is sufficiently clickbait-y and must contain one of the following:")
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'

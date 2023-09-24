from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt


from sqlalchemy import CheckConstraint, text
# from sqlalchemy import MetaData
# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)



class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-recipes.user',)

    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.String, unique=True, nullable = False)
    # _password_hash = db.Column(db.String)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', backref='user')

    def __repr__(self):
        return f'<User {self.username} | Password: {self._password_hash} | image: {self.image_url} | bio: {self.bio}>'
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Action Not Allowed')
        # return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        # utf-8 encoding and decoding is required in python 3
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    __table_args__ = (
        db.CheckConstraint("length(instructions) >= 50"),
    )


    serialize_rules = ('-user.recipes',)
    
    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String, nullable = False)
    instructions = db.Column(db.String, nullable = False)
    minutes_to_complete = db.Column(db.Integer)


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Recipe {self.title} | Instructions: {self.instructions} | Minutes: {self.minutes_to_complete}>'







# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy_serializer import SerializerMixin

# from config import db, bcrypt

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'

#     pass

# class Recipe(db.Model, SerializerMixin):
#     __tablename__ = 'recipes'
    
#     pass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship 

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
#StarWars DB

class Users_StarWars(db.Model):
    __tablename__ = 'users_starwars'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    #relation user_favorites_characters
    user_like_character: Mapped [list['User_Favorites_Characters']] = relationship(back_populates = 'user_favorites_character')
    #relation user_favorites_planets
    user_like_planet: Mapped [list['User_Favorites_Planets']] = relationship(back_populates = 'user_favorites_planets')
    #relation user_favorites_starships
    user_like_starship: Mapped [list['User_Favorites_Starships']] = relationship(back_populates = 'user_favorites_starships')

class Characters_StarWars(db.Model):
    __tablename__ = 'characters_starwars'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specie: Mapped[str] = mapped_column(String(30), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    #relation planets_starwars
    planet_habit: Mapped [list['Planets_StarWars']] = relationship(back_populates = 'character_for_planet')
    #relation user_favorites_characters
    user_characters_favorites: Mapped [list['User_Favorites_Characters']] = relationship(back_populates = 'characters_favorites')

class Planets_StarWars(db.Model):
    __tablename__ = 'planets_starwars'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    appearances: Mapped[str] = mapped_column(String(300), nullable=False)
    species_types: Mapped[str] = mapped_column(String(30), nullable=False)
    #relation characters_starwars
    natives_characters: Mapped[int] = mapped_column(ForeignKey('characters_starwars.id'))
    character_for_planet: Mapped['Characters_StarWars'] = relationship(back_populates = 'planet_habit')
    #relation user_favorites_planets
    user_planets_favorites: Mapped [list['User_Favorites_Planets']] = relationship(back_populates = 'planets_favorites')



class Starships_StarWars(db.Model):
    __tablename__ = 'starships_starwars'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    appearances: Mapped[str] = mapped_column(String(300), nullable=False)
    affiliations: Mapped[str] = mapped_column(String(100), nullable=False)
    dimensions: Mapped[float] = mapped_column(Float, nullable=False)
    #relation user_favorites_starships
    user_starships_favorites: Mapped [list['User_Favorites_Starships']] = relationship(back_populates = 'starships_favorites')
    

#auxiliary dbs

class User_Favorites_Characters(db.Model):
    __tablename__ = 'user_favorites_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    #relation user
    user_id: Mapped[int] = mapped_column(ForeignKey('users_starwars.id'))
    user_favorites_character: Mapped['Users_StarWars'] = relationship(back_populates = 'user_like_character')
    #relation characters
    characters_id: Mapped[int] = mapped_column(ForeignKey('characters_starwars.id'))
    characters_favorites: Mapped['Characters_StarWars'] = relationship(back_populates = 'user_characters_favorites')
    #relation characters

class User_Favorites_Planets(db.Model):
    __tablename__ = 'user_favorites_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    #relation user
    user_id: Mapped[int] = mapped_column(ForeignKey('users_starwars.id'))
    user_favorites_planets: Mapped['Users_StarWars'] = relationship(back_populates = 'user_like_planet')
    #relation planets 
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets_starwars.id'))
    planets_favorites: Mapped['Planets_StarWars'] = relationship(back_populates = 'user_planets_favorites')

class User_Favorites_Starships(db.Model):
    __tablename__ = 'user_favorites_starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    #relation user
    user_id: Mapped[int] = mapped_column(ForeignKey('users_starwars.id'))
    user_favorites_starships: Mapped['Users_StarWars'] = relationship(back_populates = 'user_like_starship')
    #relation starships
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships_starwars.id'))
    starships_favorites: Mapped['Starships_StarWars'] = relationship(back_populates = 'user_starships_favorites')



#INSTAGRAM DB

class Users_Instagram (db.Model):
    __tablename__ = 'users_instagram'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(20), nullable=False)
    lastname: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    #relations followes_instagram/user_from_id
    user_like_follower: Mapped [list['Followers_Instagram']] = relationship(back_populates = 'user_follow')
    #relations followes_instagram/user_to_id
    user_following: Mapped [list['Followers_Instagram']] = relationship(back_populates = 'user_to_follow')
    #relation comment_instagram
    comment_user: Mapped [list['Comment_Instagram']] = relationship(back_populates = 'user_author_comment')
    #relation post_instagram
    post_user: Mapped [list['Post_Instagram']] = relationship(back_populates = 'user_id_post')

class Followers_Instagram (db.Model):
    __tablename__ = 'followers_instagram'
    id: Mapped[int] = mapped_column(primary_key=True)
    #relations users_instagram
    user_from_id: Mapped[int] = mapped_column(ForeignKey('users_instagram.id'))
    user_follow: Mapped['Users_Instagram'] = relationship(back_populates = 'user_like_follower')
     #relations users_instagram
    user_to_id: Mapped[int] = mapped_column(ForeignKey('users_instagram.id'))
    user_to_follow: Mapped['Users_Instagram'] = relationship(back_populates = 'user_following')

class  Post_Instagram (db.Model):
    __tablename__ = 'post_instagram'
    id: Mapped[int] = mapped_column(primary_key=True)
    #relation user_instagram
    user_id: Mapped[int] = mapped_column(ForeignKey('users_instagram.id'))
    user_id_post: Mapped['Users_Instagram'] = relationship(back_populates = 'post_user')
    #relation comment_instagram
    post_to_comment: Mapped [list['Comment_Instagram']] = relationship(back_populates = 'post_id_select')
    #relation media_instagram
    post_to_media: Mapped [list['Media_Instagram']] = relationship(back_populates = 'post_id_media')

class  Comment_Instagram (db.Model):
    __tablename__ = 'comment_instagram'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(200), nullable=False)
    #relation user_instagram
    author_id: Mapped[int] = mapped_column(ForeignKey('users_instagram.id'))
    user_author_comment: Mapped['Users_Instagram'] = relationship(back_populates = 'comment_user')
    #relation post_instagram
    post_id: Mapped[int] = mapped_column(ForeignKey('post_instagram.id'))
    post_id_select: Mapped['Post_Instagram'] = relationship(back_populates = 'post_to_comment')

class  Media_Instagram (db.Model):
    __tablename__ = 'media_instagram'
    id: Mapped[int] = mapped_column(primary_key=True)
    url_media: Mapped[str] = mapped_column(String(300), nullable=False)
    #relation post_instagram
    post_id: Mapped[int] = mapped_column(ForeignKey('post_instagram.id'))
    post_id_media: Mapped['Post_Instagram'] = relationship(back_populates = 'post_to_media')



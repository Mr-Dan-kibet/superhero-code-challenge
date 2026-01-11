from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import  relationship

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)


class Hero(db.Model):

    __tablename__ = "heros"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # defines relationship between heros and hero_powers tables
    hero_powers = relationship("HeroPower", back_populates="hero", cascade="all, delete-orphan")

    # defines association proxy beween heros and powers tables
    powers = association_proxy("hero_powers", "power")

class Power(db.Model):

    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # defines relationship between powers and hero_powers tables
    hero_powers = relationship("HeroPower", back_populates="power", cascade="all, delete-orphan")

    # defines association proxy beween heros and powers tables
    heroes = association_proxy("hero_powers", "hero")



class HeroPower(db.Model):

    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey("heros.id"))
    power_id =  db.Column(db.Integer, db.ForeignKey("powers.id"))

    # defines population relationship between her0_powers and all other tables
    hero = relationship("Hero", back_populates='hero_powers')
    power = relationship("Power", back_populates='hero_powers')


    
    
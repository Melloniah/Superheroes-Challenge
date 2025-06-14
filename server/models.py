from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata=MetaData()

db=SQLAlchemy(metadata=metadata)


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    id=db.Column(db.Integer, primary_key=True)
    _strength=db.Column("strength", db.String)
    
    #foreign keys
    hero_id= db.Column(db.Integer, db.ForeignKey("heroes.id"))
    power_id= db.Column(db.Integer, db.ForeignKey("powers.id"))

    #relationships
    hero=db.relationship("Hero", back_populates='hero_powers')
    power=db.relationship("Power", back_populates='hero_powers')

    serialize_rules=('-hero.hero_powers', '-power.hero_powers') #Skip listing all hero_powers entirely

    #Strength validation
    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        allowed_strengths=["Strong", "Average", "Weak"]
        if value not in allowed_strengths:
            raise ValueError(f"strength must be one of: {allowed_strengths}")
        self._strength=value



class Hero (db.Model, SerializerMixin):
    __tablename__ ='heroes'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    super_name=db.Column(db.String)

    #relationship
    hero_powers=db.relationship('HeroPower', back_populates='hero', cascade= "all, delete-orphan")
 
    #serialization
    serialize_rules=('-hero_powers.hero',) #Inside each HeroPower, skip its .hero

   
class Power(db.Model, SerializerMixin):

    __tablename__ ='powers' 
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    _description=db.Column(db.String)  

    hero_powers=db.relationship('HeroPower', back_populates='power', cascade="all, delete-orphan")

    #serialization
    serialize_rules=('-hero_powers.power',) #Inside Power, skip .hero_powers


#description validation

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
       if not value or len(value)< 20:
           raise ValueError(f"Description cannot be empty or be less than 20 characters long")
       self._description=value        
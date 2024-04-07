from app import db

pokemon_skills = db.Table('pokemon_skills',
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

pokemon_weaknesses = db.Table('pokemon_weaknesses',
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), primary_key=True),
    db.Column('weakness_id', db.Integer, db.ForeignKey('weakness.id'), primary_key=True)
)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    hp = db.Column(db.Integer, default=100)
    skills = db.relationship('Skill', secondary=pokemon_skills, lazy='subquery', backref=db.backref('pokemons', lazy=True))
    weaknesses = db.relationship('Weakness', secondary=pokemon_weaknesses, lazy='subquery', backref=db.backref('pokemons', lazy=True))


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Weakness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Battle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon1_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    pokemon2_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'))

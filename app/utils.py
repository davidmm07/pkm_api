from .models import db, Skill, Weakness

def add_skill_to_pokemon(pokemon, skill_name):
    skill = Skill(name=skill_name, pokemon=pokemon)
    db.session.add(skill)
    db.session.commit()

def add_weakness_to_pokemon(pokemon, weakness_name):
    weakness = Weakness(name=weakness_name, pokemon=pokemon)
    db.session.add(weakness)
    db.session.commit()

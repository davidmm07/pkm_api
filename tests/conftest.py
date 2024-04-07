import pytest
from app import create_app, db
from app.models import Pokemon, Skill, Weakness, Battle


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def new_pokemon(new_skill,new_weakness):
    pokemon = Pokemon(name='Charmander', attack=35,
                      defense=15, speed=40, hp=140,skills=[new_skill], weaknesses=[new_weakness])
    db.session.add(pokemon)
    db.session.commit()
    return pokemon


@pytest.fixture
def new_pokemon2(new_skill_2,new_weakness_2):
    pokemon = Pokemon(name='Squirtle', attack=30, defense=10,
                      speed=30, hp=140, skills=[new_skill_2], weaknesses=[new_weakness_2])
    db.session.add(pokemon)
    db.session.commit()
    return pokemon


@pytest.fixture
def new_pokemon3(new_skill_3,new_weakness_3):
    pokemon = Pokemon(name='Pikachu', attack=30, defense=10, speed=30,
                      hp=140, skills=[new_skill_3], weaknesses=[new_weakness_3])
    db.session.add(pokemon)
    db.session.commit()
    return pokemon


@pytest.fixture
def new_skill():
    skill = Skill(name='Flamethrower')
    db.session.add(skill)
    db.session.commit()
    return skill



@pytest.fixture
def new_weakness():
    weakness = Weakness(name='Water')
    db.session.add(weakness)
    db.session.commit()
    return weakness

@pytest.fixture
def new_skill_2():
    skill = Skill(name='Water')
    db.session.add(skill)
    db.session.commit()
    return skill

@pytest.fixture
def new_skill_3():
    skill = Skill(name='Thunderbolt')
    db.session.add(skill)
    db.session.commit()
    return skill


@pytest.fixture
def new_weakness_2():
    weakness = Weakness(name='Thunderbolt')
    db.session.add(weakness)
    db.session.commit()
    return weakness
@pytest.fixture
def new_weakness_3():
    weakness = Weakness(name='Ground')
    db.session.add(weakness)
    db.session.commit()
    return weakness

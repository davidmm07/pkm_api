from flask import Blueprint, request, jsonify
from .models import db, Pokemon, Skill, Weakness, Battle
from .utils import add_skill_to_pokemon, add_weakness_to_pokemon

pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('/pokemon', methods=['GET'])
def list_pokemon():
    name_filter = request.args.get('name')
    skill_filter = request.args.get('skill')
    weakness_filter = request.args.get('weakness')

    pokemon_query = Pokemon.query

    if name_filter:
        pokemon_query = pokemon_query.filter_by(name=name_filter)

    if skill_filter:
        pokemon_query = pokemon_query.join(Pokemon.skills).filter(Skill.name == skill_filter)

    if weakness_filter:
        pokemon_query = pokemon_query.join(Pokemon.weaknesses).filter(Weakness.name == weakness_filter)

    pokemon_list = pokemon_query.all()

    return jsonify([{'id': pokemon.id, 'name': pokemon.name, 'skills': [skill.name for skill in pokemon.skills], 'weaknesses': [weakness.name for weakness in pokemon.weaknesses]} for pokemon in pokemon_list])


@pokemon_bp.route('/pokemon', methods=['POST'])
def create_pokemon():
    data = request.json
    name = data.get('name')
    attack = data.get('attack')
    defense = data.get('defense')
    speed = data.get('speed')
    hp = data.get('hp')
    skills = data.get('skills', [])
    weaknesses = data.get('weaknesses', [])

    if not name or not attack or not defense or not speed or not hp:
        return jsonify({'message': 'All fields (name, attack, defense, speed, hp) are required!'}), 400

    pokemon = Pokemon(name=name, attack=attack, defense=defense, speed=speed, hp=hp)

    for skill_name in skills:
        skill = Skill.query.filter_by(name=skill_name).first()
        if not skill:
            skill = Skill(name=skill_name)
            db.session.add(skill)
        pokemon.skills.append(skill)

    for weakness_name in weaknesses:
        weakness = Weakness.query.filter_by(name=weakness_name).first()
        if not weakness:
            weakness = Weakness(name=weakness_name)
            db.session.add(weakness)
        pokemon.weaknesses.append(weakness)

    db.session.add(pokemon)
    db.session.commit()

    return jsonify({
        'message': 'Pokemon created successfully!',
        'pokemon': {
            'id': pokemon.id,
            'name': pokemon.name,
            'attack': pokemon.attack,
            'defense': pokemon.defense,
            'speed': pokemon.speed,
            'hp': pokemon.hp,
            'skills': [skill.name for skill in pokemon.skills],
            'weaknesses': [weakness.name for weakness in pokemon.weaknesses]
        }
    }), 201

@pokemon_bp.route('/pokemon/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if not pokemon:
        return jsonify({'message': 'Pokemon not found!'}), 404
    
    pokemon_data = {
        'id': pokemon.id,
        'name': pokemon.name,
        'attack': pokemon.attack,
        'defense': pokemon.defense,
        'speed': pokemon.speed,
        'hp': pokemon.hp,
        'skills': [skill.name for skill in pokemon.skills],
        'weaknesses': [weakness.name for weakness in pokemon.weaknesses]
    }
    
    return jsonify(pokemon_data)
@pokemon_bp.route('/pokemon/<int:pokemon_id>', methods=['PUT'])
def update_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if not pokemon:
        return jsonify({'message': 'Pokemon not found!'}), 404

    data = request.json
    name = data.get('name')
    attack = data.get('attack')
    defense = data.get('defense')
    speed = data.get('speed')
    hp = data.get('hp')
    skills = data.get('skills', [])
    weaknesses = data.get('weaknesses', [])

    if not name or not attack or not defense or not speed or not hp:
        return jsonify({'message': 'All fields (name, attack, defense, speed, hp) are required!'}), 400

    pokemon.name = name
    pokemon.attack = attack
    pokemon.defense = defense
    pokemon.speed = speed
    pokemon.hp = hp

    # Clear current skills and weaknesses
    pokemon.skills.clear()
    pokemon.weaknesses.clear()

    # Add new skills
    for skill_name in skills:
        skill = Skill.query.filter_by(name=skill_name).first()
        if not skill:
            skill = Skill(name=skill_name)
            db.session.add(skill)
        pokemon.skills.append(skill)

    # Add new weaknesses
    for weakness_name in weaknesses:
        weakness = Weakness.query.filter_by(name=weakness_name).first()
        if not weakness:
            weakness = Weakness(name=weakness_name)
            db.session.add(weakness)
        pokemon.weaknesses.append(weakness)

    db.session.commit()

    return jsonify({
        'message': 'Pokemon updated successfully!',
        'pokemon': {
            'id': pokemon.id,
            'name': pokemon.name,
            'attack': pokemon.attack,
            'defense': pokemon.defense,
            'speed': pokemon.speed,
            'hp': pokemon.hp,
            'skills': [skill.name for skill in pokemon.skills],
            'weaknesses': [weakness.name for weakness in pokemon.weaknesses]
        }
    }), 200


@pokemon_bp.route('/pokemon/<int:pokemon_id>', methods=['DELETE'])
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if not pokemon:
        return jsonify({'message': 'Pokemon not found!'}), 404
    db.session.delete(pokemon)
    db.session.commit()
    return jsonify({'message': 'Pokemon deleted successfully!'})

@pokemon_bp.route('/battle', methods=['POST'])
def battle():
    data = request.get_json()
    pokemon1_id = data.get('pokemon1_id')
    pokemon2_id = data.get('pokemon2_id')

    pokemon1 = Pokemon.query.get(pokemon1_id)
    pokemon2 = Pokemon.query.get(pokemon2_id)

    if not pokemon1 or not pokemon2:
        return jsonify({'message': 'Both Pokemon should exist!'}), 404

    pokemon1_skills = [skill.name for skill in pokemon1.skills]
    pokemon2_weaknesses = [weakness.name for weakness in pokemon2.weaknesses]

    for skill in pokemon1_skills:
        if skill in pokemon2_weaknesses:
            winner = pokemon1.name
            break
    else:
        winner = pokemon2.name

    new_battle = Battle(pokemon1_id=pokemon1_id, pokemon2_id=pokemon2_id, winner_id=pokemon1.id if winner == pokemon1.name else pokemon2.id)
    db.session.add(new_battle)
    db.session.commit()

    return jsonify({'message': f'{winner} wins the battle!', 'winner': winner,'battle_id':new_battle.id})

@pokemon_bp.route('/battle/<int:battle_id>', methods=['DELETE'])
def delete_battle(battle_id):
    battle = Battle.query.get(battle_id)
    if not battle:
        return jsonify({'message': 'Battle not found!'}), 404
    db.session.delete(battle)
    db.session.commit()
    return jsonify({'message': 'Battle deleted successfully!'})

@pokemon_bp.route('/battle/survival', methods=['POST'])
def survival_battle():
    data = request.get_json()
    pokemon1_id = data.get('pokemon1_id')
    pokemon2_id = data.get('pokemon2_id')

    pokemon1 = Pokemon.query.get(pokemon1_id)
    pokemon2 = Pokemon.query.get(pokemon2_id)

    if not pokemon1 or not pokemon2:
        return jsonify({'message': 'Both Pokemon should exist!'}), 404

    while pokemon1.hp > 0 and pokemon2.hp > 0:
        if pokemon1.speed > pokemon2.speed:
            attack_pokemon = pokemon1
            defense_pokemon = pokemon2
        elif pokemon1.speed < pokemon2.speed:
            attack_pokemon = pokemon2
            defense_pokemon = pokemon1
        else:
            if pokemon1.attack > pokemon2.attack:
                attack_pokemon = pokemon1
                defense_pokemon = pokemon2
            else:
                attack_pokemon = pokemon2
                defense_pokemon = pokemon1

        damage = attack_pokemon.attack - defense_pokemon.defense
        if damage <= 0:
            damage = 1

        defense_pokemon.hp -= damage

    winner = pokemon1 if pokemon1.hp > 0 else pokemon2

    new_battle = Battle(pokemon1_id=pokemon1_id, pokemon2_id=pokemon2_id, winner_id=winner.id)
    db.session.add(new_battle)
    db.session.commit()

    return jsonify({'message': f'{winner.name} wins the survival battle!', 'winner': {'id': winner.id, 'name': winner.name, 'hp': winner.hp}})

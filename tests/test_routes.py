def test_create_pokemon(client):
    response = client.post(
        '/pokemon',
        json={
            'name': 'Pikachu',
            'attack': 40,
            'defense': 30,
            'speed': 50,
            'hp': 100,
            'skills': ['Thunderbolt'],
            'weaknesses': ['Ground']
        }
    )
    assert response.status_code == 201
    assert response.json['message'] == 'Pokemon created successfully!'
    assert response.json['pokemon']['name'] == 'Pikachu'
    assert response.json['pokemon']['attack'] == 40
    assert response.json['pokemon']['defense'] == 30
    assert response.json['pokemon']['speed'] == 50
    assert response.json['pokemon']['hp'] == 100
    assert response.json['pokemon']['skills'] == ['Thunderbolt']
    assert response.json['pokemon']['weaknesses'] == ['Ground']


def test_get_pokemon(client, new_pokemon, new_skill, new_weakness):
    response = client.get(f'/pokemon/{new_pokemon.id}')
    assert response.status_code == 200
    assert response.json['name'] == new_pokemon.name
    assert response.json['attack'] == new_pokemon.attack
    assert response.json['defense'] == new_pokemon.defense
    assert response.json['speed'] == new_pokemon.speed
    assert response.json['hp'] == new_pokemon.hp
    assert response.json['skills'] == [new_skill.name]
    assert response.json['weaknesses'] == [new_weakness.name]


def test_update_pokemon(client, new_pokemon):
    response = client.put(f'/pokemon/{new_pokemon.id}', json={
                          'name': new_pokemon.name, 'attack': new_pokemon.attack,
                          'defense': new_pokemon.defense, 'speed': new_pokemon.speed, 'hp': new_pokemon.hp})
    assert response.status_code == 200
    assert response.json['message'] == 'Pokemon updated successfully!'
    assert response.json['pokemon']['name'] == 'Charmander'
    assert response.json['pokemon']['attack'] == 35
    assert response.json['pokemon']['defense'] == 15
    assert response.json['pokemon']['speed'] == 40


def test_delete_pokemon(client, new_pokemon):
    response = client.delete(f'/pokemon/{new_pokemon.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Pokemon deleted successfully!'


def test_battle_per_weaknesses(client, new_pokemon, new_pokemon2):
    response = client.post(
        '/battle', json={'pokemon1_id': new_pokemon.id, 'pokemon2_id': new_pokemon2.id})
    assert response.status_code == 200
    assert response.json['message'] == f'{new_pokemon2.name} wins the battle!'
    assert response.json['winner'] == new_pokemon2.name


def test_request_battle(client, new_pokemon2, new_pokemon3):
    response = client.post(
        '/battle', json={'pokemon1_id': new_pokemon2.id, 'pokemon2_id': new_pokemon3.id})
    assert response.status_code == 200
    assert response.json['message'] == f'{new_pokemon3.name} wins the battle!'
    assert response.json['winner'] == new_pokemon3.name


def test_delete_battle(client, new_pokemon, new_pokemon2):
    response = client.post(
        '/battle', json={'pokemon1_id': new_pokemon.id, 'pokemon2_id': new_pokemon2.id})
    battle_id = response.json['battle_id']
    response = client.delete(f'/battle/{battle_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Battle deleted successfully!'


def test_list_pokemon(client, new_pokemon3, new_skill, new_weakness, new_pokemon2):
    skills_names = [skill.name for skill in new_pokemon3.skills]
    weaknesses_names = [weakness.name for weakness in new_pokemon3.weaknesses]
    
    response = client.post('/pokemon', json={'name': new_pokemon3.name, 'attack': new_pokemon3.attack, 'defense': new_pokemon3.defense,
                           'speed': new_pokemon3.speed, 'skills': skills_names, 'weaknesses': weaknesses_names})
    response = client.get('/pokemon')

    assert response.status_code == 200
    assert len(response.json) == 2  # Two pokemons in the list
    # Pikachu is in the list
    assert any(pokemon['name'] == 'Pikachu' for pokemon in response.json)
    # The other new_pokemon is also in the list
    assert any(pokemon['name'] ==
               new_pokemon2.name for pokemon in response.json)



def test_list_pokemon_with_name_filter(client, new_pokemon, new_pokemon2, new_pokemon3):
    Charmander=new_pokemon
    Squirtle =new_pokemon2
    Pikachu = new_pokemon3
    response = client.get('/pokemon?name=Pikachu')
    
    assert response.status_code == 200
    assert len(response.json) == 1  # Only Pikachu in the list
    assert response.json[0]['name'] == Pikachu.name

    response = client.get('/pokemon?name=Squirtle')
    
    assert response.status_code == 200
    assert len(response.json) == 1  # Only Squirtle in the list
    assert response.json[0]['name'] == Squirtle.name

def test_list_pokemon_with_skill_filter(client, new_pokemon, new_skill, new_weakness, new_pokemon2):
    response = client.get(f'/pokemon?skill={new_skill.name}')
    
    assert response.status_code == 200
    assert len(response.json) == 1  # Only new_pokemon with the specified skill in the list
    assert response.json[0]['name'] == new_pokemon.name


def test_list_pokemon_with_weakness_filter(client, new_pokemon, new_skill, new_weakness, new_pokemon2):
    response = client.get(f'/pokemon?weakness={new_weakness.name}')
    
    assert response.status_code == 200
    assert len(response.json) == 1  # Only new_pokemon with the specified weakness in the list
    assert response.json[0]['name'] == new_pokemon.name

def test_survival_battle(client, new_pokemon, new_pokemon2):
    new_pokemon.attack = 30
    new_pokemon.defense = 10
    new_pokemon.speed = 20

    new_pokemon2.attack = 25
    new_pokemon2.defense = 8
    new_pokemon2.speed = 18

    response = client.post('/battle/survival', json={'pokemon1_id': new_pokemon.id, 'pokemon2_id': new_pokemon2.id})
    assert response.status_code == 200
    assert response.json['message'] == f'{new_pokemon.name} wins the survival battle!'
    assert response.json['winner']['name'] == new_pokemon.name

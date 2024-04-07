# Pokemon Challenge API

This API allows you to manage and challenge Pokemon. Each Pokemon can have several skills and weaknesses.

## Installation

### Prerequisites

- Python 3.x
- pip

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/davidmm07/pkm_api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd pkm_api
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - **Windows:**

        ```bash
        .\venv\Scripts\activate
        ```

    - **macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

5. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```
### Required packages(there is also in the requirements)    
    ```bash
    pip install Flask-Migrate
    ```

    ```bash
    pip install SQLAlchemy
    ```
## Database Migration

### Initialize Database

1. Set the `FLASK_APP` environment variable:

    ```bash
    export FLASK_APP=app
    ```

    - **Windows:**

        ```bash
        set FLASK_APP=app
        ```

2. Create the database and apply migrations:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Testing

### Run Tests with Coverage

1. Run the tests:

    ```bash
    pytest
    ```

2. View the coverage report:

    Open `htmlcov/index.html` in a web browser.

## API Usage

### Create a Pokemon

```bash
curl -X POST http://127.0.0.1:5000/pokemon -H "Content-Type: application/json" -d '{
    "name": "Charmander",
    "attack": 35,
    "defense": 15,
    "speed": 40,
    "hp": 100,
    "skills": ["Ember", "Scratch"],
    "weaknesses": ["Water"]
}'
```

### Get a Pokemon
```bash
curl http://127.0.0.1:5000/pokemon/1

```
### Update a Pokemon

```bash
curl -X PUT http://127.0.0.1:5000/pokemon/1 -H "Content-Type: application/json" -d '{
    "name": "Charmander",
    "attack": 40,
    "defense": 20,
    "speed": 50,
    "hp": 120,
    "skills": ["Flamethrower", "Slash"],
    "weaknesses": ["Water", "Rock"]
}'
```
### Delete a Pokemon
```bash
curl -X DELETE http://127.0.0.1:5000/pokemon/1


```
### List all Pokemon
```bash
curl http://127.0.0.1:5000/pokemon

```
### Filter Pokemon by Name
```bash
curl http://127.0.0.1:5000/pokemon?name=Charmander


```
### Filter Pokemon by Skill
```bash
curl http://127.0.0.1:5000/pokemon?skill=Ember

```
### Filter Pokemon by Weakness
```bash
curl http://127.0.0.1:5000/pokemon?weakness=Water

```

### Start a Survival Mode Battle

```bash
curl -X POST http://127.0.0.1:5000/pokemon/survival -H "Content-Type: application/json" -d '{
    "pokemon1_id": 1,
    "pokemon2_id": 2
}'
```
### Start a Battle Mode Battle

```bash
curl -X POST http://127.0.0.1:5000/pokemon/battle -H "Content-Type: application/json" -d '{
    "pokemon1_id": 1,
    "pokemon2_id": 2
}'

```

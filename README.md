# Superhero API

A Flask RESTful API for tracking superheroes and their superpowers.  
This API allows you to manage `Heroes`, `Powers`, and the `HeroPower` association linking them with specific strengths.

---

## Table of Contents

- [Features](#features)  
- [Models](#models)  
- [Routes](#routes)  
- [Example Requests & Responses](#example-requests--responses)  
- [Setup](#setup)  
- [Testing](#testing)  

---

## Features

- Manage heroes and their superpowers.
- Assign powers to heroes with strength levels: `Strong`, `Weak`, or `Average`.
- Validations:
  - `Power.description` must be present and at least 20 characters.
  - `HeroPower.strength` must be one of `Strong`, `Weak`, or `Average`.
- Full CRUD for powers (GET, PATCH) and creation of hero-power associations (POST).

---

## Models

### Hero

| Field       | Type   |
|------------|--------|
| `id`      | Integer (Primary Key) |
| `name`    | String |
| `super_name` | String |

- Relationship: `hero_powers` (one-to-many)
- Association proxy: `powers` (many-to-many through HeroPower)

---

### Power

| Field       | Type   |
|------------|--------|
| `id`      | Integer (Primary Key) |
| `name`    | String |
| `description` | String (min 20 characters) |

- Relationship: `hero_powers` (one-to-many)
- Association proxy: `heroes` (many-to-many through HeroPower)

---

### HeroPower

| Field       | Type   |
|------------|--------|
| `id`      | Integer (Primary Key) |
| `strength`| String (`Strong`, `Weak`, `Average`) |
| `hero_id` | Foreign Key (Hero) |
| `power_id`| Foreign Key (Power) |

- Relationships: belongs to `Hero` and `Power`.

---

## Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/heroes` | List all heroes |
| GET    | `/heroes/<id>` | Get hero by ID with powers |
| GET    | `/powers` | List all powers |
| GET    | `/powers/<id>` | Get power by ID |
| PATCH  | `/powers/<id>` | Update a power’s description |
| POST   | `/hero_powers` | Create a HeroPower association |

---

## Example Requests & Responses

### PATCH /powers/:id

**Request Body:**
json
```
{
  "description": "Gives the wielder super-human agility and speed."
}
```

**Successful Response:**
json
```
{
  "id": 1,
  "name": "super strength",
  "description": "Gives the wielder super-human agility and speed."
}
```

**Error Response (Power not found):**
json
```
{
  "error": "Power not found"
}
```

**Validation Error Response:**
```
{
  "errors": ["Description must be 20 characters or longer"]
}
```

### POST /hero_powers
**Request Body:**
json
```
{
  "strength": "Average",
  "power_id": 1,
  "hero_id": 3
}
```

**Successful Response:**
json
```
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
}
```

**Validation Error Response:**
json
```
{
  "errors": ["strength must be Strong, Weak, or Average"]
}
```

## Setup

1. Clone the repository:
bash
```
Copy code
git clone <repo-url>
cd <repo-folder>
```

2. Create a virtual environment:
bash
```
python3 -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
bash
```
pip install -r requirements.txt
```

4. Initialize the database:
bash
```
flask db init
flask db migrate
flask db upgrade
```

5. Seed the database :
bash
```
python seed.py
```

6. Run the Flask server:
```
python app.py
```
#### API available at: http://127.0.0.1:5555

## Author

This project was created by Dev. Dan Rotich

## License

This project is open source and is available for educational purposes



# Full Stack Users App
Flask + SQLite + HTML/CSS/JS

## Project Structure

```
fullstack-app/
├── app.py               ← Flask backend (API + routing)
├── database.db          ← SQLite database (auto-created)
├── requirements.txt     ← Python dependencies
├── templates/
│   └── index.html       ← Frontend HTML (served by Flask)
└── static/
    ├── style.css        ← Styles
    └── app.js           ← Frontend JavaScript (fetch calls)
```

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python app.py

# 3. Open browser
http://localhost:5000
```

## API Endpoints

| Method | URL            | Description        |
|--------|----------------|--------------------|
| GET    | /users         | Get all users      |
| GET    | /users/<id>    | Get one user       |
| POST   | /add-user      | Create a new user  |
| DELETE | /users/<id>    | Delete a user      |

## POST /add-user — Request body

```json
{
  "name":  "Ahmed Hassan",
  "email": "ahmed@example.com"
}
```

## Flow

User → index.html → app.js → fetch() → Flask → SQLite → JSON → DOM
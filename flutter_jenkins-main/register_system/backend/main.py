from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# CORS supaya Flutter Web bisa akses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# database
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT
)
""")

class User(BaseModel):
    username: str
    email: str
    password: str

@app.post("/register")
def register(user: User):

    cursor.execute(
        "INSERT INTO users(username,email,password) VALUES(?,?,?)",
        (user.username, user.email, user.password)
    )

    conn.commit()

    return {"message": "User registered successfully"}
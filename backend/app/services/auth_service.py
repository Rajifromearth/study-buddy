import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..models.user import User
from .note_service import DATABASE_PATH

load_dotenv(Path(__file__).resolve().parents[2] / '.env')
JWT_SECRET = os.getenv('JWT_SECRET')
if not JWT_SECRET:
    JWT_SECRET = 'study-buddy-dev-only-secret-change-me'
    print('WARNING: JWT_SECRET is not set; using an insecure development default.')

ALGORITHM = 'HS256'
TOKEN_EXPIRES_HOURS = 24
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def _connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    return connection


def _user(row: sqlite3.Row) -> User:
    return User(id=row['id'], email=row['email'], created_at=row['created_at'])


def create_user(email: str, password: str) -> User:
    normalized_email = email.strip().lower()
    with _connection() as connection:
        existing = connection.execute('SELECT id FROM users WHERE email = ?', (normalized_email,)).fetchone()
        if existing:
            raise ValueError('An account with this email already exists.')
        user = User(id=str(uuid4()), email=normalized_email, created_at=datetime.now(timezone.utc).isoformat())
        connection.execute('INSERT INTO users (id, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
            (user.id, user.email, password_context.hash(password), user.created_at))
    return user


def authenticate_user(email: str, password: str) -> User | None:
    with _connection() as connection:
        row = connection.execute('SELECT * FROM users WHERE email = ?', (email.strip().lower(),)).fetchone()
    if not row or not password_context.verify(password, row['password_hash']):
        return None
    return _user(row)


def get_user_by_id(user_id: str) -> User | None:
    with _connection() as connection:
        row = connection.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return _user(row) if row else None


def create_access_token(user_id: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRES_HOURS)
    return jwt.encode({'sub': user_id, 'exp': expires_at}, JWT_SECRET, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload.get('sub')
    except JWTError:
        return None

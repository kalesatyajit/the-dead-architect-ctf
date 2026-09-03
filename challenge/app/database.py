import sqlite3
from pathlib import Path

from werkzeug.security import generate_password_hash


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    year INTEGER NOT NULL,
    genre TEXT NOT NULL,
    description TEXT NOT NULL,
    cover_color TEXT NOT NULL,
    featured INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'public',
    studio_note TEXT NOT NULL DEFAULT ''
);
"""

SAMPLE_USERS = [("architect", generate_password_hash("demo-only"))]
SAMPLE_PROJECTS = [
    (
        "glass-cities",
        "Glass Cities",
        "Mara Venn",
        2025,
        "Post-industrial ambient",
        "A precise, nocturnal study in fractured piano, tape hiss, and rooms that seem to remember their occupants.",
        "#d35d45",
        1,
        "public",
        "Mastered at Northline, February 2025.",
    ),
    (
        "soft-machines",
        "Soft Machines",
        "Northline",
        2024,
        "Textural electronica",
        "Warm circuits and slow-motion percussion assembled for late train rides and empty control rooms.",
        "#4f8f8c",
        1,
        "public",
        "A live modular performance edited into a concise studio cut.",
    ),
    (
        "after-the-signal",
        "After the Signal",
        "Ilya Kade",
        2023,
        "Cinematic downtempo",
        "Low-lit synths, close-mic'd strings, and a pulse built to carry a story past its final frame.",
        "#b58a4b",
        0,
        "public",
        "Available for licensing inquiries.",
    ),
    (
        "the-quiet-engine",
        "The Quiet Engine",
        "Architect",
        2022,
        "Unfinished archive",
        "A private workprint assembled from room tone, clockwork percussion, and a melody that never resolves.",
        "#7d7468",
        0,
        "private",
        "The index says: the old workshop keeps its own history. Mirror path: /archive/architect-notes.git. The phrase in the margin is 'rooms remember twice'.",
    ),
    (
        "blue-hour-protocol",
        "Blue Hour Protocol",
        "Sable Index",
        2021,
        "Electroacoustic",
        "A restrained study in granular light and the mechanical rhythm of an empty building.",
        "#586b81",
        0,
        "private",
        "Catalogued, but never released.",
    ),
    (
        "signal-bloom",
        "Signal Bloom",
        "Mara Venn",
        2020,
        "Ambient pop",
        "A small, bright collection of field recordings and patient harmonic movement.",
        "#9b6553",
        0,
        "public",
        "The first public commission from the studio.",
    ),
    (
        "night-index",
        "Night Index",
        "Northline",
        2019,
        "Minimal electronics",
        "A skeletal record of clicks, low voltage, and distant voices reduced to texture.",
        "#65715e",
        0,
        "public",
        "Archived from the original control-room sessions.",
    ),
    (
        "unfinished-sun",
        "Unfinished Sun",
        "Ilya Kade",
        2018,
        "Cinematic ambient",
        "The earliest surviving collaboration in the Architect catalog.",
        "#a17b55",
        0,
        "private",
        "Artwork pending approval.",
    ),
]


def get_db(database_path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(database_path: str) -> None:
    Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    with get_db(database_path) as connection:
        connection.executescript(SCHEMA)
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(projects)").fetchall()
        }
        if "status" not in columns:
            connection.execute(
                "ALTER TABLE projects ADD COLUMN status TEXT NOT NULL DEFAULT 'public'"
            )
        if "studio_note" not in columns:
            connection.execute(
                "ALTER TABLE projects ADD COLUMN studio_note TEXT NOT NULL DEFAULT ''"
            )
        connection.executemany(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            SAMPLE_USERS,
        )
        connection.executemany(
            """INSERT OR IGNORE INTO projects
            (slug, title, artist, year, genre, description, cover_color, featured,
             status, studio_note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            SAMPLE_PROJECTS,
        )

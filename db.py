"""
Zugriff auf die Datenbank (SQLite).

Alle SQL-Befehle gehören in diese Datei. app.py ruft nur Funktionen von hier auf.
"""
import concurrent.futures
import sqlite3
from pathlib import Path

from flask import current_app, g


def verbindung() -> sqlite3.Connection:
    """Eine Verbindung pro Anfrage, wird am Ende der Anfrage automatisch geschlossen."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row  # Zeilen wie Dictionaries: zeile["name"]
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def schliessen(_fehler=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def tabellen_anlegen():
    """Führt schema.sql aus."""
    schema = (Path(__file__).parent / "schema.sql").read_text(encoding="utf-8")
    verbindung().executescript(schema)


def sqlite_version() -> str:
    return verbindung().execute("SELECT sqlite_version()").fetchone()[0]

# UC1 (Salome)

# Diese Funktion gibt die offene Datenbankverbindung zurück
# SELECT id, number, name FROM project holt diese drei Spalten
# ORDER BY sortiert nach Projektnummer.
# .fetchall() holt alle gefundenen Zeilen auf einmal als Liste
def get_all_projects() -> list[sqlite3.Row]:
    """Return all projects, sorted by project number.""" # Docstring habe ich gelernt :-)
    return verbindung().execute(
        "SELECT id, number, name FROM project ORDER BY number"
    ).fetchall()

# Bekommt Nummer und Name als Text und gibt True oder False zurück.
# (app.py muss so nichts über SQL wissen, sondern kann einfach nur fragen, ob es geklappt hat)
def create_project(number: str, name: str) -> bool:
    """
    Save a new project.
    Return True if it was saved,
    and False if the project number already exists.
    """
    con = verbindung()
    try:
        # Die ? sind Platzhalter
        con.execute(
            "INSERT INTO project (number, name) VALUES (?, ?)",
            (number, name),
        )
        con.commit() # Änderung fixen, sonst geht sie beim Schliessen verloren
        return True
    except sqlite3.IntegrityError:
        # Wird geworfen wenn UNIQUE nicht eingehalten wird also die Nummer schon existiert
        return False
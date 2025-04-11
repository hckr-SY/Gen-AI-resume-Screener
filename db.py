# db.py

import sqlite3
import os

DB_PATH = "data/jobmatch.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        education TEXT,
        experience TEXT,
        certifications TEXT,      
        achievements TEXT,        
        file_name TEXT UNIQUE
    )
    ''')

    conn.commit()
    conn.close()


def insert_candidate(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    skills = ", ".join(data.get("skills", []))
    education = "; ".join([f'{e.get("degree", "")} in {e.get("field", "")}' for e in data.get("education", [])])
    experience = "; ".join([f'{e.get("role", "")} at {e.get("company", "")} ({e.get("duration", "")})' for e in data.get("experience", [])])
    certifications = ", ".join(data.get("certifications", []))
    achievements = "; ".join(data.get("achievements", []))

    c.execute('''
        INSERT OR IGNORE INTO candidates (
            name, email, phone, skills, education, experience,
            certifications, achievements, file_name
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get("name"), data.get("email"), data.get("phone"),
        skills, education, experience, certifications, achievements,
        data.get("file")
    ))

    conn.commit()
    conn.close()


def candidate_exists(file_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM candidates WHERE file_name = ?", (file_name,))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_incomplete_candidates():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT file_name FROM candidates
        WHERE 
            skills IS NULL OR skills = ''
            OR education IS NULL OR education = ''
            OR experience IS NULL OR experience = ''
    """)
    results = c.fetchall()
    conn.close()
    return [row[0] for row in results]

def update_candidate(file_name, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    skills = ", ".join(data.get("skills", []))
    education = "; ".join([f'{e.get("degree", "")} in {e.get("field", "")}' for e in data.get("education", [])])
    experience = "; ".join([f'{e.get("role", "")} at {e.get("company", "")} ({e.get("duration", "")})' for e in data.get("experience", [])])
    certifications = ", ".join(data.get("certifications", []))
    achievements = "; ".join(data.get("achievements", []))

    c.execute('''
        UPDATE candidates SET
            name = ?, email = ?, phone = ?, skills = ?, education = ?, experience = ?,
            certifications = ?, achievements = ?
        WHERE file_name = ?
    ''', (
        data.get("name"), data.get("email"), data.get("phone"),
        skills, education, experience, certifications, achievements,
        file_name
    ))

    conn.commit()
    conn.close()




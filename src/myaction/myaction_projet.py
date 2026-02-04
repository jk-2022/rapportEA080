import asyncio
import os
from dataclasses import dataclass 
import sqlite3 
from mystorage import *

NAME_DB="rapport.db"


@dataclass
class Projet:
    id:int 
    name:str 
    title:str 
    secteurs: str
    created_at:str 

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

async def init_db():
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS projets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                title TEXT ,
                secteurs TEXT ,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP 
                )
    """)
    conn.commit()
    conn.close()

def load_all_projets():
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM projets ORDER BY created_at DESC").fetchall()
    return [Projet(*row) for row in rows]

def create_projet(name,title,secteurs):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO projets(name,title,secteurs) VALUES(?,?,?)", (name,title,secteurs))
    conn.commit()
    conn.close()

def update_projet(projet:Projet):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("UPDATE projets SET name=?, title=?, secteurs=? WHERE id=?", (projet.name,projet.title,projet.secteurs,projet.id))
    conn.commit()
    conn.close()

def delete_projet(projet_id:int):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM projets  WHERE id=?", (projet_id,))
    conn.commit()
    conn.close()
    return True



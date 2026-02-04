from dataclasses import dataclass 
import sqlite3 
import os

import flet as ft

from mystorage import get_value 

NAME_DB="rapport.db"


@dataclass
class Entreprise:
    id:int 
    name:str 
    contact:str 
    created_at : str

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

async def init_db_entreprise():
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS entreprises(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
    """)
    conn.commit()
    conn.close()

def load_all_entreprises():
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM entreprises ORDER BY created_at DESC").fetchall()
    return [Entreprise(*row) for row in rows]

def create_entreprise(name,contact):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO entreprises(name,contact) VALUES(?,?)", (name, contact))
    conn.commit()
    conn.close()

def update_entreprise(entreprise:Entreprise):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("UPDATE entreprises SET name=?, contact=? WHERE id=?", (entreprise.name,entreprise.contact, entreprise.id))
    conn.commit()
    conn.close()

def delete_entreprise(entreprise_id:int):
    # print('delete')
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM entreprises  WHERE id=?", (entreprise_id,))
    conn.commit()
    conn.close()
    return True



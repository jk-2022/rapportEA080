from dataclasses import dataclass 
import sqlite3 
import os

import flet as ft

from mystorage import get_value 

NAME_DB="rapport.db"


@dataclass
class Village:
    id : int
    prefecture: str
    commune: str
    canton: str
    localite: str
    coordonnee_x: float
    coordonnee_y: float
    ressource: str
    status: str
    observation: str
    created_at: str

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

async def init_db_village():
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS villages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prefecture TEXT, 
                commune TEXT, 
                canton TEXT, 
                localite TEXT, 
                coordonnee_x REAL, 
                coordonnee_y REAL,
                ressource TEXT, 
                status TEXT,
                observation TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
    """)
    conn.commit()
    conn.close()

def load_all_villages():
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM villages ORDER BY created_at DESC").fetchall()
    return [Village(*row) for row in rows]

def load_one_village(village_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM villages WHERE id=?", (village_id,)).fetchall()
    if rows:
        col_names = [description[0] for description in cur.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data
    return rows

def create_village(prefecture, commune, canton, localite, coordonnee_x, coordonnee_y, ressource,  status, observation):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO villages( prefecture, commune, canton, localite, coordonnee_x, coordonnee_y, ressource,  status,  observation) VALUES(?,?,?,?,?,?,?,?,?)", (prefecture, commune, canton, localite, coordonnee_x, coordonnee_y,ressource,  status, observation))
    conn.commit()
    conn.close()

def update_village(village:Village):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("UPDATE villages SET prefecture=?, commune=?, canton=?, localite=?, coordonnee_x=?, coordonnee_y=?,ressource=?, status=?, observation=? WHERE id=?", ( village.prefecture,village.commune,village.canton,village.localite,village.coordonnee_x,village.coordonnee_y,village.ressource,village.status, village.observation,village.id))
    conn.commit()
    conn.close()

def delete_village(village_id:int):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM villages  WHERE id=?", (village_id,))
    conn.commit()
    conn.close()
    return True



from dataclasses import dataclass 
import sqlite3 
import os

import flet as ft

from mystorage import get_value 

NAME_DB="rapport.db"


@dataclass
class Panne:
    id : int
    ouvrage_id :int
    date_signaler :str
    description :str
    solution :str
    observation :str
    created_at : str
   

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

async def init_db_panne():
    conn=connected_db()
    cur=conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS panne(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ouvrage_id INTEGER NOT NULL,
            date_signaler TEXT,
            description TEXT,
            solution TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ouvrage_id) REFERENCES ouvrages(id)
            )
        ''')
    conn.commit()
    conn.close()

def load_all_pannes(ouvrage_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM panne WHERE ouvrage_id=? ORDER BY created_at DESC", (ouvrage_id,)).fetchall()
    return [Panne(*row) for row in rows]

def load_one_panne(panne_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM panne WHERE id=?", (panne_id,)).fetchall()
    if rows:
        col_names = [description[0] for description in cur.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data
    return rows

def create_panne(ouvrage_id,date_signaler, description, solution, observation):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO panne(ouvrage_id, date_signaler, description, solution, observation) VALUES(?,?,?,?,?)", (ouvrage_id,date_signaler, description, solution,observation))
    conn.commit()
    conn.close()

def update_panne(panne:Panne):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("UPDATE panne SET ouvrage_id=?, date_signaler=?, description=?, solution=?=?, observation=? WHERE id=?", (panne.ouvrage_id, panne.date_signaler, panne.description, panne.solution, panne.observation, panne.id))
    conn.commit()
    conn.close()

def delete_panne(panne_id:int):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM panne  WHERE id=?", (panne_id,))
    conn.commit()
    conn.close()
    return True



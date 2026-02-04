from dataclasses import dataclass 
import sqlite3 
import os

import flet as ft

from mystorage import get_value 

storage_paths = ft.StoragePaths()

DB_PATH= storage_paths.get_application_documents_directory

NAME_DB="rapport.db"


@dataclass
class Suivi:
    id : int
    ouvrage_id :int
    date_reception :str
    type_reception :str
    participants :str
    recommandation :str
    observation :str
    created_at :str
   

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

async def init_db_suivi():
    conn=connected_db()
    cur=conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS suivi(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ouvrage_id INTEGER NOT NULL,
            date_reception TEXT,
            type_reception TEXT,
            participants TEXT,
            recommandation TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ouvrage_id) REFERENCES ouvrages(id)
            )
        ''')
    conn.commit()
    conn.close()

def load_all_suivis(ouvrage_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM suivi WHERE ouvrage_id=? ORDER BY created_at DESC", (ouvrage_id,)).fetchall()
    return [Suivi(*row) for row in rows]

def load_one_suivi(suivi_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM suivi WHERE id=?", (suivi_id,)).fetchall()
    if rows:
        col_names = [description[0] for description in cur.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data
    return rows

def create_suivi(ouvrage_id,date_reception, type_reception, participants, recommandation, observation):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO suivi(ouvrage_id, date_reception, type_reception, participants, recommandation, observation) VALUES(?,?,?,?,?,?)", (ouvrage_id,date_reception, type_reception, participants, recommandation,observation))
    conn.commit()
    conn.close()

def update_suivi(suivi:Suivi):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("UPDATE suivi SET ouvrage_id=?, date_reception=?, type_reception=?, participants=?, recommandation=?, observation=? WHERE id=?", (suivi.ouvrage_id, suivi.date_reception,suivi.type_reception,suivi.participants,suivi.recommandation,suivi.observation, suivi.id))
    conn.commit()
    conn.close()

def delete_suivi(suivi_id:int):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM suivi  WHERE id=?", (suivi_id,))
    conn.commit()
    conn.close()
    return True



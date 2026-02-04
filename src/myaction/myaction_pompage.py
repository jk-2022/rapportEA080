from dataclasses import dataclass 
import sqlite3 
import os

import flet as ft

from mystorage import get_value 

NAME_DB="rapport.db"


@dataclass
class Pompage:
    id : int
    ouvrage_id :int
    date_pompage :str
    type_pompe :str
    cote_pompe :str
    temps_pompage :str
    debit_pompage :str
    niv_dynamique :str
    niv_statique :str
    observation :str
    created_at :str
   

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

async def init_db_pompage():
    conn=connected_db()
    cur=conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS pompage(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ouvrage_id INTEGER NOT NULL,
            date_pompage TEXT,
            type_pompe TEXT,
            cote_pompe TEXT,
            temps_pompage TEXT,
            debit_pompage TEXT,
            niv_dynamique TEXT,
            niv_statique TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ouvrage_id) REFERENCES ouvrages(id)
            )
        ''')
    conn.commit()
    conn.close()

# def load_all_pompage(projet_id):
#     conn=connected_db()
#     cur=conn.cursor()
#     rows=cur.execute(" SELECT * FROM pompage WHERE id=? ORDER BY created_at DESC", (projet_id,)).fetchall()
#     return [Pompage(*row) for row in rows]

def load_one_pompage(ouvrage_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM pompage WHERE ouvrage_id=?", (ouvrage_id,)).fetchall()
    if rows:
        col_names = [description[0] for description in cur.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data
    return rows

def create_pompage(ouvrage_id,date_pompage, type_pompe, cote_pompe, temps_pompage, debit_pompage, niv_dynamique, niv_statique, observation):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO pompage(ouvrage_id, date_pompage, type_pompe, cote_pompe, temps_pompage, debit_pompage, niv_dynamique, niv_statique, observation) VALUES(?,?,?,?,?,?,?,?,?)", (ouvrage_id,date_pompage, type_pompe, cote_pompe, temps_pompage, debit_pompage, niv_dynamique, niv_statique,observation))
    conn.commit()
    conn.close()

def update_pompage(pompage:Pompage):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("UPDATE pompage SET ouvrage_id=?, date_pompage=?, type_pompe=?, cote_pompe=?, temps_pompage=?, debit_pompage=?, niv_dynamique=?, niv_statique=?, observation=? WHERE id=?", (pompage.ouvrage_id, pompage.date_pompage,pompage.type_pompe,pompage.cote_pompe,pompage.temps_pompage,pompage.debit_pompage,pompage.niv_dynamique,pompage.niv_statique,pompage.observation, pompage.id))
    conn.commit()
    conn.close()

def delete_pompage(pompage_id:int):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM pompage  WHERE id=?", (pompage_id,))
    conn.commit()
    conn.close()
    return True



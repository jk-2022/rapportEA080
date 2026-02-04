from dataclasses import dataclass 
import sqlite3 
import os

import flet as ft

from mystorage import get_value 

NAME_DB="rapport.db"


@dataclass
class Foration:
    id : int
    ouvrage_id :int
    date_foration :str
    prof_alteration :str
    prof_socle :str
    prof_total :str
    prof_tube_plein :str
    prof_tube_crepine :str
    debit_soufflage :str
    observation :str
    created_at :str
   

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

async def init_db_foration():
    conn=connected_db()
    cur=conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS foration(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ouvrage_id INTEGER NOT NULL,
            date_foration TEXT,
            prof_alteration TEXT,
            prof_socle TEXT,
            prof_total TEXT,
            prof_tube_crepine TEXT,
            prof_tube_plein TEXT,
            debit_soufflage TEXT,
            observation TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ouvrage_id) REFERENCES ouvrage(id)
            )
        ''')
    conn.commit()
    conn.close()

def load_one_foration(ouvrage_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM foration WHERE ouvrage_id=?", (ouvrage_id,)).fetchall()
    if rows:
        col_names = [description[0] for description in cur.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data
    return rows

def create_foration(ouvrage_id,date_foration, prof_alteration, prof_socle, prof_total, prof_tube_crepine, prof_tube_plein, debit_soufflage, observation):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO foration(ouvrage_id, date_foration, prof_alteration, prof_socle, prof_total, prof_tube_crepine, prof_tube_plein, debit_soufflage, observation) VALUES(?,?,?,?,?,?,?,?,?)", (ouvrage_id,date_foration, prof_alteration, prof_socle, prof_total, prof_tube_crepine, prof_tube_plein, debit_soufflage,observation))
    conn.commit()
    conn.close()

def update_foration(foration:Foration):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("UPDATE foration SET ouvrage_id=?, date_foration=?, prof_alteration=?, prof_socle=?, prof_total=?, prof_tube_crepine=?, prof_tube_plein=?, debit_soufflage=?, observation=? WHERE id=?", (foration.ouvrage_id, foration.date_foration,foration.prof_alteration,foration.prof_socle,foration.prof_total,foration.prof_tube_crepine,foration.prof_tube_plein,foration.debit_soufflage,foration.observation, foration.id))
    conn.commit()
    conn.close()

def delete_foration(foration_id:int):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM foration  WHERE id=?", (foration_id,))
    conn.commit()
    conn.close()
    return True



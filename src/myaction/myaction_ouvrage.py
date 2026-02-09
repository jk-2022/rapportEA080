from dataclasses import dataclass 
import sqlite3 
import os

import flet as ft

from mystorage import get_value 

NAME_DB="rapport.db"


@dataclass
class Ouvrage:
    id : int
    projet_id : int
    prefecture: str
    commune: str
    canton: str
    localite: str
    lieu: str
    coordonnee_x: float
    coordonnee_y: float
    entreprise: str
    type_ouvrage: str
    numero_irh: str
    annee : int
    type_energie: str
    type_reservoir: str
    volume_reservoir :float
    etat: str
    cause_panne: str
    observation: str
    created_at: str
    def to_dict(self):
        return {
        "id":self.id,
        "projet_id":self.projet_id,
        "prefecture":self.prefecture,
        "commune":self.commune,
        "canton":self.canton,
        "localite":self.localite,
        "lieu":self.lieu,
        "coordonnee_x":self.coordonnee_x,
        "coordonnee_y":self.coordonnee_y,
        "entreprise":self.entreprise,
        "type_ouvrage":self.type_ouvrage,
        "numero_irh":self.numero_irh,
        "annee":self.annee,
        "type_energie":self.type_energie,
        "type_reservoir": self.type_reservoir,
        "volume_reservoir": self.volume_reservoir,
        "etat": self.etat,
        "cause_panne": self.cause_panne,
        "observation": self.observation,
        }
    def to_dict_other(self):
        return {
        "commune":self.commune,
        "canton":self.canton,
        "localite":self.localite,
        "lieu":self.lieu,
        "coordonnee_x":self.coordonnee_x,
        "coordonnee_y":self.coordonnee_y,
        "entreprise":self.entreprise,
        }

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

async def init_db_ouvrage():
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS ouvrages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                projet_id INTEGER,
                prefecture TEXT, 
                commune TEXT, 
                canton TEXT, 
                localite TEXT, 
                lieu TEXT, 
                coordonnee_x REAL, 
                coordonnee_y REAL,
                entreprise TEXT, 
                type_ouvrage TEXT, 
                numero_irh REAL, 
                annee TEXT, 
                type_energie TEXT, 
                type_reservoir TEXT,
                volume_reservoir TEXT, 
                etat TEXT, 
                cause_panne TEXT,
                observation TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (projet_id) REFERENCES projets(id)
                )
    """)
    conn.commit()
    conn.close()

def load_all_ouvrages(projet_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM ouvrages WHERE projet_id=? ORDER BY created_at DESC", (projet_id,)).fetchall()
    return [Ouvrage(*row) for row in rows]

def load_one_ouvrage(ouvrage_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM ouvrages WHERE id=?", (ouvrage_id,)).fetchall()
    if rows:
        col_names = [description[0] for description in cur.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data
    return rows

def create_ouvrage(projet_id,prefecture, commune, canton, localite, lieu, coordonnee_x, coordonnee_y,entreprise, type_ouvrage, numero_irh, annee, type_energie, type_reservoir,volume_reservoir, etat, cause_panne,observation):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO ouvrages(projet_id, prefecture, commune, canton, localite, lieu, coordonnee_x, coordonnee_y,entreprise, type_ouvrage, numero_irh, annee, type_energie, type_reservoir,volume_reservoir, etat, cause_panne, observation) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (projet_id,prefecture, commune, canton, localite, lieu, coordonnee_x, coordonnee_y,entreprise, type_ouvrage, numero_irh, annee, type_energie, type_reservoir,volume_reservoir, etat, cause_panne,observation))
    conn.commit()
    conn.close()

def update_ouvrage(ouvrage:Ouvrage):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("UPDATE ouvrages SET projet_id=?, prefecture=?, commune=?, canton=?, localite=?, lieu=?, coordonnee_x=?, coordonnee_y=?,entreprise=?, type_ouvrage=?, numero_irh=?, annee=?, type_energie=?, type_reservoir=?,volume_reservoir=?, etat=?, cause_panne=?, observation=? WHERE id=?", (ouvrage.projet_id, ouvrage.prefecture,ouvrage.commune,ouvrage.canton,ouvrage.localite,ouvrage.lieu,ouvrage.coordonnee_x,ouvrage.coordonnee_y,ouvrage.entreprise,ouvrage.type_ouvrage,ouvrage.numero_irh,ouvrage.annee,ouvrage.type_energie,ouvrage.type_reservoir,ouvrage.volume_reservoir,ouvrage.etat,ouvrage.cause_panne, ouvrage.observation,ouvrage.id))
    conn.commit()
    conn.close()

def delete_ouvrage(ouvrage_id:int):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM ouvrages  WHERE id=?", (ouvrage_id,))
    conn.commit()
    conn.close()
    return True



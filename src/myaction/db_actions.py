# import asyncio
import os
from typing import Optional
from dataclasses import dataclass 
import sqlite3 
from mystorage import *

NAME_DB="rapport.db"

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

# ================================================
# ==============init DB===========================
# ================================================
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
    cur.execute("""
            CREATE TABLE IF NOT EXISTS entreprises(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
    """)
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

# ================================================
# ==============Projets===========================
# ================================================

@dataclass
class Projet:
    id:int 
    name:str 
    title:str 
    secteurs: str
    created_at:str 

def load_all_projets():
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM projets ORDER BY created_at DESC").fetchall()
    return [Projet(*row) for row in rows]

def load_one_projets(id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM projets WHERE id=?", (id,)).fetchall()
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

# ================================================
# ==============Ouvrages==========================
# ================================================

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
    suivi:str="autre"
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
        "suivi": self.suivi,
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
        "suivi":self.suivi,
        }

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

def load_all_ouvrages(projet_id:Optional[int]=None):
    conn=connected_db()
    cur=conn.cursor()
    if projet_id:
        rows=cur.execute(" SELECT * FROM ouvrages WHERE projet_id=? ORDER BY created_at DESC", (projet_id,)).fetchall()
    else:
        rows=cur.execute(" SELECT * FROM ouvrages ORDER BY created_at DESC").fetchall()
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

def get_one_ouvrage(ouvrage_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM ouvrages WHERE id=? ", (ouvrage_id,)).fetchall()
    return [Ouvrage(*row) for row in rows]

def create_ouvrage(projet_id,prefecture, commune, canton, localite, lieu, coordonnee_x, coordonnee_y,entreprise, type_ouvrage, numero_irh, annee, type_energie, type_reservoir,volume_reservoir, etat, cause_panne,observation,suivi):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO ouvrages(projet_id, prefecture, commune, canton, localite, lieu, coordonnee_x, coordonnee_y,entreprise, type_ouvrage, numero_irh, annee, type_energie, type_reservoir,volume_reservoir, etat, cause_panne, observation,suivi) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (projet_id,prefecture, commune, canton, localite, lieu, coordonnee_x, coordonnee_y,entreprise, type_ouvrage, numero_irh, annee, type_energie, type_reservoir,volume_reservoir, etat, cause_panne,observation,suivi))
    conn.commit()
    conn.close()

def update_ouvrage(ouvrage:Ouvrage):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("UPDATE ouvrages SET projet_id=?, prefecture=?, commune=?, canton=?, localite=?, lieu=?, coordonnee_x=?, coordonnee_y=?,entreprise=?, type_ouvrage=?, numero_irh=?, annee=?, type_energie=?, type_reservoir=?,volume_reservoir=?, etat=?, cause_panne=?, observation=?, suivi=? WHERE id=?", (ouvrage.projet_id, ouvrage.prefecture,ouvrage.commune,ouvrage.canton,ouvrage.localite,ouvrage.lieu,ouvrage.coordonnee_x,ouvrage.coordonnee_y,ouvrage.entreprise,ouvrage.type_ouvrage,ouvrage.numero_irh,ouvrage.annee,ouvrage.type_energie,ouvrage.type_reservoir,ouvrage.volume_reservoir,ouvrage.etat,ouvrage.cause_panne, ouvrage.observation,ouvrage.suivi, ouvrage.id))
    conn.commit()
    conn.close()

def delete_ouvrage(ouvrage_id:int):
    conn=connected_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM ouvrages  WHERE id=?", (ouvrage_id,))
    conn.commit()
    conn.close()
    return True

# ================================================
# ==============foration==========================
# ================================================

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
    
def load_all_forations(projet_id:Optional[int]=None):
    conn=connected_db()
    cur=conn.cursor()
    if projet_id:
        rows=cur.execute(" SELECT * FROM foration WHERE projet_id=? ORDER BY created_at DESC", (projet_id,)).fetchall()
    else:
        rows=cur.execute(" SELECT * FROM foration ORDER BY created_at DESC").fetchall()
    return [Foration(*row) for row in rows]

def load_one_foration(ouvrage_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM foration WHERE ouvrage_id=?", (ouvrage_id,)).fetchall()
    if rows:
        col_names = [description[0] for description in cur.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data[0]
    return {}

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

# ================================================
# ==============Pompages==========================
# ================================================

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


    
def load_all_pompages(projet_id:Optional[int]=None):
    conn=connected_db()
    cur=conn.cursor()
    if projet_id:
        rows=cur.execute(" SELECT * FROM pompage WHERE projet_id=? ORDER BY created_at DESC", (projet_id,)).fetchall()
    else:
        rows=cur.execute(" SELECT * FROM pompage ORDER BY created_at DESC").fetchall()
    return [Pompage(*row) for row in rows]

def load_one_pompage(ouvrage_id):
    conn=connected_db()
    cur=conn.cursor()
    rows=cur.execute(" SELECT * FROM pompage WHERE ouvrage_id=?", (ouvrage_id,)).fetchall()
    if rows:
        col_names = [description[0] for description in cur.description]
        data = [dict(zip(col_names, row)) for row in rows]
        return data[0]
    return {}

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

# ================================================
# ==============Pannes============================
# ================================================

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


# def load_all_pannes(ouvrage_id):
#     conn=connected_db()
#     cur=conn.cursor()
#     rows=cur.execute(" SELECT * FROM panne WHERE ouvrage_id=? ORDER BY created_at DESC", (ouvrage_id,)).fetchall()
#     return [Panne(*row) for row in rows]

def load_all_pannes(ouvrage_id:Optional[int]=None):
    conn=connected_db()
    cur=conn.cursor()
    if ouvrage_id:
        rows=cur.execute(" SELECT * FROM panne WHERE ouvrage_id=? ORDER BY created_at DESC", (ouvrage_id,)).fetchall()
    else:
        rows=cur.execute(" SELECT * FROM panne ORDER BY created_at DESC").fetchall()
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

# ================================================
# ==============Suivis============================
# ================================================

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

def load_all_suivis(ouvrage_id:Optional[int]=None):
    conn=connected_db()
    cur=conn.cursor()
    if ouvrage_id:
        rows=cur.execute(" SELECT * FROM suivi WHERE ouvrage_id=? ORDER BY created_at DESC", (ouvrage_id,)).fetchall()
    else:
        rows=cur.execute(" SELECT * FROM suivi ORDER BY created_at DESC").fetchall()
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

# ================================================
# ==============entreprise========================
# ================================================

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

# ================================================
# ==============Villages==========================
# ================================================

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


# ===========================================================
# ================= Actions Bases ===========================
# ===========================================================

async def ajouter_colonne_si_absente():
    conn = connected_db()
    cursor = conn.cursor()
    # Récupérer les colonnes existantes
    cursor.execute("PRAGMA table_info(ouvrages);")
    colonnes = [col[1] for col in cursor.fetchall()]
    # Vérifier si "suivi" existe
    if "suivi" not in colonnes:
        cursor.execute(
            "ALTER TABLE ouvrages ADD COLUMN suivi TEXT DEFAULT 'autre';"
        )
        conn.commit()
        print("Colonne 'suivi' ajoutée.")
    else:
        print("Colonne 'suivi' existe déjà.")

    conn.close()


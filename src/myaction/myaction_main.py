import os
import json
import sqlite3
from collections import defaultdict
import sqlite3 

from mystorage import get_value 

NAME_DB="rapport.db"

def connected_db():
    base_path=get_value("base_path")
    BASEDB_PATH=os.path.join(base_path,NAME_DB)
    return sqlite3.connect(BASEDB_PATH, check_same_thread=False)

def load_all_data(ouvrage_id):
    conn = connected_db()
    c=conn.cursor()
    all_data={
        'ouvrages':[],
        'foration':[],
        'pompage':[]
    }
    c.execute(f"SELECT * FROM ouvrages WHERE id=?",(ouvrage_id,))
    rows = c.fetchall()
    col_names = [description[0] for description in c.description]
    data = [dict(zip(col_names, row)) for row in rows]
    all_data["ouvrages"]=data
    tables=['foration', 'pompage']
    for table in tables:
        c.execute(f"SELECT * FROM {table} WHERE ouvrage_id=?",(ouvrage_id,))
        rows = c.fetchall()
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in rows]
        all_data[table]=data
    return all_data

def recuperer_one_local(ouvrage_id):
    conn = connected_db()
    c = conn.cursor()
    c.execute(""" SELECT * FROM ouvrages WHERE id=? """, (ouvrage_id,))
    ouvrage = c.fetchall()
    if ouvrage:
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in ouvrage]
        return data
    return ouvrage

def recuperer_projet_id(name):
    conn = connected_db()
    c = conn.cursor()
    c.execute(""" SELECT id FROM projets WHERE name=? """,(name,))
    projet_id = c.fetchone()
    return projet_id[0]

def recuperer_one_projet(projet_id):
    conn = connected_db()
    c = conn.cursor()
    c.execute(""" SELECT * FROM projets WHERE id=? """, (projet_id,))
    projet = c.fetchall()
    if projet:
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in projet]
        return data
    return projet

def recuperer_projet_name(projet_id):
    conn = connected_db()
    c = conn.cursor()
    c.execute(""" SELECT name FROM projets WHERE id=? """,(projet_id,))
    projet_name = c.fetchone()
    # print(type(projet_name[0]))
    return projet_name[0]


def recuperer_liste_ouvrage_by_projet(projet_id):
    conn = connected_db()
    try:
        c = conn.cursor()
        c.execute(""" SELECT * FROM ouvrage WHERE projet_id=? ORDER BY created_at DESC """, (projet_id,))
        ouvrages = c.fetchall()
        if ouvrages:
            col_names = [description[0] for description in c.description]
            data = [dict(zip(col_names, row)) for row in ouvrages]
            return data
        return ouvrages
    except Exception as e:
        print(e)

def get_all_projets():
    conn = connected_db()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM projets ORDER BY created_at DESC
    """)
    projets = c.fetchall()
    if projets:
        col_names = [description[0] for description in c.description]
        data = [dict(zip(col_names, row)) for row in projets]
        return data
    conn.close()
    return projets


def get_all_localites(projet_id):
    conn = connected_db()
    try:
        c = conn.cursor()
        c.execute(""" SELECT localite FROM ouvrages WHERE projet_id=? ORDER BY created_at DESC """, (projet_id,))
        localites = c.fetchall()
        return localites
    except Exception as e:
        print(e)

def get_filtered_ouvrages(type_ouvrage=None, 
                          localite=None, 
                          etat=None, 
                          numero_irh=None, 
                          projet_id=None):
    conn = connected_db()
    cursor = conn.cursor()

    query = "SELECT * FROM ouvrages WHERE 1=1"
    params = []

    if type_ouvrage:
        query += " AND type_ouvrage = ?"
        params.append(type_ouvrage)
    if localite:
        query += " AND localite = ?"
        params.append(localite)
    if etat:
        query += " AND etat = ?"
        params.append(etat)
    if numero_irh:
        query += " AND numero_irh = ?"
        params.append(numero_irh)
    if projet_id:
        query += " AND projet_id = ?"
        params.append(projet_id)

    cursor.execute(query, params)
    ouvrages = cursor.fetchall()
    if ouvrages :
        col_names = [description[0] for description in cursor.description]
        data = [dict(zip(col_names, row)) for row in ouvrages]
        return data
    return ouvrages

def get_all_communes():
    conn = connected_db()
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT commune 
        FROM ouvrages
        WHERE commune IS NOT NULL AND commune <> ''
        ORDER BY commune ASC
    """)

    communes = [row[0] for row in c.fetchall()]

    conn.close()
    return communes


def get_all_cantons():
    conn = connected_db()
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT canton 
        FROM ouvrages
        WHERE canton IS NOT NULL AND canton <> ''
        ORDER BY canton ASC
    """)

    cantons = [row[0] for row in c.fetchall()]

    conn.close()
    return cantons

#     print("✅ Import JSON vers SQLite réussi.")

def import_json_to_sqlite(json_path: str):
    """
    Importe un fichier JSON dans une base SQLite3.
    
    :param json_path: Chemin du fichier JSON à importer
    :param db_path: Chemin de la base SQLite3
    """
    try:
        # Charger le JSON
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        
        conn = connected_db()
        cursor = conn.cursor()

        for table_name, rows in data.items():
            if not rows:
                continue

            # Récupérer les colonnes à partir du premier élément
            columns = rows[0].keys()
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["?"] * len(columns))

            # Créer la table si elle n'existe pas (toutes les colonnes en TEXT)
            create_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {", ".join([col + " TEXT" for col in columns])}
            )
            """
            cursor.execute(create_query)

            # Insérer les données
            for row in rows:
                values = tuple(str(row[col]) for col in columns)
                cursor.execute(
                    f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})",
                    values
                )

        conn.commit()
        print(f"✅ Import réussi depuis {json_path} → ")
    except Exception as e:
        print(f"❌ Erreur d'import : {e}")
    finally:
        conn.close()


def export_sqlite_to_json(file_name):
    """
    Exporte toute la base SQLite3 en JSON.
    
    :param db_path: Chemin de la base SQLite3 (ex: 'database.db')
    :param json_path: Chemin du fichier JSON exporté
    """
    try:
        conn = connected_db()
        cursor = conn.cursor()

        # Récupérer toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        data = {}

        for table_name, in tables:
            # Ignorer les tables système
            if table_name.startswith('sqlite_'):
                continue

            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Récupérer les noms des colonnes
            col_names = [description[0] for description in cursor.description]

            # Créer une liste de dictionnaires
            data[table_name] = [
                dict(zip(col_names, row))
                for row in rows
            ]

        # Sauvegarder en JSON
        # with open(json_path, "w", encoding="utf-8") as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)
        # print(data)
        path=get_value("archive_path")
        name_path=os.path.join(path,file_name)
        with open(f"{name_path}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"✅ Export réussi → {name_path}")
    except Exception as e:
        print(f"❌ Erreur d'export : {e}")
    finally:
        conn.close()


def get_statistiques():
    conn = connected_db()
    cursor = conn.cursor()

    # --- Totaux simples ---
    cursor.execute("SELECT COUNT(*) FROM projets")
    nombre_projet = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(DISTINCT commune) FROM ouvrages")
    nombre_commune = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(DISTINCT canton) FROM ouvrages")
    nombre_canton = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM ouvrages")
    total_ouvrages = cursor.fetchone()[0] or 0

    # --- Totaux par état (depuis ouvrages) ---
    totals_par_etat = {"Bon état": 0, "En panne": 0, "Abandonné": 0}
    cursor.execute("SELECT etat, COUNT(*) FROM ouvrages GROUP BY etat")
    for etat_raw, cnt in cursor.fetchall():
        etat = _norm(etat_raw)
        if etat not in totals_par_etat:
            totals_par_etat[etat] = cnt
        else:
            totals_par_etat[etat] += cnt

    # --- par_type (calculé uniquement depuis ouvrages pour éviter doublons) ---
    par_type = defaultdict(lambda: {"Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0})
    cursor.execute("SELECT type_ouvrage, etat, COUNT(*) FROM ouvrages GROUP BY type_ouvrage, etat")
    for type_raw, etat_raw, cnt in cursor.fetchall():
        type_ = _norm(type_raw)
        etat = _norm(etat_raw)
        par_type[type_][etat] = par_type[type_].get(etat, 0) + cnt
        par_type[type_]["total_ouvrage"] += cnt

    # --- par_annee : année -> totaux + par_type -> par etat ---
    par_annee = defaultdict(lambda: {
        "total_ouvrages": 0,
        "total_bon_etat": 0,
        "total_panne": 0,
        "total_abandonne": 0,
        "par_type": defaultdict(lambda: {"Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0})
    })

    cursor.execute("SELECT annee, type_ouvrage, etat, COUNT(*) FROM ouvrages GROUP BY annee, type_ouvrage, etat")
    for annee_raw, type_raw, etat_raw, cnt in cursor.fetchall():
        annee = _norm(annee_raw)
        type_ = _norm(type_raw)
        etat = _norm(etat_raw)

        par_annee[annee]["total_ouvrages"] += cnt
        if etat == "Bon état":
            par_annee[annee]["total_bon_etat"] += cnt
        elif etat == "En panne":
            par_annee[annee]["total_panne"] += cnt
        elif etat == "Abandonné":
            par_annee[annee]["total_abandonne"] += cnt
        else:
            # si état inattendu, l'ajouter aussi
            par_annee[annee].setdefault("total_autres", 0)
            par_annee[annee]["total_autres"] += cnt

        par_annee[annee]["par_type"][type_][etat] = par_annee[annee]["par_type"][type_].get(etat, 0) + cnt
        par_annee[annee]["par_type"][type_]["total_ouvrage"] += cnt

    conn.close()

    # --- Trier les années en décroissant (numériques en premier) ---
    def year_key(k):
        if str(k).isdigit():
            return (0, int(k))
        return (1, str(k))
    ordered_years = sorted(par_annee.keys(), key=year_key, reverse=True)

    par_annee_ordered = {}
    for y in ordered_years:
        data = par_annee[y]
        # convertir par_type internes en dict
        par_type_dict = {t: dict(v) for t, v in data["par_type"].items()}
        par_annee_ordered[y] = {
            "total_ouvrages": data["total_ouvrages"],
            "total_bon_etat": data["total_bon_etat"],
            "total_panne": data["total_panne"],
            "total_abandonne": data["total_abandonne"],
            "par_type": par_type_dict
        }

    # convertir par_type global en dict
    par_type = {t: dict(v) for t, v in par_type.items()}

    # --- Construire le résultat final ---
    result = {
        "nombre_projet": nombre_projet,
        "nombre_commune": nombre_commune,
        "nombre_canton": nombre_canton,
        "total_ouvrages": total_ouvrages,
        "total_bon_etat": totals_par_etat.get("Bon état", 0),
        "total_panne": totals_par_etat.get("En panne", 0),
        "total_abandonne": totals_par_etat.get("Abandonné", 0),
        "par_type": par_type,
        "par_annee": par_annee_ordered
    }

    return result


def convert_to_dict(obj):
    """Convertit récursivement les defaultdict en dict classiques."""
    if isinstance(obj, defaultdict):
        obj = {k: convert_to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, dict):
        obj = {k: convert_to_dict(v) for k, v in obj.items()}
    return obj


from collections import defaultdict

def get_stats_commune(nom_commune):
    conn = connected_db()
    cursor = conn.cursor()
    """
    Récupère les stats pour UNE commune donnée.
    Accepts either a sqlite3.Connection or a sqlite3.Cursor as first arg.
    Exemple: get_stats_commune(conn, "Tône 4") ou get_stats_commune(cursor, "Tône 4")
    """
   
    # structure de travail
    stats = {
        "total_ouvrages": 0,
        "total_bon_etat": 0,
        "total_panne": 0,
        "total_abandonne": 0,
        "par_type": defaultdict(lambda: {
            "Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0
        }),
        "par_annee": defaultdict(lambda: {
            "total_ouvrages": 0,
            "total_bon_etat": 0,
            "total_panne": 0,
            "total_abandonne": 0,
            "par_type": defaultdict(lambda: {
                "Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0
            })
        })
    }

    # Requête CORRIGÉE : JOIN sur ouvrage.id via o.ouvrage_id
    cursor.execute("""
        SELECT o.annee, o.type_ouvrage, o.etat, COUNT(DISTINCT o.id) as cnt
        FROM ouvrages o WHERE o.commune = ?
        GROUP BY o.annee, o.type_ouvrage, o.etat
    """, (nom_commune,))

    rows = cursor.fetchall()

    # si aucune ligne, on retourne la structure vide (0)
    if not rows:
        # normaliser clés vides: convertir defaultdict en dict vide
        return {
            "total_ouvrages": 0,
            "total_bon_etat": 0,
            "total_panne": 0,
            "total_abandonne": 0,
            "par_type": {},
            "par_annee": {}
        }

    # traitement
    for annee_raw, type_raw, etat_raw, cnt in rows:
        annee = _norm(annee_raw)
        type_ = _norm(type_raw)
        etat = _norm(etat_raw)
        count = int(cnt or 0)

        stats["total_ouvrages"] += count
        if etat == "Bon état":
            stats["total_bon_etat"] += count
        elif etat == "En panne":
            stats["total_panne"] += count
        elif etat == "Abandonné":
            stats["total_abandonne"] += count

        # par type
        stats["par_type"][type_][etat] += count
        stats["par_type"][type_]["total_ouvrage"] += count

        # par année
        y = stats["par_annee"][annee]
        y["total_ouvrages"] += count
        if etat == "Bon état":
            y["total_bon_etat"] += count
        elif etat == "En panne":
            y["total_panne"] += count
        elif etat == "Abandonné":
            y["total_abandonne"] += count

        y["par_type"][type_][etat] += count
        y["par_type"][type_]["total_ouvrage"] += count

    # conversion finale : supprimer defaultdict
    final = {
        "total_ouvrages": stats["total_ouvrages"],
        "total_bon_etat": stats["total_bon_etat"],
        "total_panne": stats["total_panne"],
        "total_abandonne": stats["total_abandonne"],
        "par_type": {},
        "par_annee": {}
    }

    for typ, d in stats["par_type"].items():
        final["par_type"][typ] = dict(d)

    # tri décroissant des années (essaye de trier numériquement si possible)
    def year_key(y):
        try:
            return int(y)
        except Exception:
            return y
    for annee in sorted(stats["par_annee"].keys(), key=year_key, reverse=True):
        y = stats["par_annee"][annee]
        final["par_annee"][annee] = {
            "total_ouvrages": y["total_ouvrages"],
            "total_bon_etat": y["total_bon_etat"],
            "total_panne": y["total_panne"],
            "total_abandonne": y["total_abandonne"],
            "par_type": {t: dict(dd) for t, dd in y["par_type"].items()}
        }

    return final


def get_stats_canton(nom_canton):
    conn = connected_db()
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # 1) Préparer la structure des résultats
    # ---------------------------------------------------------
    stats = {
        "total_ouvrages": 0,
        "total_bon_etat": 0,
        "total_panne": 0,
        "total_abandonne": 0,

        "par_type": {},
        "par_annee": {}
    }

    # ---------------------------------------------------------
    # 2) Récupérer toutes les lignes correspondant au canton
    # ---------------------------------------------------------
    cursor.execute("""
        SELECT 
            o.annee,
            o.type_ouvrage,
            o.etat,
            COUNT(DISTINCT o.id)
        FROM ouvrages o
        WHERE o.canton = ?
        GROUP BY o.annee, o.type_ouvrage, o.etat
    """, (nom_canton,))

    rows = cursor.fetchall()

    # ---------------------------------------------------------
    # 3) Si aucun ouvrage trouvé → renvoyer structure vide
    # ---------------------------------------------------------
    if not rows:
        conn.close()
        return stats

    # ---------------------------------------------------------
    # 4) Traitement des lignes trouvées
    # ---------------------------------------------------------
    for annee, type_o, etat, count in rows:

        # ---------- Général ----------
        stats["total_ouvrages"] += count

        if etat == "Bon état":
            stats["total_bon_etat"] += count
        elif etat == "En panne":
            stats["total_panne"] += count
        elif etat == "Abandonné":
            stats["total_abandonne"] += count

        # ---------- Par type ----------
        if type_o not in stats["par_type"]:
            stats["par_type"][type_o] = {
                "Bon état": 0,
                "En panne": 0,
                "Abandonné": 0,
                "total_ouvrage": 0
            }

        stats["par_type"][type_o][etat] += count
        stats["par_type"][type_o]["total_ouvrage"] += count

        # ---------- Par année ----------
        if annee not in stats["par_annee"]:
            stats["par_annee"][annee] = {
                "total_ouvrages": 0,
                "total_bon_etat": 0,
                "total_panne": 0,
                "total_abandonne": 0,
                "par_type": {}
            }

        stats["par_annee"][annee]["total_ouvrages"] += count
        if etat == "Bon état":
            stats["par_annee"][annee]["total_bon_etat"] += count
        elif etat == "En panne":
            stats["par_annee"][annee]["total_panne"] += count
        elif etat == "Abandonné":
            stats["par_annee"][annee]["total_abandonne"] += count

        # --- par type dans par_annee ---
        if type_o not in stats["par_annee"][annee]["par_type"]:
            stats["par_annee"][annee]["par_type"][type_o] = {
                "Bon état": 0,
                "En panne": 0,
                "Abandonné": 0,
                "total_ouvrage": 0
            }

        stats["par_annee"][annee]["par_type"][type_o][etat] += count
        stats["par_annee"][annee]["par_type"][type_o]["total_ouvrage"] += count

    # ---------------------------------------------------------
    # 5) Trier les années par ordre décroissant
    # ---------------------------------------------------------
    stats["par_annee"] = dict(sorted(stats["par_annee"].items(), reverse=True))

    conn.close()
    return stats



def found_ouvrage_interval(date1, date2):
    conn = connected_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # ------------------------------------------------------------
    # 1️⃣ Récupération des ouvrages filtrés par dates
    cur.execute("""
        SELECT o.*, o.commune, o.canton, o.lieu
        FROM ouvrages o 
        WHERE date(o.created_at) BETWEEN date(?) AND date(?)
    """, (date1, date2))

    ouvrages = cur.fetchall()

    # Aucun résultat → renvoyer structure vide propre
    if not ouvrages:
        return {
            "total_ouvrages": 0,
            "total_communes": 0,
            "total_cantons": 0,
            "par_type_global": {},
            "par_commune": {},
            "par_canton": {},
            "details": []
        }

    # ------------------------------------------------------------
    # 2️⃣ Totaux simples
    total = len(ouvrages)
    communes = {o["commune"] for o in ouvrages if o["commune"]}
    cantons = {o["canton"] for o in ouvrages if o["canton"]}

    # ------------------------------------------------------------
    # 3️⃣ STRUCTURE GLOBALE PAR TYPE (version simplifiée)
    total_bon = 0
    total_panne = 0
    total_abandonne = 0

    par_type_global = {}

    for o in ouvrages:
        etat = o["etat"]
        type_ouv = o["type_ouvrage"]

        # Totaux globaux par état
        if etat == "Bon état":
            total_bon += 1
        elif etat == "En panne":
            total_panne += 1
        elif etat == "Abandonné":
            total_abandonne += 1

        # Initialisation
        if type_ouv not in par_type_global:
            par_type_global[type_ouv] = {
                "Bon état": 0,
                "En panne": 0,
                "Abandonné": 0,
                "Total": 0
            }

        # Comptage
        if etat in par_type_global[type_ouv]:
            par_type_global[type_ouv][etat] += 1
        par_type_global[type_ouv]["Total"] += 1

    par_type_global_final = {
        "total_ouvrages": total,
        "total_en_bon_etat": total_bon,
        "total_en_panne": total_panne,
        "total_abandonnee": total_abandonne,
        "par_type": par_type_global
    }

    # ------------------------------------------------------------
    # 4️⃣ STATISTIQUES PAR COMMUNE
    stats_commune = {}

    for o in ouvrages:
        c = o["commune"]
        if not c:
            continue

        if c not in stats_commune:
            stats_commune[c] = {
                "total_ouvrages": 0,
                "total_bon_etat": 0,
                "total_panne": 0,
                "total_abandonne": 0,
                "par_type": {}
            }

        etat = o["etat"]
        type_ouv = o["type_ouvrage"]

        # Totaux
        stats_commune[c]["total_ouvrages"] += 1

        if etat == "Bon état":
            stats_commune[c]["total_bon_etat"] += 1
        elif etat == "En panne":
            stats_commune[c]["total_panne"] += 1
        elif etat == "Abandonné":
            stats_commune[c]["total_abandonne"] += 1

        # Par type
        if type_ouv not in stats_commune[c]["par_type"]:
            stats_commune[c]["par_type"][type_ouv] = {
                "Bon état": 0, "En panne": 0, "Abandonné": 0, "Total": 0
            }

        stats_commune[c]["par_type"][type_ouv][etat] += 1
        stats_commune[c]["par_type"][type_ouv]["Total"] += 1

    # ------------------------------------------------------------
    # 5️⃣ STATISTIQUES PAR CANTON
    stats_canton = {}

    for o in ouvrages:
        ct = o["canton"]
        if not ct:
            continue

        if ct not in stats_canton:
            stats_canton[ct] = {
                "total_ouvrages": 0,
                "total_bon_etat": 0,
                "total_panne": 0,
                "total_abandonne": 0,
                "par_type": {}
            }

        etat = o["etat"]
        type_ouv = o["type_ouvrage"]

        # Totaux
        stats_canton[ct]["total_ouvrages"] += 1

        if etat == "Bon état":
            stats_canton[ct]["total_bon_etat"] += 1
        elif etat == "En panne":
            stats_canton[ct]["total_panne"] += 1
        elif etat == "Abandonné":
            stats_canton[ct]["total_abandonne"] += 1

        # Par type
        if type_ouv not in stats_canton[ct]["par_type"]:
            stats_canton[ct]["par_type"][type_ouv] = {
                "Bon état": 0, "En panne": 0, "Abandonné": 0, "Total": 0
            }

        stats_canton[ct]["par_type"][type_ouv][etat] += 1
        stats_canton[ct]["par_type"][type_ouv]["Total"] += 1

    # ------------------------------------------------------------
    # 6️⃣ LISTE DES DÉTAILS AVEC COMMUNE ET CANTON
    details = [
        {
            "id": o["id"],
            "type_ouvrage": o["type_ouvrage"],
            "etat": o["etat"],
            "annee": o["annee"],
            "commune": o["commune"],
            "canton": o["canton"],
            "lieu": o["lieu"]
        }
        for o in ouvrages
    ]

    conn.close()

    # ------------------------------------------------------------
    # 7️⃣ STRUCTURE FINALE
    return {
        "total_ouvrages": total,
        "total_communes": len(communes),
        "total_cantons": len(cantons),
        "par_type_global": par_type_global_final,
        "par_commune": stats_commune,
        "par_canton": stats_canton,
        "details": details
    }



def get_stats_par_projets(nom_projet):
    conn = connected_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Récupérer l'ID du projet
    cursor.execute("SELECT id FROM projets WHERE name = ?", (nom_projet,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {"error": f"Projet '{nom_projet}' introuvable"}

    projet_id = row["id"]

    # 2. Sélectionner tous les ouvrages liés à ce projet
    cursor.execute("""
        SELECT 
            o.id,
            o.type_ouvrage,
            o.annee,
            o.etat
        FROM ouvrages o
        WHERE o.projet_id = ?
    """, (projet_id,))

    rows = cursor.fetchall()
    conn.close()

    # Initialisation des compteurs
    stats = {
        "total_ouvrages": 0,
        "total_bon_etat": 0,
        "total_panne": 0,
        "total_abandonne": 0,
        "par_type": defaultdict(lambda: {"Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0}),
        "par_annee": defaultdict(lambda: {
            "total_ouvrages": 0,
            "total_bon_etat": 0,
            "total_panne": 0,
            "total_abandonne": 0,
            "par_type": defaultdict(lambda: {"Bon état": 0, "En panne": 0, "Abandonné": 0, "total_ouvrage": 0})
        })
    }

    # 3. Remplissage des statistiques
    for row in rows:
        etat = row["etat"]
        type_ouvr = row["type_ouvrage"]
        annee = row["annee"]

        # Global
        stats["total_ouvrages"] += 1
        if etat == "Bon état":
            stats["total_bon_etat"] += 1
        elif etat == "En panne":
            stats["total_panne"] += 1
        elif etat == "Abandonné":
            stats["total_abandonne"] += 1

        # Par type (global)
        stats["par_type"][type_ouvr][etat] += 1
        stats["par_type"][type_ouvr]["total_ouvrage"] += 1

        # Par année
        s_an = stats["par_annee"][annee]
        s_an["total_ouvrages"] += 1

        if etat == "Bon état":
            s_an["total_bon_etat"] += 1
        elif etat == "En panne":
            s_an["total_panne"] += 1
        elif etat == "Abandonné":
            s_an["total_abandonne"] += 1

        # Par type dans l'année
        s_an["par_type"][type_ouvr][etat] += 1
        s_an["par_type"][type_ouvr]["total_ouvrage"] += 1

    # Convertir les defaultdict en dict pour sortie propre
    stats["par_type"] = {k: dict(v) for k, v in stats["par_type"].items()}
    for annee, data in stats["par_annee"].items():
        data["par_type"] = {k: dict(v) for k, v in data["par_type"].items()}
        stats["par_annee"][annee] = dict(data)

    return stats


def _norm(s):
    """Nettoie les chaînes (supprime espaces, None -> 'Inconnue')."""
    if s is None:
        return "Inconnue"
    return str(s).strip()
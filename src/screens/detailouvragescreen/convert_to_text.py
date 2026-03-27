
def convert_data_all_to_text(ouvrage, foration, pompage):
    datas=ouvrage
    key_localisation=["lieu","canton",'commune','coordonnee_x','coordonnee_y','entreprise']
    
    title="Localisation".center(20,"*")
    
    text_to_shared=""
    text_to_shared+=f"{title}\n"
    
    for key in key_localisation:
        text_to_shared+=f"{key} : {datas[key]}\n"
            
    title2="Foration".center(20,"*")
    
    key_foration=["date_foration","prof_alteration",'prof_socle','prof_total','prof_tube_crepine','prof_tube_plein','debit_soufflage']
    text_to_shared+=f"{title2}\n"
    for key in key_foration:
        text_to_shared+=f"{key} : {foration.get(key, '--')}\n"
    
    title2="Pompage".center(20,"*")
    key_pompage=["date_pompage","type_pompe",'cote_pompe','temps_pompage','debit_pompage','niv_dynamique','niv_statique']
    text_to_shared+=f"{title2}\n"
    for key in key_pompage:
        text_to_shared+=f"{key} : {pompage.get(key, '--')}\n"
        
    return text_to_shared

def convert_data_foration_to_text(ouvrage, foration):
    datas=ouvrage
    key_localisation=["lieu","canton",'commune','coordonnee_x','coordonnee_y','entreprise']
    
    title="Localisation".center(20,"*")
    
    text_to_shared=""
    text_to_shared+=f"{title}\n"
    
    for key in key_localisation:
        text_to_shared+=f"{key} : {datas[key]}\n"
            
    title2="Foration".center(20,"*")
    
    key_foration=["date_foration","prof_alteration",'prof_socle','prof_total','prof_tube_crepine','prof_tube_plein','debit_soufflage']
    text_to_shared+=f"{title2}\n"
    for key in key_foration:
        text_to_shared+=f"{key} : {foration.get(key, '--')}\n"
    return text_to_shared


def convert_data_pompage_to_text(ouvrage, pompage):
    datas=ouvrage
    key_localisation=["lieu","canton",'commune','coordonnee_x','coordonnee_y','entreprise']
    
    title="Localisation".center(20,"*")
    
    text_to_shared=""
    text_to_shared+=f"{title}\n"
    
    for key in key_localisation:
        text_to_shared+=f"{key} : {datas[key]}\n"
            
    title2="Foration".center(20,"*")
    
    key_pompage=["date_pompage","type_pompe",'cote_pompe','temps_pompage','debit_pompage','niv_dynamique','niv_statique']
    text_to_shared+=f"{title2}\n"
    for key in key_pompage:
        text_to_shared+=f"{key} : {pompage.get(key, '--')}\n"
    return text_to_shared
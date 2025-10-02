import pandas as pd
from backend.utils import split_code_epreuve, group_c2
import streamlit as st

def get_numerique(db_connection, id_classement:int):
    # db_connection = get_db_connection()
    requete = f'''
    SELECT a.Code_bateau, a.Point, a.Nb_perf, a.Code_epreuve, c.Nom, c.Prenom, c.club, c.Numero_club
    FROM Clt_Bateau a, Liste_Bateaux_Coureur b, Liste_Coureur c
    WHERE a.Code_liste = {id_classement}
    AND a.Code_bateau = b.Numero
    AND b.Origine = 'DES'
    AND b.Matric = c.Matric
    ORDER BY a.Code_epreuve ASC, a.Nb_perf DESC, a.Point ASC 
    '''
    # numerique = pd.read_sql(requete, con=db_connection)
    numerique = st.session_state.db_connection.query(requete)

    numerique.columns = [col.lower() for col in numerique.columns]

    numerique['nom'] = numerique['nom'].str.upper()
    numerique['prenom'] = numerique['prenom'].str.upper()

    numerique = split_code_epreuve(numerique)

    numerique = group_c2(numerique)

    return numerique

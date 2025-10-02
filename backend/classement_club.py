import streamlit as st
import pandas as pd
import os
import math
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from backend.numerique import get_numerique


def calcul_valeur_club(df_club, verbose=False):
    numero_club = df_club['numero_club'].values[0] 
    if verbose:   
        print(f'Calcul de la valeur du club {numero_club}')

    valeur = 0
    penalites = 0

    # DataFrame to collect boats that count
    bateaux_qui_comptent = pd.DataFrame(columns=list(df_club.columns) + ['type_bateau'])

    # recherche des embarcations jeunes
    if verbose:
        print('\tJeunes:')
    jeunes = df_club.loc[df_club.categorie.isin(['U15', 'U18'])].head(2)
    if len(jeunes):
        for idx_jeune, (_, row) in enumerate(jeunes.iterrows(), 1):
            valeur += row['point']
            row_data = row.to_dict()
            row_data['type_bateau'] = f'Jeune {idx_jeune}'
            bateaux_qui_comptent = pd.concat([bateaux_qui_comptent, pd.DataFrame([row_data])], ignore_index=True)
    if len(jeunes) < 2:
        penalites += (2 - len(jeunes)) * 1000
        if verbose:
            print('\t\t{} jeunes manquants: {} points de pénalité'.format(2-len(jeunes), 1000 * (2-len(jeunes))))  

    # recherche des autres embarcations obligatoires  
    if verbose:
        print('\tCanoe Dame:')
    canoe_dame = df_club.loc[df_club.embarcation.isin(['C1D', 'C2D'])].head(1)
    if len(canoe_dame):
        valeur += canoe_dame.iloc[0]['point']
        row_data = canoe_dame.iloc[0].to_dict()
        row_data['type_bateau'] = 'Canoë Dame'
        bateaux_qui_comptent = pd.concat([bateaux_qui_comptent, pd.DataFrame([row_data])], ignore_index=True)
    else:
        penalites += 1000
        if verbose:
            print('\t\tPas de Canoë Dame, 1000 points de pénalité')

    if verbose:
        print('\tCanoe Homme:')
    canoe_homme = df_club.loc[df_club.embarcation.isin(['C1H'])].head(1)
    if len(canoe_homme):
        valeur += canoe_homme.iloc[0]['point']
        row_data = canoe_homme.iloc[0].to_dict()
        row_data['type_bateau'] = 'Canoë Homme'
        bateaux_qui_comptent = pd.concat([bateaux_qui_comptent, pd.DataFrame([row_data])], ignore_index=True)
    else:
        penalites += 1000
        if verbose:
            print('\t\tPas de Canoë Homme, 1000 points de pénalité')

    if verbose:
        print('\tKayak Dame:')
    kayak_dame = df_club.loc[df_club.embarcation.isin(['K1D'])].head(1)
    if len(kayak_dame):
        valeur += kayak_dame.iloc[0]['point']
        row_data = kayak_dame.iloc[0].to_dict()
        row_data['type_bateau'] = 'Kayak Dame'
        bateaux_qui_comptent = pd.concat([bateaux_qui_comptent, pd.DataFrame([row_data])], ignore_index=True)
    else:
        penalites += 1000
        if verbose:
            print('\t\tPas de Kayak Dame, 1000 points de pénalité')
    
    if verbose:
        print('\tKayak Homme:')
    kayak_homme = df_club.loc[df_club.embarcation.isin(['K1H'])].head(1)
    if len(kayak_homme):    
        valeur += kayak_homme.iloc[0]['point']
        row_data = kayak_homme.iloc[0].to_dict()
        row_data['type_bateau'] = 'Kayak Homme'
        bateaux_qui_comptent = pd.concat([bateaux_qui_comptent, pd.DataFrame([row_data])], ignore_index=True)
    else:
        penalites += 1000
        if verbose:
            print('\t\tPas de Kayak Homme, 1000 points de pénalité')       

    if verbose:
        print('\tCanoë Biplace:')
    canoe_biplace = df_club.loc[df_club.embarcation.isin(['C2H', 'C2M'])].head(1)
    if len(canoe_biplace):
        valeur += canoe_biplace.iloc[0]['point']
        row_data = canoe_biplace.iloc[0].to_dict()
        row_data['type_bateau'] = 'Canoë Biplace'
        bateaux_qui_comptent = pd.concat([bateaux_qui_comptent, pd.DataFrame([row_data])], ignore_index=True)
    else:
        penalites += 1000
        if verbose:
            print('\t\tPas de Canoë Biplace, 1000 points de pénalité')

    # recherche des 5 autres bateaux restants
    if verbose:
        print('\tAutres bateaux:')
    # Exclude already counted boats
    deja_comptes = bateaux_qui_comptent['code_bateau'].tolist()
    autres_bateaux = df_club[~df_club['code_bateau'].isin(deja_comptes)]
    n_bateaux_supplementaires = min(len(autres_bateaux), 5)

    for idx, (_, row) in enumerate(autres_bateaux.head(n_bateaux_supplementaires).iterrows()):
        valeur += row['point']
        row_data = row.to_dict()
        row_data['type_bateau'] = f'Autre Bateau {idx+1}'
        bateaux_qui_comptent = pd.concat([bateaux_qui_comptent, pd.DataFrame([row_data])], ignore_index=True)

    if len(autres_bateaux) < 5:
        n_bateaux_manquants = 5-len(autres_bateaux)
        penalites += 1000 * n_bateaux_manquants
        if verbose:
            print(f'\t\tManque {n_bateaux_manquants} bateaux, {n_bateaux_manquants}*1000 points de pénalité')

    valeur += penalites
    if verbose:
        print(f"Total: {valeur} points dont {penalites} de pénalité")

    # mise en commun de tous les bateaux à 4 courses, avec tag pour ceux qui comptent
    tous_les_bateaux_club = pd.DataFrame(columns=list(df_club.columns) + ['type_bateau'])
    autres_bateaux = df_club[~df_club['code_bateau'].isin(bateaux_qui_comptent['code_bateau'])]
    for i, row in autres_bateaux.head(n_bateaux_supplementaires).iterrows():
        row_data = row.to_dict()
        row_data['type_bateau'] = ''
        tous_les_bateaux_club = pd.concat([tous_les_bateaux_club, pd.DataFrame([row_data])], ignore_index=True)

    tous_les_bateaux_club = pd.concat([tous_les_bateaux_club, bateaux_qui_comptent], ignore_index=True)

    return tous_les_bateaux_club, float(valeur), penalites

def classement_club(db_connection, id_classement:int, bonus_file_path:str=None, save:bool=True,                    
                    save_dir: str = '../classements'
                    ):
    """
    Calcule et retourne le classement des clubs pour un identifiant de classement donné.

    Paramètres:
        id_classement (int): Identifiant du classement à traiter.
        bonus_file_path (str, optionnel): Chemin vers un fichier CSV contenant les bonus à appliquer par club.
        save_dir (str, optionnel): Répertoire de sauvegarde (non utilisé ici).

    Retourne:
        tuple: (df_classement, df_classement_details)
            - df_classement : DataFrame avec le classement des clubs (code_club, club, valeur, penalites, bonus)
            - df_classement_details : DataFrame détaillant les bateaux pris en compte pour chaque club

    Notes:
        - Trie les résultats par numéro de club puis par points croissants.
        - Utilise la fonction get_numerique pour récupérer les données de classement.
        - Applique les bonus si un fichier est fourni.
        - Exclut les bateaux biclub et ceux n'ayant pas 4 performances.
        - Les points sont bornés à 1000.
    """
    numerique = get_numerique(db_connection=db_connection, id_classement=id_classement)

    # Extraction de la liste des clubs qui apparaissent dans le classement numérique
    tous_clubs = numerique[['numero_club', 'club']].drop_duplicates().sort_values(by='numero_club')

    # Filtrage des bateaux n'ayant pas 4 performances
    numerique = numerique.loc[numerique.nb_perf == 4]

    # Filtrage des bateaux biclub
    numerique = numerique.loc[numerique.biclub == False]

    # Bornage des points des embarcations à 1000 points
    numerique['point'] = numerique['point'].clip(upper=1000)

    # Ordonnancement par numéro de club puis par points croissants 
    numerique = numerique.sort_values(by=['numero_club', 'point'], ascending=[True, True])

    # Lecture des bonus
    if bonus_file_path:
        bonus_data = pd.read_csv(bonus_file_path)[['code_club', 'Total_bonus']]
        bonus_data['code_club'] = bonus_data['code_club'].astype(str)
        bonus_exists = True
    else:
        bonus_exists = False 

    classement = []
    classement_details = []

    # Dictionnaire des clubs : code_club -> nom du club
    clubs_dict = numerique[['numero_club', 'club']].drop_duplicates().set_index('numero_club')['club'].to_dict()

    # Liste des clubs à traiter
    numeros_clubs = numerique['numero_club'].unique()

    for code_club in numeros_clubs:
        if bonus_exists and code_club in bonus_data['code_club'].values:
            bonus = bonus_data.loc[bonus_data.code_club == code_club, 'Total_bonus'].values[0]
            # print(f'Club {code_club} a un bonus de {bonus}')
        else:
            bonus = 0

        bateaux_club, valeur, penalites = calcul_valeur_club(numerique.loc[numerique.numero_club==code_club])

        classement.append([code_club, clubs_dict[code_club], valeur-bonus, penalites, bonus])

        for _, row in bateaux_club.iterrows():
            classement_details.append([
                row['club'],
                row['numero_club'],
                row['code_epreuve'], 
                row['embarcation'], 
                row['categorie'], 
                row['nom_prenom'], 
                row['point'], 
                row['type_bateau']
            ])

    # Finalisation du DataFrame détails
    df_classement_details = pd.DataFrame(classement_details, columns=[
        'club', 'numero_club', 'code_epreuve', 'embarcation', 'categorie', 'nom_prenom', 'point', 'type_bateau'
    ])
    df_classement_details = df_classement_details.sort_values(by=['numero_club', 'point'], ascending=[True, True]).reset_index(drop=True)
    
    # Preparation du pdf de sortie
    now = datetime.now()   
    YEAR = now.strftime("%Y")
    DAY = now.strftime("%d")    
    MONTH = now.strftime("%m")
    year_dir = os.path.join(save_dir, YEAR, 'club')
    os.makedirs(year_dir, exist_ok=True)

    if save:
        df_classement_details.to_csv(os.path.join(year_dir, f'classement_club_{YEAR}_version_{DAY}_{MONTH}_classement_{id_classement}.csv'), index=False)
    
    # Finalisation du DataFrame classement
    df_classement = pd.DataFrame(classement, columns=['code_club', 'club', 'valeur', 'penalites', 'bonus'])
    df_classement = df_classement.sort_values(by='valeur', ascending=True).reset_index(drop=True)
    
    # Ajout des clubs qui n'ont pas à minima un compétiteur à 4 courses
    clubs_manquants = tous_clubs[~tous_clubs['numero_club'].isin(df_classement['code_club'])]
    # Retirer les clubs dont le code_club contient un "/"
    clubs_manquants = clubs_manquants[~clubs_manquants['numero_club'].astype(str).str.contains('/')]
    for _, row in clubs_manquants.iterrows():
        df_classement = pd.concat([
            df_classement,
            pd.DataFrame([{
                'code_club': row['numero_club'],
                'club': row['club'],
                'valeur': float('nan'),
                'penalites': float('nan'),
                'bonus': float('nan')
            }])
        ], ignore_index=True)
    df_classement = df_classement.sort_values(by='valeur', ascending=True).reset_index(drop=True)

    if save:
        # Ajouter une colonne d'indice (rang) au début de chaque tableau
        df_n1 = df_classement[:15].copy()
        df_n1.insert(0, 'rang', range(1, len(df_n1) + 1))
        df_n2 = df_classement[15:30].copy()
        df_n2.insert(0, 'rang', range(16, 16 + len(df_n2)))
        df_n3 = df_classement[30:45].copy()
        df_n3.insert(0, 'rang', range(31, 31 + len(df_n3)))
        df_regional = df_classement[45:].copy()
        df_regional.insert(0, 'rang', range(46, 46 + len(df_regional)))

        # Tous les clubs régionaux sans points n'ont pas de classement
        df_regional.loc[df_regional['valeur'].isnull(), 'rang'] = ''

        # Preparation du pdf de sortie
        file_name = f"classement_club_{YEAR}_version_{DAY}_{MONTH}_classement_{id_classement}"
        

        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg

        a4_width, a4_height = 8.27, 11.69
        row_height = 0.25
        header_height = 0.35
        bottom_margin = 0.5
        top_margin = 0.7

        header = f"Classement Club {YEAR}\n\nClassement provisoire au {now.strftime('%d/%m/%Y')}"
        display_columns = ['rang', 'code_club', 'club', 'valeur']
        display_colnames = ['Rang', 'Code Club', 'Club', 'Valeur']

        # Calcul du nombre total de pages
        n_rows_regional = len(df_regional)
        usable_height = a4_height - top_margin - bottom_margin - header_height
        rows_per_page = max(1, int(usable_height // row_height))
        n_pages_regional = math.ceil(n_rows_regional / rows_per_page)
        total_pages = 1 + n_pages_regional  # 1 page pour N1/N2/N3 + pages régionales

        # Couleurs très claires pour chaque niveau
        color_n1 = "#ffe5e5"      # rouge très clair
        color_n2 = "#e5f0ff"      # bleu très clair
        color_n3 = "#e5ffe5"      # vert très clair
        color_reg = "#fff7e5"     # orange très clair

        # Première page : N1, N2, N3 sur la même page, titres juste au-dessus, tables alignées
        with PdfPages(os.path.join(year_dir, f"{file_name}.pdf")) as pdf:
            fig = plt.figure(figsize=(a4_width, a4_height))
            # Add logos and header
            logo_path_left = os.path.join('../data', 'logo_left.jpg')
            logo_path_right = os.path.join('../data', 'logo_right.png')
            if os.path.isfile(logo_path_left):
                img_left = mpimg.imread(logo_path_left)
                fig.add_axes([0.04, 0.855, 0.1495, 0.115], anchor='NW', zorder=1).imshow(img_left)
                plt.axis('off')
            if os.path.isfile(logo_path_right):
                img_right = mpimg.imread(logo_path_right)
                fig.add_axes([0.8, 0.86, 0.1625, 0.125], anchor='NE', zorder=1).imshow(img_right, interpolation='antialiased')
                plt.axis('off')
            fig.text(0.5, 1 - (top_margin - 0.2) / a4_height, header, ha='center', va='top', fontsize=12, weight='bold')

            # Placement des titres et tableaux
            block_height = 0.22  # hauteur totale pour chaque bloc (titre + table)
            table_height = 0.16  # hauteur de la table
            title_height = 0.03  # hauteur du titre
            left = 0.08
            width = 0.84

            blocks_top = [0.62, 0.35, 0.08]  # top positions pour chaque bloc (N1, N2, N3)
            titles = ["Nationale 1", "Nationale 2", "Nationale 3"]
            dfs = [df_n1, df_n2, df_n3]
            colors = [color_n1, color_n2, color_n3]

            column_alignments = ['center', 'center', 'left', 'right']
            largeurs_colonnes = [0.05, 0.07, 0.45, 0.09]
            for i, (top, title, df, color) in enumerate(zip(blocks_top, titles, dfs, colors)):
                # Titre juste au-dessus de la table
                fig.text(left + width/2, top + table_height + 0.04, title, ha='center', va='bottom', fontsize=11, weight='bold')
                ax = fig.add_axes([left, top, width, table_height])
                ax.axis('tight')
                ax.axis('off')
                page_data = df[display_columns].copy()
                for col in ['valeur']:
                    page_data[col] = page_data[col].apply(
                        lambda x: "" if pd.isnull(x) else f"{x:.2f}" if isinstance(x, float) else x
                    )
                table = ax.table(
                    cellText=page_data.values,
                    loc='center',
                    cellLoc='left',
                    colWidths=largeurs_colonnes
                )
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                for (row, col_idx), cell in table.get_celld().items():
                    cell.PAD = 0.02
                    cell.set_text_props(ha=column_alignments[col_idx])
                    cell.set_facecolor(color)
            fig.text(0.5, bottom_margin / 2 / a4_height, f"Page 1/{total_pages}", ha='center', va='center', fontsize=9)
            pdf.savefig(fig, bbox_inches=None)
            plt.close(fig)

            # Pages suivantes : régional (peut être sur plusieurs pages)
            page_data = df_regional[display_columns].copy()
            for col in ['valeur']:
                page_data[col] = page_data[col].apply(
                    lambda x: "" if pd.isnull(x) else f"{x:.2f}" if isinstance(x, float) else x
                )
            n_rows = len(page_data)
            usable_height = a4_height - top_margin - bottom_margin - header_height
            rows_per_page = max(1, int(usable_height // row_height))
            n_pages = math.ceil(n_rows / rows_per_page)

            for page in range(n_pages):
                start = page * rows_per_page
                end = min(start + rows_per_page, n_rows)
                page_slice = page_data.iloc[start:end]

                fig, ax = plt.subplots(figsize=(a4_width, a4_height))
                ax.axis('tight')
                ax.axis('off')

                # Add logos and header
                if os.path.isfile(logo_path_left):
                    img_left = mpimg.imread(logo_path_left)
                    fig.add_axes([0.04, 0.855, 0.1495, 0.115], anchor='NW', zorder=1).imshow(img_left)
                    plt.axis('off')
                if os.path.isfile(logo_path_right):
                    img_right = mpimg.imread(logo_path_right)
                    fig.add_axes([0.8, 0.86, 0.1625, 0.125], anchor='NE', zorder=1).imshow(img_right, interpolation='antialiased')
                    plt.axis('off')
                fig.text(0.5, 1 - (top_margin - 0.2) / a4_height, header, ha='center', va='top', fontsize=12, weight='bold')
                # Calculer la position verticale du haut de la table régionale
                table_top = 1 - (top_margin + 0.38) / a4_height
                table_height_reg = 0.7  # hauteur pour la table régionale

                # Titre juste au-dessus de la table
                table_title = f"Régional"
                if page < 1:
                    fig.text(left + width/2, table_top - 0.13, table_title, ha='center', va='bottom', fontsize=11, weight='bold')

                # Table alignée et largeur identique aux autres
                ax_table = fig.add_axes([left, bottom_margin / a4_height, width, table_top - bottom_margin / a4_height])
                ax_table.axis('tight')
                ax_table.axis('off')
                table = ax_table.table(
                    cellText=page_slice.values,
                    loc='center',
                    cellLoc='left',
                    colWidths=[0.05, 0.07, 0.5, 0.08]
                )
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                for (row, col_idx), cell in table.get_celld().items():
                    cell.PAD = 0.02
                    cell.set_text_props(ha=column_alignments[col_idx])                
                    cell.set_facecolor(color_reg)

                fig.text(0.5, bottom_margin / 2 / a4_height, f"Page {page + 2}/{total_pages}", ha='center', va='center', fontsize=9)

                pdf.savefig(fig, bbox_inches=None)
                plt.close(fig)
    

    # Add 1 to every index of df_classement
    df_classement.index = df_classement.index + 1

    # Ne pas remplacer les valeurs NaN dans df_classement['valeur']
    # Pour les lignes où 'valeur' est NaN, l'index doit être ''
    df_classement.index = [
        '' if pd.isnull(v) else i+1
        for i, v in enumerate(df_classement['valeur'])
    ]

    df_classement['valeur'] = df_classement['valeur'].apply(
        lambda x: '' if pd.isnull(x) else f"{x:.2f}" if isinstance(x, (float, int)) else x
    )
    df_classement['valeur'] = df_classement['valeur'].apply(lambda x: '' if pd.isnull(x) else x)



    df_classement_details['point'] = df_classement_details['point'].apply(
        lambda x: '' if pd.isnull(x) else f"{x:.2f}" if isinstance(x, (float, int)) else x
    )


    return df_classement, df_classement_details


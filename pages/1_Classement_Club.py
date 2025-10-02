import streamlit as st
import pandas as pd
from backend.sql_connection import initialize_connections
from backend.classement_club import classement_club
from params import CLASSEMENT_CLUB_CSV_BONUS_2025
from params import CLASSEMENT_CLUB_ID_DERNIER_NUMERIQUE
from params import CLASSEMENT_CLUB_DATE_DERNIER_NUMERIQUE
import datetime


st.markdown("# Classement Club")

# Appel de la fonction pour initialiser les connexions
initialize_connections()

@st.cache_data
def compute_classement_club():
    return classement_club(st.session_state.db_connection,
                           CLASSEMENT_CLUB_ID_DERNIER_NUMERIQUE,
                           bonus_file_path=CLASSEMENT_CLUB_CSV_BONUS_2025,
                           save=False)

df_classement, df_classement_details = compute_classement_club()


print(df_classement_details.columns)

date_MAJ_club = CLASSEMENT_CLUB_DATE_DERNIER_NUMERIQUE
if isinstance(date_MAJ_club, str):
    try:
        date_MAJ_club = datetime.datetime.strptime(date_MAJ_club, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        pass
elif isinstance(date_MAJ_club, (datetime.date, datetime.datetime)):
    date_MAJ_club = date_MAJ_club.strftime("%d/%m/%Y")

st.write(f"**Dernière mise à jour du classement club : {date_MAJ_club}**")

tab1, tab2, tab3, tab4= st.tabs(["Classement", "Détails", "Classement Numérique Sans Régionaux", "Rappel des régles de calcul"])

### TAB 1
def display_table(tab, title, df_slice, color=None):
    tab.markdown(f"<h2 style='text-align: center;'>{title}</h2>", unsafe_allow_html=True)
    styled_df = df_slice.rename(
        columns={
            'code_club': 'Code Club',
            'club': 'Club',
            'valeur': 'Valeur'
        }
    )[['Code Club', 'Club', 'Valeur']].style.set_table_styles(
        [{
            'selector': 'th',
            'props': [('text-align', 'center')]
        }]
    )
    tab.table(styled_df)

display_table(tab1, "Nationale 1", df_classement[:15])
display_table(tab1, "Nationale 2", df_classement[15:30])
display_table(tab1, "Nationale 3", df_classement[30:45])
display_table(tab1, "Régionale", df_classement[45:])


### TAB 2
option = tab2.selectbox(
    "",
    df_classement_details.numero_club.unique(),
    index=None,
    placeholder="Numéro du club ...",
    label_visibility='hidden'

)
with tab2.container():
    if option:
        nom_club = df_classement.loc[df_classement['code_club'] == option, 'club'].values[0]
        tab2.write(f"{option} - {nom_club}")

        penalite = df_classement.loc[df_classement['code_club'] == option, 'penalites'].values[0]
        points = df_classement.loc[df_classement['code_club'] == option, 'valeur'].values[0]

        if penalite > 0:            
            tab2.write(f"{points} points dont {penalite} de pénalités")
        else:
            tab2.write(f"{points} points")

    data_club = df_classement_details.loc[df_classement_details.numero_club==option].drop(['numero_club', 'club', 'embarcation', 'categorie'], axis=1).reset_index(drop=True)
    data_club.index = data_club.index + 1
    data_club = data_club.rename(
        columns={
            data_club.columns[0]: 'Embarcation - Catégorie',
            data_club.columns[1]: 'Nom Prénom',
            data_club.columns[2]: 'Valeur',
            data_club.columns[3]: ''
        }
    )
    tab2.table(data_club.style.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]}]
    ))

# tab2.write(f"Club affiché: {option}")

### TAB 3
tab3.write("Ce classement numérique **sans les courses régionales** sert de base pour le calcul du classement club.")

# cates = ['Scratch'] + list(df['Embarcation'].unique())
# cates_options = tab3.pills(
#     'Embarcation',
#     cates,
#     selection_mode = 'multi'
#     )
# print(cates_options)

# ages = ['Scratch'] + list(df['Age'].unique())
# ages_options = tab3.pills(
#     'Catégorie',
#     ages,
#     selection_mode = 'multi'
#     )
# print(ages_options)
# if 'Scratch' in cates_options:  
#     if 'Scratch' in ages_options:
#         display_data = df
#     else:
#         display_data = df[df['Age'].isin(ages_options)]
# else:
#     if 'Scratch' in ages_options:
#         display_data = df[df['Embarcation'].isin(cates_options)]
#     else:
#         display_data = df[df['Embarcation'].isin(cates_options) & df['Age'].isin(ages_options)]

#         # Add an index to allow ex aequo place
# display_data = display_data.sort_values(by=['n_courses', 'valeur'], ascending=[False, True])
# display_data['Place'] = display_data.groupby(['valeur', 'n_courses'], sort=True).ngroup() + 1
# display_data.reset_index(drop=True, inplace=True)
# display_data.set_index('Place', inplace=True)

# tab3.dataframe(display_data, hide_index=False)


### TAB 4

tab4.image('data/annexes_club_2025.PNG', caption='Annexes du règlement 2025', use_container_width =True)


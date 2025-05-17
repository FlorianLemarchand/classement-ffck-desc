import streamlit as st
import pandas as pd


st.markdown("# Classement Club")

@st.cache_data
def load_club_details():
    df = pd.read_csv(r"data/classement_club_details.csv")
    df.columns = ['Embarcation', 'Catégorie', 'Prénom', 'Nom', 'Valeur', '', 'code_club']
    df['Valeur'] = df['Valeur'].apply(lambda x: f"{x:.2f}")
    return df

@st.cache_data
def load_club():
    df = pd.read_csv(r"data/classement_club.csv")
    df.index = df.index + 1
    df.columns = ['Code Club', 'Nom Club', 'Valeur', 'Penalite']
    df['Valeur'] = df['Valeur'].apply(lambda x: f"{x:.2f}")
    return df

@st.cache_data
def load_MAJs():
    df = pd.read_csv(r"data/dernieres_MAJ.csv")
    return df

@st.cache_data
def load_numerique_club():
    df = pd.read_csv(r"data/numerique_club.csv").drop(columns=['Code_bateau'])
    # df_sort = df.sort_values(by=['Categorie', 'valeur'], ascending=[True, True])
    return df

df = load_numerique_club()

classement = load_club()
details = load_club_details()
date_MAJ_club = load_MAJs()
date_MAJ_club = date_MAJ_club.loc[date_MAJ_club.type_classement=='club'].date.iloc[0]

st.write(f"**Dernière mise à jour du classement club : {date_MAJ_club}**")

tab1, tab2, tab3, tab4= st.tabs(["Classement", "Détails", "Classement Numérique Sans Régionaux", "Rappel des régles de calcul"])

### TAB 1

tab1.markdown("<h2 style='text-align: center;'>Nationale 1</h2>", unsafe_allow_html=True)
tab1.table(classement[:15].drop(columns=['Penalite']), )

tab1.markdown("<h2 style='text-align: center;'>Nationale 2</h2>", unsafe_allow_html=True)
tab1.table(classement[15:30].drop(columns=['Penalite']))

tab1.markdown("<h2 style='text-align: center;'>Nationale 3</h2>", unsafe_allow_html=True)
tab1.table(classement[30:45].drop(columns=['Penalite']))

tab1.markdown("<h2 style='text-align: center;'>Régionale</h2>", unsafe_allow_html=True)
tab1.table(classement[45:].drop(columns=['Penalite']))


### TAB 2
option = tab2.selectbox(
    "",
    details.code_club.unique(),
    index=None,
    placeholder="Numéro du club ...",
    label_visibility='hidden'

)
with tab2.container():
    if option:
        nom_club = classement.loc[classement['Code Club'] == option, 'Nom Club'].values[0]
        tab2.write(f"{option} - {nom_club}")
        penalite = classement.loc[classement['Code Club'] == option, 'Penalite'].values[0]
        points = classement.loc[classement['Code Club'] == option, 'Valeur'].values[0]

        if penalite > 0:            
            tab2.write(f"{points} points dont {penalite} de pénalités")
        else:
            tab2.write("Pas de pénalité")
        
    data_club = details.loc[details.code_club==option].drop('code_club', axis=1).sort_values('Valeur').reset_index(drop=True)
    data_club.index = data_club.index + 1
    tab2.table(data_club)

# tab2.write(f"Club affiché: {option}")

### TAB 3
tab3.write("Ce classement numérique **sans les courses régionales** sert de base pour le calcul du classement club.")

cates = ['Scratch'] + list(df['Embarcation'].unique())
cates_options = tab3.pills(
    'Embarcation',
    cates,
    selection_mode = 'multi'
    )
print(cates_options)

ages = ['Scratch'] + list(df['Age'].unique())
ages_options = tab3.pills(
    'Catégorie',
    ages,
    selection_mode = 'multi'
    )
print(ages_options)
if 'Scratch' in cates_options:  
    if 'Scratch' in ages_options:
        display_data = df
    else:
        display_data = df[df['Age'].isin(ages_options)]
else:
    if 'Scratch' in ages_options:
        display_data = df[df['Embarcation'].isin(cates_options)]
    else:
        display_data = df[df['Embarcation'].isin(cates_options) & df['Age'].isin(ages_options)]

        # Add an index to allow ex aequo place
display_data = display_data.sort_values(by=['n_courses', 'valeur'], ascending=[False, True])
display_data['Place'] = display_data.groupby(['valeur', 'n_courses'], sort=True).ngroup() + 1
display_data.reset_index(drop=True, inplace=True)
display_data.set_index('Place', inplace=True)

tab3.dataframe(display_data, hide_index=False)


### TAB 4

tab4.image('data/annexes_club_2025.PNG', caption='Annexes du règlement 2025', use_container_width =True)


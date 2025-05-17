import streamlit as st
import pandas as pd
import os

st.markdown("# Classement Numérique")

@st.cache_data
def load_data():
    df = pd.read_csv(r"data/last_avec_SR.csv").drop(columns=['Code_bateau'])
    # df_sort = df.sort_values(by=['Categorie', 'valeur'], ascending=[True, True])
    return df

df = load_data()

cates = ['Scratch'] + list(df['Embarcation'].unique())
cates_options = st.pills(
    'Embarcation',
    cates,
    selection_mode = 'multi'
    )
print(cates_options)

ages = ['Scratch'] + list(df['Age'].unique())
ages_options = st.pills(
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

st.dataframe(display_data, hide_index=False)


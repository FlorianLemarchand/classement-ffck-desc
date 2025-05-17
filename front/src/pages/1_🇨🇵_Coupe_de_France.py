import streamlit as st
import pandas as pd


# st.markdown("# Classement Numérique")

# @st.cache_data
# def load_data():
#     df = pd.read_csv(r"./data/numerique_2025-02-24_avec_SR.csv").drop(columns=['Code_bateau'])
#     # df_sort = df.sort_values(by=['Categorie', 'valeur'], ascending=[True, True])
#     return df

# df = load_data()

# st.session_state
# keys = ['embarcation', 'cate']
# dict_keys = {'embarcation': 'Embarcation', 'cate': 'Age'}

# if all([x not in st.session_state for x in keys]):
#     df_run = df

# else:
#     df_run = df
#     for k in keys:
#         if st.session_state[k] is not None:
#             df_run = df_run[df_run[dict_keys[k]] == st.session_state[k]]


# embarcation = st.selectbox('Embarcation', df_run.Embarcation.unique(), index=None, placeholder="Embarcation ...", label_visibility='hidden', key='embarcation')
# cate = st.selectbox('Catégorie', df_run.Age.unique(), index=None, placeholder="Catégorie ...", label_visibility='hidden', key='cate')

    
# for k in keys:
#         if st.session_state[k] is not None:
#             df_run = df_run[df_run[dict_keys[k]] == st.session_state[k]]

# st.dataframe(df_run.sort_values(by=['n_courses','valeur'], ascending=[False, True]), hide_index=True)


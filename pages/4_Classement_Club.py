import streamlit as st
import pandas as pd


st.markdown("# Classement Club")

tab1, tab2, tab3, tab4= st.tabs(["Classement", "Détails", "Classement Numérique Sans Régionaux", "Rappel des régles de calcul"])

### TAB 1

### TAB 2
option = tab2.selectbox(
    "",
    ("6102-Argentan", "3801-Grenoble"),
    index=None,
    placeholder="Numéro ou nom du club ...",
    label_visibility='hidden'

)

# tab2.write(f"Club affiché: {option}")

### TAB 3
tab3.write("Ce classement numérique sans les courses régionales sert de base pour le calcul du classement club.")

### TAB 4


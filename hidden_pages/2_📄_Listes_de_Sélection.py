import streamlit as st
import pandas as pd
from streamlit_pdf_viewer import pdf_viewer


st.markdown("# Listes de Sélection")

tab1, tab2 = st.tabs(["Championnat de France Sprint 2025", "Championnat de France Classique 2025"])

with tab1.container():    
    pdf_viewer('data/selection_provisoire_france_sprint_2025_14-05-25.pdf')


with tab2.container():    
    pdf_viewer('data/selection_provisoire_france_classique_2025_14-05-25.pdf')

"""
Accueil.py - Page d'accueil de l'application Streamlit pour les classements descente FFCK

Cette application permet l'accès aux classements descente en attendant la refonte 
de la page descente FFCK officielle.
"""

import streamlit as st
from streamlit_extras.buy_me_a_coffee import button 
from backend.sql_connection import initialize_connections
from streamlit_extras.add_vertical_space import add_vertical_space 

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Classements Descente",
    page_icon="🛶"
)

# Contenu principal de la page d'accueil
st.markdown(
"""
# Classements Descente

Cette page a pour but de permettre l'accès aux classements descente en attendant la refonte de la page descente FFCK. 

Ces classements sont officieux, réalisés bénévolement. 

Seules les informations disponibles sur le site [FFCK](https://www.ffck.org/descente/) ont un caractère officiel.

### Liste des développements futurs

- Classement numérique:
    - Hyperlien compétiteur pour accès aux différents résultats
    - Graphique d'évolution des performances
- Classement club 
- Listes de sélection
- Historique des résultats

### Contributions

Pour toute remarque, veuillez écrire à l'adresse mail suivante: affichagedescente@gmail.com
"""
)

# Appel de la fonction pour initialiser les connexions
initialize_connections()


# =============================================================================
# Interface utilisateur - Section de contribution
# =============================================================================

# Ajout d'espace vertical pour la mise en page
add_vertical_space(1)

# Note: Bouton "Buy me a coffee" désactivé temporairement
# button(username="flck", floating=False, width=220, bg_color="#A6A6A8")

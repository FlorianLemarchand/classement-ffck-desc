import streamlit as st
from streamlit_extras.buy_me_a_coffee import button 
from streamlit_extras.add_vertical_space import add_vertical_space 

# Show the page title and description.
st.set_page_config(page_title="Classements Descente",
                   page_icon="🛶")


st.markdown(
"""
# Classements Descente

Cette page a pour but de permettre l'accès aux classements descente en attendant la refonte de la page descente FFCK. 

Ces classements sont officieux, réalisés bénévolement. 

Seules les informations disponibles sur le site [FFCK](https://www.ffck.org/descente/) ont un caractère officiel.

### Pages Disponibles

- [Classement Numérique](https://classement-ffck-desc-mqo63rtilj6dpjgzzmdsoq.streamlit.app/Classement_Numérique)

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

add_vertical_space(1)

# button(username="flck", floating=False, width=220, bg_color="#A6A6A8")


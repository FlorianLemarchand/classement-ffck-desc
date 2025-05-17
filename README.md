# Ce depôt stocke le code de calcul et d'affiche des résultats FFCK Descente.

# Installation

pip install -r requirements.txt

## Back
Le back-end est interfacé avec l'outil CompetFFCK. 
Le principe est d'aller lire les tables SQL présentes en local lorsque CompetFFCK tourne.
La mise à jour des données se fait hors-ligne.

## Front
Le front-end utilise l'outil streamlit pour afficher les tables calculées hors-ligne.


# Organisation du depôt

 * back : contient le code du back-end
 * front: contient le code du front-end
 * data: contient les données calculées par le back-end:
  * seule les dernières données calculées sont présentes sur le dépot 

  


# Environnement de dévelopement
Le code a été développé sur un PC Windows via Visual Studio. Aucun autere vnironnement n'a été testé.

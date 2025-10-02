import pandas as pd

################# FONCTIONS UTILES #####################

def split_code_epreuve(df):
    df[['embarcation', 'categorie']] = df['code_epreuve'].apply(
        lambda x: pd.Series([x[:3], x[3:]])
    )
    return df

def group_c2(df):
    # Ensure 'embarcation' and 'categorie' columns exist
    if 'embarcation' not in df.columns or 'categorie' not in df.columns:
        df = split_code_epreuve(df)

    # Work on a copy to avoid SettingWithCopyWarning
    df = df.copy()

    # Separate C2 and non-C2 rows
    is_c2 = df['embarcation'].str.contains('C2', na=False)
    df_c2 = df[is_c2].copy()
    df_non_c2 = df[~is_c2].copy()

    # Prepare output for C2
    out = []
    grouped = df_c2.groupby('code_bateau', sort=False)
    for n, g in grouped:
        if len(g) == 2:
            # Handle missing columns gracefully
            club1 = str(g.iloc[0].get('club', ''))
            club2 = str(g.iloc[1].get('club', ''))
            numero_club1 = str(g.iloc[0].get('numero_club', ''))
            numero_club2 = str(g.iloc[1].get('numero_club', ''))
            biclub = club1 != club2 or numero_club1 != numero_club2
            club = f"{club1}/{club2}" if biclub else club1
            numero_club = f"{numero_club1}/{numero_club2}" if biclub else numero_club1
            nom = f"{g.iloc[0].get('nom', '')}/{g.iloc[1].get('nom', '')}"
            prenom = f"{g.iloc[0].get('prenom', '')}/{g.iloc[1].get('prenom', '')}"
            nom_prenom = f"{g.iloc[0].get('nom', '')} {g.iloc[0].get('prenom', '')}/{g.iloc[1].get('nom', '')} {g.iloc[1].get('prenom', '')}"
            out.append([
                n,
                g.iloc[0].get('point', None),
                g.iloc[0].get('nb_perf', None),
                g.iloc[0].get('code_epreuve', ''),
                nom,
                prenom,
                club,
                numero_club,
                g.iloc[0].get('embarcation', ''),
                g.iloc[0].get('categorie', ''),
                biclub,
                nom_prenom
            ])
        else:
            # Skip groups that do not have exactly 2 members
            continue

    df_c2_out = pd.DataFrame(out, columns=[
        'code_bateau', 'point', 'nb_perf', 'code_epreuve', 'nom', 'prenom',
        'club', 'numero_club', 'embarcation', 'categorie', 'biclub', 'nom_prenom'
    ])

    # For non-C2, add biclub and nom_prenom columns
    df_non_c2['biclub'] = False
    df_non_c2['nom_prenom'] = df_non_c2['nom'].astype(str) + ' ' + df_non_c2['prenom'].astype(str)

    # Align columns for concatenation
    missing_cols = set(df_c2_out.columns) - set(df_non_c2.columns)
    for col in missing_cols:
        df_non_c2[col] = None
    df_non_c2 = df_non_c2[df_c2_out.columns]

    # Concatenate and reset index
    out_df = pd.concat([df_c2_out, df_non_c2], ignore_index=True)

    return out_df

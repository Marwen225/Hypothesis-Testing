import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Interface Streamlit
st.title("Analyse A/B Testing de Performances Web")
st.write("Téléchargez votre données A/B pour comparer les performances entre deux thèmes.")

# Upload du fichier
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Résumé de données
    st.subheader("Statistiques Descriptives")
    st.write(f"Nombre d'enregistrements : {df.shape[0]}")
    st.write(f"Nombre de colonnes : {df.shape[1]}")
    st.write(df.describe())
    
    # Valeurs manquantes
    st.subheader("Valeurs manquantes")
    st.write(df.isnull().sum())

    # Résumé de la performance par thème
    st.subheader("Comparaison de la performance par thème")
    theme_performance = df.groupby('Theme').mean()
    st.write(theme_performance)

    # Visualisation - Comparaison par thème
    st.subheader("Visualisations")
    metric_to_plot = st.selectbox("Sélectionnez une métrique à visualiser", df.columns[2:])
    sns.barplot(data=df, x="Theme", y=metric_to_plot)
    plt.title(f"Comparaison des Thèmes : {metric_to_plot}")
    st.pyplot(plt)

    # Test d'hypothèse
    st.subheader("Test d'hypothèse")
    
    # Comparaison du Taux de Clics
    ctr_light = df[df['Theme'] == 'Light Theme']['Click Through Rate']
    ctr_dark = df[df['Theme'] == 'Dark Theme']['Click Through Rate']
    t_stat_ctr, p_value_ctr = ttest_ind(ctr_light, ctr_dark, equal_var=False)
    
    # Comparaison du Taux de Rebond
    bounce_rates_light = df[df['Theme'] == 'Light Theme']['Bounce Rate']
    bounce_rates_dark = df[df['Theme'] == 'Dark Theme']['Bounce Rate']
    t_stat_bounce, p_value_bounce = ttest_ind(bounce_rates_light, bounce_rates_dark, equal_var=False)

    # Comparaison de la Profondeur de Défilement
    scroll_depth_light = df[df['Theme'] == 'Light Theme']['Scroll_Depth']
    scroll_depth_dark = df[df['Theme'] == 'Dark Theme']['Scroll_Depth']
    t_stat_scroll, p_value_scroll = ttest_ind(scroll_depth_light, scroll_depth_dark, equal_var=False)

    # Tableau récapitulatif des tests statistiques
    comparison_table = pd.DataFrame({
        'Métrique': ['Taux de Clics', 'Taux de Rebond', 'Profondeur de Défilement'],
        'T-Statistic': [t_stat_ctr, t_stat_bounce, t_stat_scroll],
        'P-Value': [p_value_ctr, p_value_bounce, p_value_scroll]
    })

    st.write(comparison_table)

    # Interprétation des résultats
    st.subheader("Interprétation des résultats")
    
    st.write(f"**Taux de clics (CTR)** : P-value = {p_value_ctr:.4f}")
    if p_value_ctr < 0.05:
        st.write("-> Le test révèle une différence significative, avec le thème sombre ayant probablement de meilleures performances.")
    else:
        st.write("-> Aucune interprétation de signification pour le taux de clics.")
    
    st.write(f"**Taux de conversion** : P-value = {p_value_bounce:.4f}")
    if p_value_bounce < 0.05:
        st.write("-> Il existe une différence significative pour le taux de rebond.")
    else:
        st.write("-> Aucune différence significative pour le taux de rebond.")
    
    st.write(f"**Profondeur de défilement** : P-value = {p_value_scroll:.4f}")
    if p_value_scroll < 0.05:
        st.write("-> Il existe une différence significative pour la profondeur de défilement.")
    else:
        st.write("-> Aucune différence significative pour la profondeur de défilement.")

else:
    st.write("Veuillez télécharger un fichier CSV pour commencer l'analyse.")

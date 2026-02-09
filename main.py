import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Géopolitique & Enjeux du Lithium")

# --- 1. DONNÉES ENRICHIES ---

# ACTEURS (Points sur la carte)
acteurs = [
    {"nom": "Triangle du Lithium", "lat": -22.0, "lon": -67.0, "type": "Extraction", "desc": "<b>Impact :</b> Stress hydrique critique dans le désert d'Atacama."},
    {"nom": "Mines de Greenbushes", "lat": -33.8, "lon": 116.0, "type": "Extraction", "desc": "Leader rocheux. Entreprise : <b>Albemarle / Tianqi</b>"},
    {"nom": "Raffinage Sichuan/Jiangxi", "lat": 28.0, "lon": 115.0, "type": "Transformation", "desc": "<b>Impact :</b> Pollution chimique locale. Leader : <b>Ganfeng</b>"},
    {"nom": "Gigafactory Nevada", "lat": 39.5, "lon": -119.8, "type": "Consommation", "desc": "Hub Tesla. Recyclage en développement (Mine urbaine)."},
    {"nom": "Battery Valley (UE)", "lat": 51.0, "lon": 10.0, "type": "Consommation", "desc": "Objectif : 25% de lithium recyclé d'ici 2030."},
    {"nom": "Mines de Manono (RDC)", "lat": -7.3, "lon": 27.4, "type": "Social", "desc": "<b>Enjeux :</b> Éthique, conditions de travail et droits humains."},
]

# FLUX
flux_data = [
    {"start_lat": -22.0, "start_lon": -67.0, "end_lat": 28.0, "end_lon": 115.0, "cat": "Trajet du Minerai (Extraction-Raffinage)", "label": "Carbonate (SQM/Ganfeng)", "color": "#3498db", "width": 3},
    {"start_lat": -33.8, "start_lon": 116.0, "end_lat": 28.0, "end_lon": 115.0, "cat": "Trajet du Minerai (Extraction-Raffinage)", "label": "Spodumène (Albemarle)", "color": "#3498db", "width": 4},
    {"start_lat": 48.0, "start_lon": 2.0, "end_lat": 52.0, "end_lon": 13.0, "cat": "Boucle de Récupération Locale", "label": "Économie circulaire européenne", "color": "#f1c40f", "width": 6}, 
]

# Données pour le graphique de comparaison (Réserves vs Production)
data_reserves = {
    'Pays': ['Bolivie', 'Argentine', 'Chili', 'Australie', 'Chine', 'USA'],
    'Réserves (Mt)': [21, 19, 11, 7.9, 6.8, 1.0],
    'Production (kt)': [1, 33, 39, 61, 19, 1]
}
df_res = pd.DataFrame(data_reserves)

# --- 2. INTERFACE STREAMLIT ---

st.title("⚡ La course au lithium : Enjeux et revers")

# --- 3. CARTE INTERACTIVE ---

fig = go.Figure()

# Ajout des Flux
for _, row in pd.DataFrame(flux_data).iterrows():
    fig.add_trace(go.Scattergeo(
        lon=[row['start_lon'], row['end_lon']], lat=[row['start_lat'], row['end_lat']],
        mode='lines', line=dict(width=row['width'], color=row['color']),
        opacity=0.6, name=row['cat'], hovertemplate=f"{row['label']}<extra></extra>"
    ))

# Ajout des Acteurs avec couleurs spécifiques
couleurs = {"Extraction": "#e74c3c", "Transformation": "#8e44ad", "Consommation": "#2980b9", "Social": "#e67e22"}

for t in pd.DataFrame(acteurs)['type'].unique():
    df_t = pd.DataFrame(acteurs)[pd.DataFrame(acteurs)['type'] == t]
    fig.add_trace(go.Scattergeo(
        lon=df_t['lon'], lat=df_t['lat'], text=df_t['nom'],
        hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>",
        customdata=df_t['desc'],
        marker=dict(size=12, color=couleurs.get(t), line=dict(width=1, color="black")),
        name=t, mode="markers"
    ))

fig.update_layout(geo=dict(projection_type="natural earth", showland=True, landcolor="#f0f0f0"), 
                  margin={"r":0,"t":0,"l":0,"b":0}, height=500)

st.plotly_chart(fig, use_container_width=True)

# --- 4. ANALYSE ET DATA-VIZ ---

tab1, tab2, tab3 = st.tabs(["📊 Données Stratégiques", "⚠️ Impacts Sociaux/Environnementaux", "🔄 Économie Circulaire"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Réserves vs Production")
        fig_bar = go.Figure(data=[
            go.Bar(name='Réserves (Millions de tonnes)', x=df_res['Pays'], y=df_res['Réserves (Mt)'], marker_color='#3498db'),
            go.Bar(name='Production (Milliers de tonnes)', x=df_res['Pays'], y=df_res['Production (kt)'], marker_color='#e74c3c')
        ])
        fig_bar.update_layout(barmode='group', height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.info("""
        **Le Paradoxe Bolivien :** La Bolivie possède les premières réserves mondiales, mais sa production est quasi-nulle faute d'infrastructures et de partenariats stables. 
        À l'inverse, l'Australie exploite intensément ses mines de roche.
        """)
        st.write("**Leaders Industriels :**")
        st.markdown("- **Albemarle (USA)** : Présent au Chili et Australie.\n- **SQM (Chili)** : Acteur historique du Salar.\n- **Tianqi & Ganfeng (Chine)** : Dominent le raffinage.")

with tab2:
    st.subheader("Le revers de la médaille")
    c1, c2, c3 = st.columns(3)
    c1.warning("💧 **Stress Hydrique**\n\nDans le Triangle du Lithium, il faut 2 millions de litres d'eau pour 1 tonne de lithium. Menace directe sur les populations indigènes.")
    c2.warning("⚒️ **Conditions Humaines**\n\nEn RDC, l'ouverture de méga-mines pose la question du respect des droits humains et du travail des mineurs artisanaux.")
    c3.warning("⚗️ **Pollution Chimique**\n\nLe raffinage chinois utilise de l'acide sulfurique. Les rejets peuvent contaminer les nappes phréatiques environnantes.")

with tab3:
    st.subheader("La Mine Urbaine : Vers l'indépendance ?")
    st.markdown("""
    Le recyclage est le levier majeur pour casser la dépendance géopolitique. 
    D'ici 2040, les batteries usagées pourraient couvrir **25% à 40%** des besoins de l'UE.
    """)
    st.progress(40, text="Potentiel de recyclage du lithium en 2050")

# --- 5. SCÉNARIOS PROSPECTIFS ---
st.markdown("---")
st.subheader("🔮 Scénarios Prospectifs 2050")
cols = st.columns(3)
with cols[0]:
    st.markdown("**1. Friend-Shoring**")
    st.caption("Les démocraties occidentales créent un circuit fermé sans la Chine.")
with cols[1]:
    st.markdown("**2. OPEP du Lithium**")
    st.caption("L'Argentine, le Chili et la Bolivie dictent les prix mondiaux.")
with cols[2]:
    st.markdown("**3. Obsolescence (Sodium-Ion)**")
    st.caption("Le Sodium (sel de table) remplace le Lithium. La carte géopolitique est totalement remise à zéro.")
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# --- 1. CHARGEMENT DU FOND DE CARTE (CORRECTION ICI) ---
# On charge directement le fichier ZIP depuis l'URL officielle Natural Earth
# car gpd.datasets.get_path a été supprimé dans GeoPandas 1.0
url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(url)

# Harmonisation des colonnes (Le fichier brut a des colonnes différentes de l'ancien dataset)
# On renomme 'ADMIN' en 'name' et 'POP_EST' en 'pop_est' pour garder la logique du script
if 'ADMIN' in world.columns:
    world = world.rename(columns={'ADMIN': 'name', 'POP_EST': 'pop_est'})

# On exclut l'Antarctique pour une meilleure visibilité
world = world[(world.pop_est > 0) & (world.name != "Antarctica")]

# --- 2. CRÉATION DES DONNÉES SIMULÉES (Indice de Stress Hydrique 0-10) ---
data_secheresse = {
    # Afrique
    'Somalia': 10, 'Ethiopia': 9, 'Sudan': 9, 'South Sudan': 9,
    'Chad': 9, 'Niger': 10, 'Mali': 9, 'Mauritania': 9,
    'Egypt': 8, 'Libya': 9, 'Algeria': 8, 'Morocco': 8,
    'South Africa': 7, 'Namibia': 8, 'Botswana': 7,
    
    # Moyen-Orient
    'Yemen': 10, 'Saudi Arabia': 9, 'Oman': 9, 'United Arab Emirates': 9,
    'Iran': 9, 'Iraq': 9, 'Syria': 9, 'Jordan': 9, 'Israel': 8, 'Turkey': 7,
    
    # Asie
    'Afghanistan': 9, 'Pakistan': 8, 'India': 7, 'China': 6, 'Mongolia': 6,
    'Kazakhstan': 6, 'Uzbekistan': 8, 'Turkmenistan': 8,
    
    # Amériques
    'United States of America': 5,
    'Mexico': 7, 'Chile': 8, 'Brazil': 4, 'Argentina': 5, 'Peru': 6,
    
    # Océanie / Europe
    'Australia': 9,
    'Spain': 7, 'Italy': 6, 'Greece': 7, 'France': 4, 'Germany': 3
}

df_data = pd.DataFrame(list(data_secheresse.items()), columns=['name', 'stress_index'])

# --- 3. FUSION DES DONNÉES ---
world_map = world.merge(df_data, on='name', how='left')
world_map['stress_index'] = world_map['stress_index'].fillna(2)

# --- 4. CRÉATION DU GRAPHIQUE ---
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.set_facecolor('#e0f7fa')

world_map.plot(
    column='stress_index',
    ax=ax,
    legend=True,
    legend_kwds={
        'label': "Indice de Risque de Sécheresse (0=Faible, 10=Extrême)",
        'orientation': "horizontal",
        'shrink': 0.6
    },
    cmap='YlOrRd',
    edgecolor='black',
    linewidth=0.3
)

# --- 5. FINITIONS ---
plt.title('Carte Mondiale des Zones à Risque de Sécheresse', fontsize=16, fontweight='bold', pad=20)
ax.set_axis_off()
plt.figtext(0.15, 0.15, "Source: Simulation / Natural Earth Data", fontsize=10, color='grey')

plt.savefig("carte_secheresse_monde_fixed.png", dpi=300, bbox_inches='tight')
print("Carte générée avec succès !")
plt.show()
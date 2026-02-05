import cv2
import numpy as np
import pyautogui
import pytesseract
import time
import re

# --- CONFIGURATION TESSERACT ---
# Si le script ne trouve pas tesseract, décommente et ajuste la ligne ci-dessous :
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

# --- COORDONNÉES (À REMPLIR PAR TOI) ---
# Utilise cmd+shift+4 sur Mac pour voir les coords, ou pyautogui.mouseInfo()
# Format: (left, top, width, height)
REGIONS = {
    "categorie": (490, 480, 300, 50),   # Titre haut (ex: "Capitale")
    "question":  (490, 610, 500, 80),   # Texte question (ex: "Corée du Nord")
    "map_area":  (490, 342, 700, 300),    # Grande zone pour la carte
    # Les 6 emplacements de boutons possibles
    "rep_1": (490, 480, 245, 75),   "rep_2": (410, 450, 245, 75),
    "rep_3": (490, 610, 245, 75),   "rep_4": (410, 530, 245, 75),
    "rep_5": (490, 740, 245, 75),   "rep_6": (410, 610, 245, 75),
    "next_btn":  (450, 800, 200, 100)
}

# --- BASE DE CONNAISSANCES (CERVEAU) ---
# Tu devras remplir ce dictionnaire au fur et à mesure
DATABASE = {
    "Albanie": {"capitale": "Tirana", "population": 2800000},
    "Allemagne": {"capitale": "Berlin", "population": 83200000},
    "Andorre": {"capitale": "Andorre-la-Vieille", "population": 80000},
    "Autriche": {"capitale": "Vienne", "population": 9000000},
    "Belgique": {"capitale": "Bruxelles", "population": 11600000},
    "Biélorussie": {"capitale": "Minsk", "population": 9300000},
    "Bosnie-Herzégovine": {"capitale": "Sarajevo", "population": 3200000},
    "Bulgarie": {"capitale": "Sofia", "population": 6800000},
    "Chypre": {"capitale": "Nicosie", "population": 1250000},
    "Croatie": {"capitale": "Zagreb", "population": 3900000},
    "Danemark": {"capitale": "Copenhague", "population": 5900000},
    "Espagne": {"capitale": "Madrid", "population": 47400000},
    "Estonie": {"capitale": "Tallinn", "population": 1330000},
    "Finlande": {"capitale": "Helsinki", "population": 5500000},
    "France": {"capitale": "Paris", "population": 67800000},
    "Grèce": {"capitale": "Athènes", "population": 10400000},
    "Hongrie": {"capitale": "Budapest", "population": 9700000},
    "Irlande": {"capitale": "Dublin", "population": 5000000},
    "Islande": {"capitale": "Reykjavik", "population": 376000},
    "Italie": {"capitale": "Rome", "population": 59000000},
    "Kosovo": {"capitale": "Pristina", "population": 1800000},
    "Lettonie": {"capitale": "Riga", "population": 1900000},
    "Liechtenstein": {"capitale": "Vaduz", "population": 39000},
    "Lituanie": {"capitale": "Vilnius", "population": 2800000},
    "Luxembourg": {"capitale": "Luxembourg", "population": 645000},
    "Macédoine du Nord": {"capitale": "Skopje", "population": 2080000},
    "Malte": {"capitale": "La Valette", "population": 520000},
    "Moldavie": {"capitale": "Chisinau", "population": 2600000},
    "Monaco": {"capitale": "Monaco", "population": 39000},
    "Monténégro": {"capitale": "Podgorica", "population": 620000},
    "Norvège": {"capitale": "Oslo", "population": 5400000},
    "Pays-Bas": {"capitale": "Amsterdam", "population": 17500000},
    "Pologne": {"capitale": "Varsovie", "population": 37800000},
    "Portugal": {"capitale": "Lisbonne", "population": 10300000},
    "République tchèque": {"capitale": "Prague", "population": 10500000},
    "Roumanie": {"capitale": "Bucarest", "population": 19000000},
    "Royaume-Uni": {"capitale": "Londres", "population": 67000000},
    "Russie": {"capitale": "Moscou", "population": 144000000},
    "Saint-Marin": {"capitale": "Saint-Marin", "population": 34000},
    "Serbie": {"capitale": "Belgrade", "population": 6800000},
    "Slovaquie": {"capitale": "Bratislava", "population": 5400000},
    "Slovénie": {"capitale": "Ljubljana", "population": 2100000},
    "Suède": {"capitale": "Stockholm", "population": 10400000},
    "Suisse": {"capitale": "Berne", "population": 8700000},
    "Ukraine": {"capitale": "Kyiv", "population": 38000000},
    "Vatican": {"capitale": "Vatican", "population": 800},
    "Afrique du Sud": {"capitale": "Pretoria", "population": 60600000},
    "Algérie": {"capitale": "Alger", "population": 45600000},
    "Angola": {"capitale": "Luanda", "population": 35600000},
    "Bénin": {"capitale": "Porto-Novo", "population": 13400000},
    "Botswana": {"capitale": "Gaborone", "population": 2630000},
    "Burkina Faso": {"capitale": "Ouagadougou", "population": 22700000},
    "Burundi": {"capitale": "Gitega", "population": 13200000},
    "Cameroun": {"capitale": "Yaoundé", "population": 28600000},
    "Cap-Vert": {"capitale": "Praia", "population": 590000},
    "République centrafricaine": {"capitale": "Bangui", "population": 5500000},
    "Comores": {"capitale": "Moroni", "population": 850000},
    "Congo-Brazzaville": {"capitale": "Brazzaville", "population": 6000000},
    "Congo-Kinshasa (RDC)": {"capitale": "Kinshasa", "population": 102000000},
    "Côte d'Ivoire": {"capitale": "Yamoussoukro", "population": 28200000},
    "Djibouti": {"capitale": "Djibouti", "population": 1100000},
    "Égypte": {"capitale": "Le Caire", "population": 112000000},
    "Érythrée": {"capitale": "Asmara", "population": 3600000},
    "Eswatini": {"capitale": "Mbabane", "population": 1200000},
    "Éthiopie": {"capitale": "Addis-Abeba", "population": 126000000},
    "Gabon": {"capitale": "Libreville", "population": 2400000},
    "Gambie": {"capitale": "Banjul", "population": 2700000},
    "Ghana": {"capitale": "Accra", "population": 33500000},
    "Guinée": {"capitale": "Conakry", "population": 13900000},
    "Guinée-Bissau": {"capitale": "Bissau", "population": 2100000},
    "Guinée équatoriale": {"capitale": "Malabo", "population": 1600000},
    "Kenya": {"capitale": "Nairobi", "population": 55000000},
    "Lesotho": {"capitale": "Maseru", "population": 2300000},
    "Liberia": {"capitale": "Monrovia", "population": 5400000},
    "Libye": {"capitale": "Tripoli", "population": 6800000},
    "Madagascar": {"capitale": "Antananarivo", "population": 30000000},
    "Malawi": {"capitale": "Lilongwe", "population": 21000000},
    "Mali": {"capitale": "Bamako", "population": 22600000},
    "Maroc": {"capitale": "Rabat", "population": 37800000},
    "Maurice": {"capitale": "Port-Louis", "population": 1300000},
    "Mauritanie": {"capitale": "Nouakchott", "population": 4700000},
    "Mozambique": {"capitale": "Maputo", "population": 33000000},
    "Namibie": {"capitale": "Windhoek", "population": 2600000},
    "Niger": {"capitale": "Niamey", "population": 26000000},
    "Nigeria": {"capitale": "Abuja", "population": 224000000},
    "Ouganda": {"capitale": "Kampala", "population": 48500000},
    "Rwanda": {"capitale": "Kigali", "population": 13800000},
    "Sao Tomé-et-Principe": {"capitale": "Sao Tomé", "population": 230000},
    "Sénégal": {"capitale": "Dakar", "population": 17300000},
    "Seychelles": {"capitale": "Victoria", "population": 107000},
    "Sierra Leone": {"capitale": "Freetown", "population": 8600000},
    "Somalie": {"capitale": "Mogadiscio", "population": 17600000},
    "Soudan": {"capitale": "Khartoum", "population": 48000000},
    "Soudan du Sud": {"capitale": "Juba", "population": 11000000},
    "Tanzanie": {"capitale": "Dodoma", "population": 65500000},
    "Tchad": {"capitale": "N'Djaména", "population": 17700000},
    "Togo": {"capitale": "Lomé", "population": 8800000},
    "Tunisie": {"capitale": "Tunis", "population": 12400000},
    "Zambie": {"capitale": "Lusaka", "population": 20000000},
    "Zimbabwe": {"capitale": "Harare", "population": 16300000},
    "Afghanistan": {"capitale": "Kaboul", "population": 41100000},
    "Arabie Saoudite": {"capitale": "Riyad", "population": 36000000},
    "Arménie": {"capitale": "Erevan", "population": 2800000},
    "Azerbaïdjan": {"capitale": "Bakou", "population": 10100000},
    "Bahreïn": {"capitale": "Manama", "population": 1500000},
    "Bangladesh": {"capitale": "Dacca", "population": 171000000},
    "Bhoutan": {"capitale": "Thimphou", "population": 780000},
    "Birmanie (Myanmar)": {"capitale": "Naypyidaw", "population": 54000000},
    "Brunei": {"capitale": "Bandar Seri Begawan", "population": 450000},
    "Cambodge": {"capitale": "Phnom Penh", "population": 16700000},
    "Chine": {"capitale": "Pékin", "population": 1412000000},
    "Chypre": {"capitale": "Nicosie", "population": 1250000},
    "Corée du Nord": {"capitale": "Pyongyang", "population": 26000000},
    "Corée du Sud": {"capitale": "Séoul", "population": 51700000},
    "Émirats arabes unis": {"capitale": "Abou Dabi", "population": 9400000},
    "Géorgie": {"capitale": "Tbilissi", "population": 3700000},
    "Inde": {"capitale": "New Delhi", "population": 1428000000},
    "Indonésie": {"capitale": "Jakarta", "population": 277000000},
    "Irak": {"capitale": "Bagdad", "population": 44500000},
    "Iran": {"capitale": "Téhéran", "population": 88500000},
    "Israël": {"capitale": "Jérusalem", "population": 9700000},
    "Japon": {"capitale": "Tokyo", "population": 123000000},
    "Jordanie": {"capitale": "Amman", "population": 11300000},
    "Kazakhstan": {"capitale": "Astana", "population": 19600000},
    "Kirghizistan": {"capitale": "Bichkek", "population": 6700000},
    "Koweït": {"capitale": "Koweït", "population": 4300000},
    "Laos": {"capitale": "Vientiane", "population": 7500000},
    "Liban": {"capitale": "Beyrouth", "population": 5500000},
    "Malaisie": {"capitale": "Kuala Lumpur", "population": 33900000},
    "Maldives": {"capitale": "Malé", "population": 525000},
    "Mongolie": {"capitale": "Oulan-Bator", "population": 3400000},
    "Népal": {"capitale": "Katmandou", "population": 30500000},
    "Oman": {"capitale": "Mascate", "population": 4600000},
    "Ouzbékistan": {"capitale": "Tachkent", "population": 35000000},
    "Pakistan": {"capitale": "Islamabad", "population": 235000000},
    "Palestine": {"capitale": "Jérusalem-Est", "population": 5200000},
    "Philippines": {"capitale": "Manille", "population": 115000000},
    "Qatar": {"capitale": "Doha", "population": 2700000},
    "Singapour": {"capitale": "Singapour", "population": 5900000},
    "Sri Lanka": {"capitale": "Sri Jayawardenepura Kotte", "population": 22000000},
    "Syrie": {"capitale": "Damas", "population": 22000000},
    "Tadjikistan": {"capitale": "Douchanbé", "population": 10000000},
    "Taïwan": {"capitale": "Taipei", "population": 23900000},
    "Thaïlande": {"capitale": "Bangkok", "population": 71600000},
    "Timor oriental": {"capitale": "Dili", "population": 1340000},
    "Turkménistan": {"capitale": "Achgabat", "population": 6400000},
    "Turquie": {"capitale": "Ankara", "population": 85300000},
    "Vietnam": {"capitale": "Hanoï", "population": 99000000},
    "Yémen": {"capitale": "Sanaa", "population": 33700000},
    "Antigua-et-Barbuda": {"capitale": "Saint John's", "population": 94000},
    "Argentine": {"capitale": "Buenos Aires", "population": 46200000},
    "Bahamas": {"capitale": "Nassau", "population": 410000},
    "Barbade": {"capitale": "Bridgetown", "population": 282000},
    "Belize": {"capitale": "Belmopan", "population": 410000},
    "Bolivie": {"capitale": "Sucre", "population": 12200000},
    "Brésil": {"capitale": "Brasilia", "population": 215000000},
    "Canada": {"capitale": "Ottawa", "population": 39000000},
    "Chili": {"capitale": "Santiago", "population": 19600000},
    "Colombie": {"capitale": "Bogota", "population": 52000000},
    "Costa Rica": {"capitale": "San José", "population": 5200000},
    "Cuba": {"capitale": "La Havane", "population": 11200000},
    "Dominique": {"capitale": "Roseau", "population": 73000},
    "Équateur": {"capitale": "Quito", "population": 18000000},
    "États-Unis": {"capitale": "Washington D.C.", "population": 335000000},
    "Grenade": {"capitale": "Saint George's", "population": 125000},
    "Guatemala": {"capitale": "Guatemala", "population": 18000000},
    "Guyana": {"capitale": "Georgetown", "population": 800000},
    "Haïti": {"capitale": "Port-au-Prince", "population": 11600000},
    "Honduras": {"capitale": "Tegucigalpa", "population": 10500000},
    "Jamaïque": {"capitale": "Kingston", "population": 2800000},
    "Mexique": {"capitale": "Mexico", "population": 128000000},
    "Nicaragua": {"capitale": "Managua", "population": 7000000},
    "Panama": {"capitale": "Panama", "population": 4400000},
    "Paraguay": {"capitale": "Asuncion", "population": 6800000},
    "Pérou": {"capitale": "Lima", "population": 34000000},
    "République dominicaine": {"capitale": "Saint-Domingue", "population": 11300000},
    "Saint-Christophe-et-Niévès": {"capitale": "Basseterre", "population": 48000},
    "Sainte-Lucie": {"capitale": "Castries", "population": 180000},
    "Saint-Vincent-et-les-Grenadines": {"capitale": "Kingstown", "population": 104000},
    "Salvador": {"capitale": "San Salvador", "population": 6300000},
    "Suriname": {"capitale": "Paramaribo", "population": 620000},
    "Trinité-et-Tobago": {"capitale": "Port-d'Espagne", "population": 1500000},
    "Uruguay": {"capitale": "Montevideo", "population": 3400000},
    "Venezuela": {"capitale": "Caracas", "population": 28000000},
    "Antigua-et-Barbuda": {"capitale": "Saint John's", "population": 94000},
    "Argentine": {"capitale": "Buenos Aires", "population": 46200000},
    "Bahamas": {"capitale": "Nassau", "population": 410000},
    "Barbade": {"capitale": "Bridgetown", "population": 282000},
    "Belize": {"capitale": "Belmopan", "population": 410000},
    "Bolivie": {"capitale": "Sucre", "population": 12200000},
    "Brésil": {"capitale": "Brasilia", "population": 215000000},
    "Canada": {"capitale": "Ottawa", "population": 39000000},
    "Chili": {"capitale": "Santiago", "population": 19600000},
    "Colombie": {"capitale": "Bogota", "population": 52000000},
    "Costa Rica": {"capitale": "San José", "population": 5200000},
    "Cuba": {"capitale": "La Havane", "population": 11200000},
    "Dominique": {"capitale": "Roseau", "population": 73000},
    "Équateur": {"capitale": "Quito", "population": 18000000},
    "États-Unis": {"capitale": "Washington D.C.", "population": 335000000},
    "Grenade": {"capitale": "Saint George's", "population": 125000},
    "Guatemala": {"capitale": "Guatemala", "population": 18000000},
    "Guyana": {"capitale": "Georgetown", "population": 800000},
    "Haïti": {"capitale": "Port-au-Prince", "population": 11600000},
    "Honduras": {"capitale": "Tegucigalpa", "population": 10500000},
    "Jamaïque": {"capitale": "Kingston", "population": 2800000},
    "Mexique": {"capitale": "Mexico", "population": 128000000},
    "Nicaragua": {"capitale": "Managua", "population": 7000000},
    "Panama": {"capitale": "Panama", "population": 4400000},
    "Paraguay": {"capitale": "Asuncion", "population": 6800000},
    "Pérou": {"capitale": "Lima", "population": 34000000},
    "République dominicaine": {"capitale": "Saint-Domingue", "population": 11300000},
    "Saint-Christophe-et-Niévès": {"capitale": "Basseterre", "population": 48000},
    "Sainte-Lucie": {"capitale": "Castries", "population": 180000},
    "Saint-Vincent-et-les-Grenadines": {"capitale": "Kingstown", "population": 104000},
    "Salvador": {"capitale": "San Salvador", "population": 6300000},
    "Suriname": {"capitale": "Paramaribo", "population": 620000},
    "Trinité-et-Tobago": {"capitale": "Port-d'Espagne", "population": 1500000},
    "Uruguay": {"capitale": "Montevideo", "population": 3400000},
    "Venezuela": {"capitale": "Caracas", "population": 28000000}
    
}

DB_CARTES = {} 

def capture_and_read(region_name):
    """Capture une zone et lit le texte via OCR."""
    x, y, w, h = REGIONS[region_name]
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
    return pytesseract.image_to_string(img, config='--psm 7').strip()

def analyser_carte_rouge():
    """Cherche un point rouge dans la zone map."""
    x, y, w, h = REGIONS["map_area"]
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) # OpenCV utilise BGR
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Plages de rouge
    lower1, upper1 = np.array([0, 70, 50]), np.array([10, 255, 255])
    lower2, upper2 = np.array([170, 70, 50]), np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower1, upper1) + cv2.inRange(hsv, lower2, upper2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    return None

def main():
    print("🤖 Bot actif. CTRL+C pour arrêter.")
    
    while True:
        try:
            # 1. On essaie de lire la catégorie (Texte)
            categorie = capture_and_read("categorie")
            coords_rouge = None
            mode_carte = False

            # Si l'OCR categorie échoue ou est vide, on vérifie si c'est une carte
            if len(categorie) < 3:
                coords_rouge = analyser_carte_rouge()
                if coords_rouge:
                    mode_carte = True
                    categorie = "Map" # On force le mode Map

            print(f"--- Nouvelle Question : {categorie} ---")

            # 2. Capture des réponses (On scanne les 6 boutons au cas où)
            reponses_ocr = {}
            boutons_actifs = ["rep_1", "rep_2", "rep_3", "rep_4", "rep_5", "rep_6"]
            for btn in boutons_actifs:
                # Petite optimisation : on ne lit pas si on est sûr qu'il n'y a que 4 boutons
                # Mais pour la sécurité, on lit tout pour l'instant
                txt = capture_and_read(btn)
                if txt: reponses_ocr[btn] = txt

            choix_final = None

            # --- LOGIQUE DÉCISIONNELLE ---
            
            # CAS 1 : CARTE (Blobe Rouge)
            if mode_carte and coords_rouge:
                key_coord = f"{coords_rouge[0]}_{coords_rouge[1]}"
                print(f"📍 Carte détectée au point : {key_coord}")
                
                # Recherche approximative dans DB_CARTES
                found_pays = None
                for saved_key, saved_pays in DB_CARTES.items():
                    sx, sy = map(int, saved_key.split('_'))
                    # Si le point est à moins de 15 pixels d'un point connu
                    if abs(sx - coords_rouge[0]) < 15 and abs(sy - coords_rouge[1]) < 15:
                        found_pays = saved_pays
                        break
                
                if found_pays:
                    print(f"🧠 Je reconnais : {found_pays}")
                    for btn, txt in reponses_ocr.items():
                        if found_pays.lower() in txt.lower():
                            choix_final = btn
                else:
                    print("❓ Carte inconnue.")

            # CAS 2 : CAPITALE (Texte)
            elif "Capitale" in categorie:
                pays = capture_and_read("question") # Lire "Corée du Nord"
                # Nettoyage basique du texte pays
                pays = re.sub(r'[^\w\s]', '', pays).strip() 
                
                if pays in DATABASE and "capitale" in DATABASE[pays]:
                    target = DATABASE[pays]["capitale"]
                    for btn, txt in reponses_ocr.items():
                        if target.lower() in txt.lower():
                            choix_final = btn

            # CAS 3 : POPULATION
            elif "Population" in categorie:
                # Logique population simplifiée (à compléter)
                pass

            # --- ACTION ---
            if choix_final:
                print(f"✅ Click sur {choix_final} ({reponses_ocr[choix_final]})")
                bx, by, bw, bh = REGIONS[choix_final]
                pyautogui.click(bx + bw//2, by + bh//2)
                time.sleep(3) # Attente animation
                
                # Clique sur "Continuer" (si écran vert)
                nx, ny, nw, nh = REGIONS["next_btn"]
                pyautogui.click(nx + nw//2, ny + nh//2)
            else:
                # Si on ne sait pas, on tente au hasard le bouton 1
                print("🎲 Hasard...")
                # pyautogui.click(...) # Décommenter pour activer le hasard
                time.sleep(1)

            time.sleep(1)

        except KeyboardInterrupt:
            break
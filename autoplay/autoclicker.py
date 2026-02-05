import pyautogui
import time

def auto_clicker(nombre_de_clics, intervalle=0.1):
    print(f"Lancement dans 3 secondes... Prépare ta souris !")
    time.sleep(3)
    
    print(f"C'est parti pour {nombre_de_clics} clics.")
    
    for i in range(nombre_de_clics):
        pyautogui.click()
        # Petit délai entre chaque clic pour ne pas faire planter l'application cible
        time.sleep(intervalle)
        
    print("Terminé !")

# --- Configuration ---
# Change le chiffre ici par le nombre de clics que tu souhaites
# Change l'intervalle (en secondes) si besoin
vitesse = 0.03

auto_clicker(X, vitesse)
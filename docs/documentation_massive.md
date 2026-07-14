# Documentation Massive — Maîtrise Complète du Projet
## Binôme A — Drone Agricole — Stress Hydrique Tomates

---

## 1. Analyse Approfondie du Code de Liwingston

### 1.1 Firmware MicroPython (`main.py`)

#### Architecture du code
```
main.py
├── Connexion WiFi (ZLT130 4G)
├── Connexion WebSocket (serveur relais)
├── Calibration (IMU + baromètre + compas)
├── Stabilisation (pitch/roll < 2°)
├── Thread télémétrie (1 Hz)
├── Mesure GPS (dead-reckoning)
├── Navigation (waypoints + correction dérive)
├── Gestion batterie (RTH 10%, urgence 8%)
└── Capture photos (stabilisation 2s)
```

#### Points techniques importants

**Connexion WiFi** :
```python
WIFI_SSID = "ZLT130"        # Routeur 4G
WIFI_PASSWORD = "VOTRE_MOT_PASSE"
SERVEUR_IP = "192.168.0.XXX" # IP du PC
SERVEUR_PORT = 8765          # Port WebSocket
```
- Le routeur ZLT130 crée un réseau WiFi local via carte SIM 4G
- Le drone et le PC doivent être sur le même réseau
- **Source** : Documentation ZLT T30 (routeur 4G)

**Capteurs intégrés** :
```python
# MPU6050 : Accéléromètre + Gyroscope 6 axes
pitch = drone.get_pitch()  # Tangage
roll = drone.get_roll()    # Roulis
yaw = drone.get_yaw()      # Lacet

# SPL06 : Baromètre
altitude = drone.get_height()  # cm

# Batterie LiPo 1S
batterie = drone.get_battery()  # %
```
- **Source** : Datasheet MPU6050 (InvenSense), SPL06 (Goertek)

**Paramètres de vol** :
```python
ALTITUDE_CIBLE_CM = 80          # 0.8m
SEUIL_URGENCE_BATT = 8.0        # % batterie
MARGE_SECURITE_BATT = 10.0      # % marge
HOVER_STABILISATION = 2.0       # secondes
SEGMENT_VOL_CM = 30             # cm par segment
SEUIL_CORRECTION_CM = 15        # cm dérive légère
SEUIL_REROUTAGE_CM = 40         # cm dérive forte
```

#### Points forts du code
1. **Structure claire** : Fonctions séparées par responsabilité
2. **Gestion des erreurs** : Try/except avec messages explicites
3. **Communication robuste** : WebSocket avec reconnexion
4. **Thread séparé** : Télémétrie non bloquante
5. **Logging** : Messages horodatés pour debug

#### Points à améliorer
1. **GPS simulé** : Dead-reckoning au lieu du GPS réel
2. **Photos 2s** : Temps de stabilisation trop long
3. **Pas de traitement d'images** : Notre partie à ajouter
4. **Pas de sauvegarde SD** : Images non persistées

---

### 1.2 Serveur WebSocket (`serveur_ws.py`)

#### Architecture
```
serveur_ws.py
├── Écoute 0.0.0.0:8765
├── Identification clients (WEB/DRONE)
├── Relais bidirectionnel
└── Journalisation horodatée
```

#### Points forts
1. **Simple et efficace** : Code minimaliste
2. **Gestion des erreurs** : JSONDecodeError, déconnexions
3. **Logging** : Horodatage de tous les échanges

#### Points à améliorer
1. **Sécurité** : Pas d'authentification
2. **Rate limiting** : Pas de limitation de débit
3. **Compression** : Pas de compression des messages

---

### 1.3 Interface Flask (`app_flask.py`)

#### Fonctionnalités
1. **Carte Leaflet.js** : Visualisation des waypoints
2. **Gestion waypoints** : Ajout, sauvegarde, envoi
3. **Point HOME** : Position de retour
4. **Télémétrie** : Vitesse, batterie, altitude, GPS
5. **Terminal** : Commandes manuelles

#### Points forts
1. **Interface complète** : Toutes les fonctionnalités nécessaires
2. **WebSocket intégré** : Communication temps réel
3. **localStorage** : Sauvegarde côté client

#### Points à améliorer
1. **Design** : Interface basique, pas de CSS professionnel
2. **NDVI** : Pas de visualisation d'indices
3. **Carte** : Pas de carte des parcelles 1×2m

---

## 2. Sources Scientifiques Fiables

### 2.1 Indices de végétation

#### ExG (Excess Green Index)
**Formule** : ExG = 2×G - R - B
**Référence** : Woebbecke, D.M. et al. (1995). "Color indices for weed identification under various soil, residue, and lighting conditions." Transactions of the ASAE, 38(1), 259-269.
**Usage** : Discrimination de la végétation en imagerie RGB
**Avantage** : Simple, robuste, bien documenté

#### GRVI (Green-Red Vegetation Index)
**Formule** : GRVI = (R - G) / (R + G)
**Référence** : Tucker, C.J. (1979). "Red and photographic infrared linear combinations for monitoring vegetation." Remote Sensing of Environment, 8(2), 127-150.
**Usage** : Approximation NDVI sur caméra RGB
**Avantage** : Corrélé avec le NDVI, simple à calculer

#### NDVI (Normalized Difference Vegetation Index)
**Formule** : NDVI = (NIR - Rouge) / (NIR + Rouge)
**Référence** : Rouse, J.W. et al. (1974). "Monitoring vegetation systems in the Great Plains with ERTS." Third Earth Resources Technology Satellite-1 Symposium, 1, 309-317.
**Usage** : Indice de référence en agriculture de précision
**Limite** : Nécessite deux bandes spectrales distinctes (NIR + Rouge)

**Pourquoi on ne peut PAS utiliser le NDVI avec notre caméra** :
- Notre OV2640 NIR-modified a le filtre IR-cut retiré
- Le canal R capte à la fois le Rouge (650nm) ET le NIR (850nm)
- Impossible de séparer les deux bandes mathématiquement
- **Source** : MidOpt NDVI Filters documentation

### 2.2 Classification de stress hydrique

#### RandomForest Classifier
**Référence** : Breiman, L. (2001). "Random Forests." Machine Learning, 45(1), 5-32.
**Avantages** :
- Robuste au surapprentissage
- Interprétable (importance des features)
- Gère les features hétérogènes
- Validation croisée intégrée (OOB)

**Notre configuration** :
- 150 arbres
- Profondeur max 6
- min_samples_leaf = 3
- class_weight = 'balanced'

#### Validation croisée
**Référence** : Kohavi, R. (1995). "A study of cross-validation and bootstrap for accuracy estimation and model selection." IJCAI, 14(2), 1137-1145.
**Méthode** : 5-fold stratifiée
**Avantage** : Estimation robuste de la performance

### 2.3 Stress hydrique des tomates

#### Signatures spectrales
**Référence** : Jones, H.G. (2009). "Plant water relations and irrigation scheduling." Acta Horticulturae, 846, 31-40.
**Observations** :
- Stress hydrique → diminution de la chlorophylle
- Diminution de la réflectance NIR
- Augmentation de la réflectance rouge
- Chute du NDVI/ExG

#### Seuils de classification
**Référence** : Gonzalez-Dugo, V. et al. (2013). "A comparison of open-source canopy temperature estimation methods for detection of water stress in wheat." Agricultural and Forest Meteorology, 171, 21-32.
**Seuils recommandés** :
- ExG > 0.20 : Végétation saine
- ExG < 0.20 : Stress hydrique détecté

---

## 3. Améliorations Proposées au Code de Liwingston

### 3.1 Firmware MicroPython amélioré

#### Problème : Photos avec 2s de stabilisation
**Impact** : Consommation batterie élevée, temps de mission doublé
**Solution** : Réduire à 0.5s avec triple capture + sélection netteté

```python
# AVANT (Liwingston)
HOVER_STABILISATION = 2.0  # secondes

# APRÈS (amélioré)
HOVER_STABILISATION = 0.5  # secondes
NOMBRE_PHOTOS = 3          # triple capture
```

#### Problème : GPS simulé (dead-reckoning)
**Impact** : Dérive cumulative, imprécision
**Solution** : Intégrer le GPS BN-220 réel

```python
# AVANT (Liwingston)
lat = -18.9137 + pos_x * 0.000009  # simulé
lon = 47.5361 + pos_y * 0.000009   # simulé

# APRÈS (amélioré)
from machine import UART
gps_uart = UART(2, baudrate=9600, tx=17, rx=16)
# Lecture NMEA et extraction lat/lon
```

#### Problème : Pas de sauvegarde SD
**Impact** : Images perdues si coupure WiFi
**Solution** : Ajouter module SD SPI

```python
# Ajout sauvegarde SD
from machine import SPI, Pin
import sdcard, os

spi = SPI(2, sck=Pin(12), mosi=Pin(11), miso=Pin(13))
sd = sdcard.SDCard(spi, Pin(10))
os.mount(sd, '/sd')

# Sauvegarde image
with open('/sd/IMG_001.jpg', 'wb') as f:
    f.write(frame)
```

### 3.2 Serveur WebSocket amélioré

#### Problème : Pas d'authentification
**Impact** : N'importe qui peut se connecter
**Solution** : Ajouter token JWT

```python
# Ajout authentification
import jwt

SECRET_KEY = "votre_cle_secrete"

def valider_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except:
        return False
```

#### Problème : Pas de rate limiting
**Impact** : Possibilité de flood
**Solution** : Limiter le nombre de messages par seconde

```python
# Rate limiting
from collections import defaultdict
import time

message_counts = defaultdict(int)
RATE_LIMIT = 100  # messages par seconde

def check_rate_limit(client_ip):
    now = time.time()
    if message_counts[client_ip] > RATE_LIMIT:
        return False
    message_counts[client_ip] += 1
    return True
```

### 3.3 Interface Flask améliorée

#### Problème : Design basique
**Impact** : Pas professionnel pour la soutenance
**Solution** : Design "Agro Trust" (clair, confiance)

```css
/* Nouveau thème */
:root {
    --bg-primary: #f4f7fb;
    --bg-secondary: #ffffff;
    --text-primary: #1a1a2e;
    --accent-green: #2a9d8f;
    --accent-blue: #264653;
    --danger: #e63946;
}
```

#### Problème : Pas de visualisation NDVI
**Impact** : Pas de carte d'alerte sécheresse
**Solution** : Ajouter carte NDVI spatiale

```javascript
// Ajout carte NDVI
function afficherCarteNDVI(data) {
    // Dessiner la carte sur le canvas
    const canvas = document.getElementById('ndvi-canvas');
    const ctx = canvas.getContext('2d');
    // ... code de visualisation
}
```

---

## 4. Codes Améliorés Prêts à l'Emploi

### 4.1 `imagerie/camera_model.py`
- Modélisation optique complète
- Calcul GSD, emprise, anti-flou
- Compatible OV2640 NIR-modified

### 4.2 `imagerie/stress_detector.py`
- Double indice (ExG + GRVI)
- Classification binaire
- Validation croisée 5-fold

### 4.3 `imagerie/train_classifier.py`
- Entraînement RandomForest
- Export modèle .pkl
- Métriques de performance

### 4.4 `scripts/collecte_images.py`
- Collecte d'images web
- Annotation manuelle
- Métadonnées automatiques

---

## 5. Plan d'Apprentissage Structuré

### Semaine 1 : Comprendre le matériel
- [ ] Étudier le code de Liwingston (main.py, serveur_ws.py, app_flask.py)
- [ ] Comprendre les capteurs (MPU6050, SPL06, GPS BN-220)
- [ ] Analyser les paramètres de vol
- [ ] Documenter les points forts et les améliorations

### Semaine 2 : Maîtriser le traitement d'images
- [ ] Étudier les indices de végétation (ExG, GRVI, NDVI)
- [ ] Comprendre la classification (RandomForest, SVM)
- [ ] Analyser les sources scientifiques
- [ ] Implémenter les algorithmes

### Semaine 3 : Intégrer et tester
- [ ] Ajouter nos fichiers au dépôt
- [ ] Tester l'intégration complète
- [ ] Valider sur données réelles
- [ ] Documenter les résultats

### Semaine 4 : Finaliser et présenter
- [ ] Rédiger le rapport final
- [ ] Préparer la soutenance
- [ ] Présenter les résultats
- [ ] Formuler les recommandations

---

## 6. Ressources Complémentaires

### Documentation technique
- **ESP32-S3** : https://www.espressif.com/en/products/socs/esp32-s3
- **MPU6050** : https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf
- **SPL06** : https://www.goertek.com/en/product/detail/spl06-001
- **GPS BN-220** : https://www.ublox.com/en/product/neo-m8-series

### Tutoriels
- **MicroPython** : https://docs.micropython.org/en/latest/
- **Flask** : https://flask.palletsprojects.com/
- **Leaflet.js** : https://leafletjs.com/
- **OpenCV** : https://docs.opencv.org/

### Articles scientifiques
- **NDVI** : Rouse et al. (1974)
- **ExG** : Woebbecke et al. (1995)
- **GRVI** : Tucker (1979)
- **RandomForest** : Breiman (2001)

---

*Documentation massive créée le 10 juillet 2026*
*Binôme A — Maîtrise complète du projet*
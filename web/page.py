# ====================== SIMULATION PAGE WEB pyDrone ======================
from flask import Flask, render_template_string
import time

app = Flask(__name__)

# Variables de simulation
battery = 85

HTML_TEMPLATE = """ 
<!DOCTYPE html>
<html>
<head>
    <title>pyDrone - Mission Planner (Simulation)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        body { font-family: Arial, sans-serif; margin:0; padding:10px; background:#f0f2f5; }
        .container { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; max-width: 1400px; margin:auto; }
        .panel { background: white; border-radius: 10px; padding: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.1); }
        .map-container { grid-column: 2; grid-row: 1 / span 5; height: 620px; }
        button { padding: 10px 15px; margin: 5px 3px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-warning { background: #ffc107; color: black; }
        .btn-info { background: #17a2b8; color: white; }
        #current { min-height: 70px; background: #e7f3ff; padding: 12px; border-radius: 6px; }
    </style>
</head>
<body>

<div class="container">

    <!-- Mesurer et Sauvegarder -->
    <div class="panel">
        <h2>📍 Mesurer Coordonnées</h2>
        <button class="btn-primary" onclick="measureGPS()">Mesurer Position Actuelle (GPS)</button>
        <div id="current">Coordonnées actuelles : En attente...</div>
        <hr>
        <button onclick="saveTo('WP')">Sauvegarder → WP</button>
        <button onclick="saveTo('HOME')">Sauvegarder → Home Point</button>
    </div>

    <!-- Waypoints -->
    <div class="panel">
        <h2>📍 Waypoints</h2>
        <div id="waypoints_list">Aucun waypoint défini</div>
        <button class="btn-success" onclick="sendWaypoints()">Envoyer tous les Waypoints</button>
    </div>

    <!-- Home Point -->
    <div class="panel">
        <h2>🏠 Home Point</h2>
        <div id="home_point_div">Non défini</div>
        <button class="btn-success" onclick="sendHomePoint()">Envoyer Home Point</button>
    </div>

    <!-- Commande Mission -->
    <div class="panel">
        <h2>🚀 Commande Mission</h2>
        <button class="btn-warning" style="width:100%; font-weight:bold;" onclick="generateTrajectory()">Générer la Trajectoire</button>
        <div id="status_mission" style="margin-top:10px; color: #666;">En attente des données...</div>
    </div>

    <!-- Batterie & Décision -->
    <div class="panel">
        <h2>🔋 État Batterie & Décision</h2>
        <div id="battery">Batterie : {{ battery }}%</div>
        <div id="decision">Décision : Prêt pour mission</div>
    </div>

    <!-- Résultats -->
    <div class="panel">
        <h2>📊 Résultats</h2>
        <button class="btn-info" onclick="showResults()">Afficher Résultat</button>
        <div id="results" style="margin-top:10px;">En attente de mission...</div>
    </div>

    <!-- Historiques -->
    <div class="panel">
        <h2>📖 Historiques</h2>
        <button class="btn-info" onclick="showHistory()">Afficher Historique</button>
        <div id="history" style="margin-top:10px;">Aucun vol enregistré</div>
    </div>

    <!-- Carte -->
    <div class="panel map-container">
        <h2>🗺️ Carte</h2>
        <div id="map" style="height: 580px;"></div>
    </div>

</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
    let map = L.map('map').setView([-18.8792, 47.5079], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    
    const droneIcon = L.divIcon({
        className: 'custom-div-icon',
        html: "<div style='font-size:24px;'>🚁</div>",
        iconSize: [30, 30],
        iconAnchor: [15, 15]
    });

    let currentPos = null;
    let waypoints = [];
    let homePoint = null;
    let wpSent = false;
    let homeSent = false;
    let missionFinished = false;
    
    let droneMarker = null; 
    let polyline = L.polyline([], {color: 'red', weight: 3, dashArray: '5, 10'}).addTo(map);

    function measureGPS() {
        currentPos = {
            lat: -18.8792 + (Math.random()*0.005 - 0.0025),
            lon: 47.5079 + (Math.random()*0.005 - 0.0025),
            alt: 0.8
        };
        document.getElementById('current').innerHTML = 
            `Lat: ${currentPos.lat.toFixed(6)}<br>Lon: ${currentPos.lon.toFixed(6)}<br>Alt: ${currentPos.alt} m`;
        L.circleMarker([currentPos.lat, currentPos.lon], {radius: 5, color: 'blue'}).addTo(map);
    }

    function saveTo(type) {
        if (!currentPos) return alert("Veuillez mesurer une position d'abord !");
        if (type === 'WP') {
            waypoints.push({...currentPos});
        } else if (type === 'HOME') {
            homePoint = {...currentPos};
            document.getElementById('home_point_div').innerHTML = `${homePoint.lat.toFixed(6)}, ${homePoint.lon.toFixed(6)}`;
        }
        updateWaypointsList();
    }

    function updateWaypointsList() {
        let html = '';
        waypoints.forEach((wp, i) => {
            html += `<p>WP${i+1}: ${wp.lat.toFixed(6)}, ${wp.lon.toFixed(6)}</p>`;
        });
        document.getElementById('waypoints_list').innerHTML = html || 'Aucun waypoint défini';
    }

    function sendWaypoints() {
        if(waypoints.length === 0) return alert("Ajoutez des waypoints avant d'envoyer !");
        wpSent = true;
        alert("✅ Waypoints reçus par le drone");
    }

    function sendHomePoint() {
        if(!homePoint) return alert("Définissez le Home Point avant d'envoyer !");
        homeSent = true;
        alert("✅ Home Point reçu par le drone");
    }

    async function generateTrajectory() {
        if (!wpSent || !homeSent) {
            alert("⚠️ Erreur : Vous devez d'abord envoyer les Waypoints ET le Home Point !");
            return;
        }

        document.getElementById('status_mission').innerHTML = "⏳ Génération en cours...";
        
        if (!droneMarker) {
            droneMarker = L.marker([homePoint.lat, homePoint.lon], {icon: droneIcon}).addTo(map);
        } else {
            droneMarker.setLatLng([homePoint.lat, homePoint.lon]);
        }

        let path = [[homePoint.lat, homePoint.lon]];
        polyline.setLatLngs(path);

        for (let wp of waypoints) {
            let startCoords = droneMarker.getLatLng();
            let endCoords = [wp.lat, wp.lon];
            await animateDrone(startCoords, endCoords);
            path.push(endCoords);
            polyline.setLatLngs(path);
        }

        document.getElementById('status_mission').innerHTML = "✅ Trajectoire générée et prête !";
        missionFinished = true;
    }

    function animateDrone(start, end) {
        return new Promise((resolve) => {
            let steps = 40;
            let i = 0;
            let interval = setInterval(() => {
                let lat = start.lat + (end[0] - start.lat) * (i / steps);
                let lng = start.lng + (end[1] - start.lng) * (i / steps);
                droneMarker.setLatLng([lat, lng]);
                if (i === steps) {
                    clearInterval(interval);
                    resolve();
                }
                i++;
            }, 30);
        });
    }

    function showResults() {
        if (!missionFinished) {
            document.getElementById('results').innerHTML = "⚠️ Aucune mission terminée.";
        } else {
            document.getElementById('results').innerHTML = `<strong>Succès:</strong> ${waypoints.length} waypoints parcourus à 0.8m d'altitude.`;
        }
    }

    function showHistory() {
        if (!missionFinished) {
            document.getElementById('history').innerHTML = "Aucun vol enregistré.";
        } else {
            let now = new Date().toLocaleTimeString();
            document.getElementById('history').innerHTML = `Vol du ${new Date().toLocaleDateString()} à ${now} - Effectué.`;
        }
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, battery=battery)

if __name__ == '__main__':
    print("🚀 Serveur pyDrone actif sur http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False, port=5000)
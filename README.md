# Drone Autonome - Detection Stress Hydrique

Binome A - L3 EIT - ESP Antsiranana - 2026
FANOGNY Hernandez Liwingston & RAKOTONIRINA Ny Antso Fyh Arihvony

## Materiel
- Pydrone 01Studio ESP32-S3
- Camera OV2640 66deg sans IR 850/940mm
- GPS BN-220 Ublox M8030

## Installation
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

## Structure
simulation/matlab  -> MATLAB UAV Toolbox
simulation/python  -> PyDrone-SIM
mission            -> Code vol MicroPython
imagerie           -> ExG SVM heatmap
web                -> Flask Leaflet
data/dataset       -> sain/ stresse/
docs               -> Notes
resultats          -> PNG CSV

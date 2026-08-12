# Protocole de suivi par capteur d'humidité du sol

## But

Produire une étiquette de stress fondée sur une mesure reproductible de l'humidité du substrat, et non uniquement sur l'apparence des feuilles.

## Matériel recommandé

- Capteur capacitif d'humidité du sol, de préférence plutôt qu'un capteur résistif sujet à la corrosion.
- Même profondeur d'insertion à chaque mesure.
- Un capteur fixe par groupe si le nombre de capteurs est limité, complété par des mesures tournantes sur les autres pots.
- Éprouvette ou récipient gradué pour noter les volumes d'arrosage.

## Étalonnage avant le début du protocole

1. Relever la valeur brute du capteur dans un substrat sec ou presque sec.
2. Arroser un pot jusqu'à humidification homogène sans eau stagnante.
3. Relever la valeur humide après stabilisation.
4. Conserver les deux valeurs dans le cahier d'essai.
5. Convertir ensuite chaque valeur brute en pourcentage relatif entre ces deux repères.

L'objectif est une comparaison entre groupes. La conversion n'est pas une teneur volumique certifiée sans étalonnage de laboratoire.

## Constitution des groupes

- 12 pots témoins : arrosage maintenant l'humidité de référence.
- 12 pots test : arrosage réduit progressivement après une courte acclimatation.
- Choisir des plants de même espèce, variété et stade autant que possible.
- Photographier un témoin et un plant test avec le même cadrage, à heure proche et sous une lumière comparable.

## Règle de stress recommandée

Après deux ou trois jours d'acclimatation, définir la moyenne d'humidité des témoins comme référence. Viser pour le groupe test environ 45 à 55 pour cent de cette référence, sans provoquer de dessèchement irréversible.

Exemple : si les témoins sont maintenus autour de 80 pour cent de l'échelle relative, le groupe test est maintenu autour de 40 pour cent. Cette règle doit être ajustée à l'observation des plants et validée par l'encadrant.

## Journal quotidien

Relever chaque jour avant arrosage, à une heure stable :

| Date | Pot | Groupe | Humidité relative | Volume d'eau | Aspect des feuilles | Image |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-08-13 | P01 | healthy | 78 | 120 mL | vert, turgide | P01_J00_V1.jpg |

Reporter la valeur mesurée dans `plants_mapping.csv` pour chaque image. Les images sans mesure d'humidité associée doivent être considérées comme faiblement documentées.

# flux_magasin
## Phénomènes à prendre en compte :
- Champ de vision des clients
- Répulsion des clients entre eux
- Attirance des clients vers les articles
- Entrée, Sortie et Paiement à la caisse (+cabines d'essayages)
- Modélisation de différents types de clients
## Implémentation
- Mur : 2 points
- Meubles à vêtements : 4 points + attirance
- Client : 
  - Position (x,y)
  - Vitesse (vx,vy)
  - temps restant
  - articles restants
  - répulsion
  - Calcul des forces répulsives et attractives dans le champ de vision -> accélération
- Entrée : 2 points + débit
- Sortie : 2 points
## Répartition des tâches
1. Lila : Visualisation graphique
2. Anne : Client
3. Corentin : Calcul des forces répulsives et attractives
4. Clément :

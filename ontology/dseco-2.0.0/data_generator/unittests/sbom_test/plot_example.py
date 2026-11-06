"""
Exemple d'utilisation de matplotlib pour créer des graphiques.
"""

import matplotlib.pyplot as plt
import numpy as np

# Créer des données
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Créer une figure avec deux sous-graphiques
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Premier graphique : Sinus
ax1.plot(x, y1, 'b-', linewidth=2, label='sin(x)')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('Fonction Sinus')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Deuxième graphique : Cosinus
ax2.plot(x, y2, 'r-', linewidth=2, label='cos(x)')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('Fonction Cosinus')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Ajuster l'espacement
plt.tight_layout()

# Sauvegarder le graphique
plt.savefig('graphique.png', dpi=150)
print("Graphique sauvegardé dans 'graphique.png'")

# Afficher le graphique
plt.show()

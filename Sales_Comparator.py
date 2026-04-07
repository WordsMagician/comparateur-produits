import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIGURATION
# =========================

FICHIER_ENTREE = "comparaison.csv"
DOSSIER_SORTIE = "output"

os.makedirs(DOSSIER_SORTIE, exist_ok=True)

# =========================
# CHARGEMENT DES DONNÉES
# =========================

df = pd.read_csv(FICHIER_ENTREE)

# =========================
# PRÉPARATION DES DONNÉES
# =========================

df["revenu"] = df["ventes"] * df["prix"]

# =========================
# ANALYSE
# =========================

# CA par produit
ca_par_produit = df.groupby("produit")["revenu"].sum().round(2)

# Classement complet
classement = ca_par_produit.sort_values(ascending=False)

# Meilleur et pire produit
meilleur_produit = classement.index[0]
pire_produit = classement.index[-1]

ca_meilleur = classement.iloc[0]
ca_pire = classement.iloc[-1]

# Écarts
ecart_euros = ca_meilleur - ca_pire
ecart_pourcentage = (ecart_euros / ca_pire) * 100

# Part du CA
total_ca = classement.sum()
part_ca = ((classement / total_ca) * 100).round(2)

# =========================
# TOP 3 MÉDAILLÉ
# =========================

medailles = ["🥇", "🥈", "🥉"]
top3 = classement.head(3)

top3_lignes = []

for i, (produit, ca) in enumerate(top3.items()):
    medal = medailles[i]
    part = part_ca[produit]
    top3_lignes.append(f"{medal} {produit} : {ca:.2f} € ({part:.2f} % du CA)")

top3_str = "\n".join(top3_lignes)

# =========================
# TEXTE & EXPORTS
# =========================

# Classement complet en texte
classement_str = classement.to_string()

# Conclusion
conclusion = (
    f"{meilleur_produit} surperforme {pire_produit} "
    f"de {ecart_euros:.2f} € soit {ecart_pourcentage:.2f} %."
)

# Rapport texte
rapport = f"""
=== COMPARAISON DES PRODUITS ===

Meilleur produit : {meilleur_produit}
Moins bon produit : {pire_produit}

CA du meilleur produit : {ca_meilleur:.2f} €
CA du moins bon produit : {ca_pire:.2f} €

Écart : {ecart_euros:.2f} €
Différence : {ecart_pourcentage:.2f} %

--- TOP 3 ---
{top3_str}

--- CLASSEMENT COMPLET ---
{classement_str}

Conclusion : {conclusion}
"""

print(rapport)

# Export rapport TXT
with open(os.path.join(DOSSIER_SORTIE, "rapport_comparaison.txt"), "w", encoding="utf-8") as f:
    f.write(rapport)

# Export classement CSV
classement_df = classement.reset_index()
classement_df.columns = ["produit", "chiffre_affaires"]
classement_df.to_csv(
    os.path.join(DOSSIER_SORTIE, "classement_produits.csv"),
    index=False,
    encoding="utf-8"
)

# =========================
# GRAPHIQUE CAMEMBERT
# =========================

plt.figure(figsize=(8, 8))
plt.pie(
    classement,
    labels=classement.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Répartition du chiffre d'affaires par produit")
plt.tight_layout()
plt.savefig(os.path.join(DOSSIER_SORTIE, "camembert_ca.png"))
plt.show()

# =========================
# BAR CHART PREMIUM
# =========================

plt.figure(figsize=(10, 6))

colors = []
for i in range(len(classement)):
    if i == 0:
        colors.append("gold")
    elif i == 1:
        colors.append("silver")
    elif i == 2:
        colors.append("#cd7f32")  # bronze
    else:
        colors.append("skyblue")

bars = plt.bar(classement.index, classement.values, color=colors)

plt.title("Classement des produits par chiffre d'affaires", fontsize=14)
plt.xlabel("Produit")
plt.ylabel("CA (€)")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

for bar in bars:
    hauteur = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        hauteur,
        f"{hauteur:.0f}€",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig(os.path.join(DOSSIER_SORTIE, "barres_ca_premium.png"))
plt.show()
import streamlit as st
from Classes import User, TransportActivity, FoodActivity, CarbonCalculator, ReportGenerator
import os

# Dictionnaires globaux
TRANSPORT_EMISSION_FACTORS = {
    "voiture": 0.192,
    "moto": 0.09,
    "bus_suburbain": 0.105,
    "Train électrique régional": 0.041,
    "avion": 0.255,
    "vélo": 0.0,
    "marche": 0.0
}

FOOD_EMISSION_FACTORS = {
    "boeuf": 27.0,
    "agneau": 39.0,
    "porc": 12.1,
    "volaille": 6.9,
    "poisson": 6.0,
    "œuf": 4.8,
    "produits_laitiers": 13.0,
    "céréales": 2.7,
    "légumes": 2.0,
    "fruits": 1.1
}

# Titre de la page
st.title("🌍 Suivi de l'Empreinte Carbone Personnelle")


# 1. Informations utilisateur

st.header("🧍 Informations utilisateur")

prenom = st.text_input("Prénom")
nom = st.text_input("Nom")

# ============================
# 2. Activité de transport
# ============================
st.subheader("🚗 Transport")

transport_modes = st.multiselect(
    "Mode(s) de transport utilisé(s)",
    list(TRANSPORT_EMISSION_FACTORS.keys())
)

transport_activities = []

for mode in transport_modes:
    distance = st.number_input(
        f"Distance journaliere parcourue avec {mode} (en km)",
        min_value=0.0,
        key=f"dist_{mode}"
    )
    if distance > 0:
        transport_activities.append(TransportActivity(nom=mode, valeur=distance))

# ============================
# 3. Activité alimentaire
# ============================
st.subheader("🍽️ Alimentation")

selected_foods = st.multiselect(
    "Sélectionnez les aliments que vous consommez régulièrement",
    list(FOOD_EMISSION_FACTORS.keys())
)

food_activities = []

for food in selected_foods:
    quantity = st.number_input(
        f"Quantité de {food} consommée par jour (en kg)",
        min_value=0.0,
        key=f"qty_{food}"
    )
    if quantity > 0:
        food_activities.append(FoodActivity(nom=food, valeur=quantity))

# ============================
# 4. Résultat + Rapport
# ============================
if st.button("📊 Calculer mon empreinte carbone"):
    if prenom and nom:
        # Création des objets
        user = User(prenom=prenom, nom=nom)
        calculator = CarbonCalculator(
            transport_activities=transport_activities,
            food_activities=food_activities
        )
        report = ReportGenerator(user=user, calculator=calculator)

        # Résultats
        total = calculator.calculer_emission_totale()
        st.success(f"✅ Émissions totales : {total:.2f} kg CO₂/jour")

        # Rapport texte
        rapport_txt = report.generate_text_report()
        st.text_area("📄 Rapport détaillé", rapport_txt, height=300)

        # Sauvegarde fichier texte avec encodage UTF-8
        with open("rapport.txt", "w", encoding="utf-8") as f:
            f.write(rapport_txt)

        # Générer le graphique
        report.generate_pie_chart("emissions_pie_chart.png")

        # Affichage image
        st.image("emissions_pie_chart.png", caption="Répartition des émissions de CO₂", use_container_width=True)

        # Téléchargement
        with open("rapport.txt", "rb") as f:
            st.download_button("⬇️ Télécharger le rapport texte", f, file_name="rapport.txt", mime="text/plain")

        with open("emissions_pie_chart.png", "rb") as f:
            st.download_button("⬇️ Télécharger le graphique", f, file_name="emissions_pie_chart.png", mime="image/png")

    else:
        st.error("❌ Veuillez renseigner votre prénom et nom avant de continuer.")

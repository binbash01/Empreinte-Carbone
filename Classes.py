import matplotlib.pyplot as plt
class User:
    def __init__(self, prenom, nom, liste=[]):
        self.nom = nom
        self.prenom = prenom
        self.activities = liste


class Activity:
    def __init__(self, nom, valeur):
        self.nom = nom
        self.valeur = valeur


class TransportActivity(Activity):
    def __init__(self, nom, valeur):
        Activity.__init__(self, nom, valeur) #valeur = distance_km
        self.facteur_emission_trans = {
            "voiture": 0.192,
            "moto": 0.09,
            "bus_suburbain": 0.105,
            "Train électrique régional": 0.041,
            "avion": 0.255,
            "vélo": 0.0,
            "marche": 0.0
        }

    def emission_trans(self):
            return self.valeur*self.facteur_emission_trans[self.nom]
        


class FoodActivity(Activity):
    def __init__(self, nom, valeur):  # valeur = quantite_aliments(Kg)
        Activity.__init__(self, nom, valeur)
        self.facteur_emission_alim = {
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

    def emission_alim(self):
        return self.valeur * self.facteur_emission_alim[self.nom]


class CarbonCalculator:
    def __init__(self, transport_activities=[], food_activities=[]):
        self.transport_activities = transport_activities
        self.food_activities = food_activities

    def total_transport_emissions(self):
        total = 0.0
        for activity in self.transport_activities:
            total += activity.emission_trans()
        return total

    def total_food_emissions(self):
        total = 0.0
        for activity in self.food_activities:
            total += activity.emission_alim()
        return total

    def calculer_emission_totale(self):
        return self.total_transport_emissions() + self.total_food_emissions()  




class ReportGenerator:
    def __init__(self, user, calculator):
        self.user = user
        self.calculator = calculator

    def generate_text_report(self):
        lines = [f"Rapport Empreinte Carbone - {self.user.prenom} {self.user.nom}\n"]
        
        lines.append("Activités de transport :")
        for activity in self.calculator.transport_activities:
            emission = activity.emission_trans()
            lines.append(f" - {activity.nom} : {activity.valeur} km → {emission:.2f} kg CO₂")

        lines.append("\nActivités alimentaires :")
        for activity in self.calculator.food_activities:
            emission = activity.emission_alim()
            lines.append(f" - {activity.nom} : {activity.valeur} kg → {emission:.2f} kg CO₂")

        total = self.calculator.calculer_emission_totale()
        lines.append(f"\nTOTAL ÉMISSIONS : {total:.2f} kg CO₂/jour")

        return "\n".join(lines)

    def save_as_txt(self, filename="rapport.txt"):
        report = self.generate_text_report()
        with open(filename, "w") as f:
            f.write(report)

    def generate_pie_chart(self, filename="emissions_pie_chart.png"):
        labels = []
        emissions = []

        # Transport
        for activity in self.calculator.transport_activities:
            emission = activity.emission_trans()
            if emission > 0:
                labels.append(f"Transport - {activity.nom}")
                emissions.append(emission)

        # Alimentation
        for activity in self.calculator.food_activities:
            emission = activity.emission_alim()
            if emission > 0:
                labels.append(f"Alimentation - {activity.nom}")
                emissions.append(emission)

        if emissions:
            plt.figure(figsize=(8, 6))
            plt.pie(emissions, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title("Répartition des émissions de CO₂")
            plt.axis('equal')  # cercle parfait
            plt.savefig(filename)
            plt.close()
        else:
            print("Aucune émission enregistrée, le graphique n’a pas été généré.")              
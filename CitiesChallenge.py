# Cities Challenge

class City:
    def __init__(self, name, country, population, landmarks):
        self.name = name
        self.country = country
        self.population = population
        self.landmarks = landmarks

new_york = City("New York", "USA", 8419600, ["Statue of Liberty", "Central Park", "Times Square"])
cardiff = City("Cardiff", "Wales", 364248, ["Cardiff Castle", "Principality Stadium", "National Museum Cardiff"])
milan = City("Milan", "Italy", 1378689, ["Duomo di Milano", "Castello Sforzesco", "Galleria Vittorio Emanuele II"])

print(vars(new_york))
print(vars(cardiff))
print(vars(milan))
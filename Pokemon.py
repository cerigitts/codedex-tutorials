# Pokemon Challenge

class Pokemon:
    def __init__(self, entry, name, types, description, caught):
        self.entry = entry #integer
        self.name = name #string
        self.types = types #list of strings
        self.description = description #string
        self.caught = caught #boolean
        
    def speak(self):
        print(f"{self.name}")
        print(f"{self.name}")

    def display(self):
        print(f"Entry: {self.entry}")
        print(f"Name: {self.name}")
        print(f"Type(s): {', '.join(self.types)}")
        print(f"Description: {self.description}")
        print(f"Caught: {'Yes' if self.caught else 'No'}")

pikachu = Pokemon(25, "Pikachu", ["Electric"], "It has small electric sacs on both its cheeks. If threatened, it looses electric charges from the sacs..", False)
charizard = Pokemon(6, "Charizard", ["Fire", "Flying"], "Spits fire that is hot enough to melt boulders. Known to cause forest fires unintentionally.", False)
nidoking = Pokemon(34, "Nidoking", ["Poison", "Ground"], "A Nidoking's thick tail packs enormously destructive power. It is capable of destroying a large boulder with one blow.", False)

pikachu.speak()
pikachu.display()

charizard.speak()
charizard.display()

nidoking.speak()
nidoking.display()
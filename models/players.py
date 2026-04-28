
class Zaidejas:
    def __init__(self, vardas, pavarde):
        self.vardas = vardas.strip()
        self.pavarde = pavarde.strip()
        self.pilnas_vardas = f"{self.vardas} {self.pavarde}"

    def __str__(self):
        return self.pilnas_vardas

    def __eq__(self, other):
        if not isinstance(other, Zaidejas):
            return False
        return self.pilnas_vardas.lower() == other.pilnas_vardas.lower()

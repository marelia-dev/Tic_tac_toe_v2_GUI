import random

from models.cpu import CPUZaidejas
from models.field import Laukas
from models.symbols import Symbols
from models.scores import Skaiciuokle
import time

class Zaidimas:
    def __init__(self, zaidejas1, zaidejas2):
        self.laukas = Laukas()
        self.symbols = Symbols()

        self.zaidejas1 = zaidejas1
        self.zaidejas2 = zaidejas2

        self.simbolis1 = self.symbols.get_x()
        self.simbolis2 = self.symbols.get_o()

        if hasattr(zaidejas1, 'mano_simbolis'):
            zaidejas1.mano_simbolis = self.simbolis1
            zaidejas1.oponento_simbolis  = self.simbolis2

        if hasattr(zaidejas2, 'mano_simbolis'):
            zaidejas2.mano_simbolis = self.simbolis2
            zaidejas2.oponento_simbolis = self.simbolis1

        self.einantis = zaidejas1

    def rodyti_lauka(self):
        self.laukas.rodyti()

    def legalus_einamas(self, pozicija):
        return not self.laukas.uzimtas(pozicija)

    def padaryti_ejima(self, pozicija):
        simbolis = self.simbolis1 if self.einantis == self.zaidejas1 else self.simbolis2
        self.laukas.uzdeti_simboli(pozicija, simbolis)

    def baigta(self):
        return self.laukas.baigta()

    def lygiosios(self):
        return self.laukas.lygiosios()

    def zaisti(self):
        print(f"\nNaujas zaidimas: {self.zaidejas1} {self.symbols.get_x()} vs {self.zaidejas2} {self.symbols.get_o()}")
        self.rodyti_lauka()

        laimejantis = None

        while True:
            try:
                if isinstance(self.einantis, CPUZaidejas):
                    #CPU daro ejima
                    poz = self.einantis.gauti_ejima(self.laukas)
                    print(f"{self.einantis} CPU {self.einantis.level} issirinko pozicija {poz}!")
                    time.sleep(0.5 + random.random() * 1.0)
                else:
                    poz = int(input(f"{self.einantis} ejimas (1-9): "))

                if 1 <= poz <= 9 and self.legalus_einamas(poz):
                    self.padaryti_ejima(poz)
                    self.rodyti_lauka()
                    # patikra
                    if self.baigta():
                        print(f"Laimejo {self.einantis}!")
                        laimejantis = self.einantis
                        break

                    if self.lygiosios():
                        print("Lygiosios!")
                        laimejantis = None
                        break

                    self.einantis = self.zaidejas2 if self.einantis == self.zaidejas1 else self.zaidejas1

                else:
                    if not isinstance(self.einantis, CPUZaidejas):
                        print("Netinkamas ejimas! 1-9 arba laisvas langelis.")

            except ValueError:
                if not isinstance(self.einantis, CPUZaidejas):
                    print("Iveskite skaiciu 1-9!")


        skaiciuokle = Skaiciuokle()
        skaiciuokle.prideti_rezultata(self.zaidejas1, self.zaidejas2, laimejantis)
        skaiciuokle.rodyti_skaiciu()

        return laimejantis


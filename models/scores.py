import pickle

class Skaiciuokle:
    def __init__(self):
        self.failas = "zaidejai.pkl"
        self.skaicius = self.nuskaityti()

    def nuskaityti(self):
        try:
            with open(self.failas, "rb") as f:
                return pickle.load(f)
        except:
            return {}

    def irasyti(self):
        with open(self.failas, "wb") as f:
            pickle.dump(self.skaicius, f)

    def prideti_zaideja(self, zaidejas):
        pilnas = zaidejas.pilnas_vardas.lower()
        if pilnas not in self.skaicius:
            self.skaicius[pilnas] = {'p': 0, 'pr': 0, 'l': 0, 'total_games': 0}
            self.irasyti()
            print("Zaidejas pridetas.")
        else:
            print("Toks zaidejas jau egzistuoja!")

    def prideti_rezultata(self, zaidejas1, zaidejas2, laimejantis=None):
        pilnas1 = getattr(zaidejas1, 'pilnas_vardas', None)
        if pilnas1:
            pilnas1 = pilnas1.lower()

        pilnas2 = getattr(zaidejas2, 'pilnas_vardas', None)
        if pilnas2:
            pilnas2 = pilnas2.lower()

        # zaideju iniciacija
        if pilnas1 and pilnas1 not in self.skaicius:
            self.skaicius[pilnas1] = {'p': 0, 'pr': 0, 'l': 0, 'total_games': 0}

        if pilnas2 and pilnas2 not in self.skaicius:
            self.skaicius[pilnas2] = {'p': 0, 'pr': 0, 'l': 0, 'total_games': 0}

        #atnaujinam jei zaidzia zmogus
        if pilnas1:
            self.skaicius[pilnas1]['total_games'] += 1
            if laimejantis == zaidejas1:
                self.skaicius[pilnas1]['p'] += 1
            elif laimejantis is None:
                self.skaicius[pilnas1]['l'] += 1
            else:
                self.skaicius[pilnas1]['pr'] += 1

        if pilnas2:
            self.skaicius[pilnas2]['total_games'] += 1
            if laimejantis == zaidejas2:
                self.skaicius[pilnas2]['p'] += 1
            elif laimejantis is None:
                self.skaicius[pilnas2]['l'] += 1
            else:
                self.skaicius[pilnas2]['pr'] += 1

        if pilnas1 or pilnas2:
            self.irasyti()

    def rodyti_skaiciu(self):
        if not self.skaicius:
            print("Nera zaideju.")
            return

        surusiuoti = sorted(
            [(k, v) for k, v in self.skaicius.items() if k is not None],
            key=lambda x: (x[1]['p'], x[1]['total_games']),
            reverse=True
        )

        print("\n=== Zaideju statistika ===")
        print(f"{'TOP':<4} {'Zaidejas':<25} {'Pergales':<10} {'Pralaimejimai':<15} {'Lygiosios':<12} {'Viso zaidimu':<15}")
        print("-" * 90)

        for vieta, (vardas, stats) in enumerate(surusiuoti, 1):
            print(f"{vieta:<4} {vardas:<25} {stats['p']:<10} {stats['pr']:<15} {stats['l']:<12} {stats['total_games']:<15}")

        print("-" * 90)

        if surusiuoti:
            top1 = surusiuoti[0][0]
            print(f"TOP 1 pagal pergales: {top1}")
class Laukas:
    def __init__(self):
        self.langeliai = ['  ' for _ in range(9)]

    def rodyti(self):
        s = self.langeliai
        print("\n   1   |  2   |  3   ")
        print(f"1  {s[0]}  |  {s[1]}  |  {s[2]}  ")
        print(" ------+------+------")
        print(f"4  {s[3]}  |  {s[4]}  |  {s[5]}  ")
        print(" ------+------+------")
        print(f"7  {s[6]}  |  {s[7]}  |  {s[8]}  ")

    def uzimtas(self, pozicija):
        val = self.langeliai[pozicija - 1]
        return val != '  '

    def uzdeti_simboli(self, pozicija, simbolis):
        self.langeliai[pozicija - 1] = simbolis

    def baigta(self):
            def nelaisvas(v):
                return v != '  '
            # Eiles
            for i in range(0, 9, 3):
                if nelaisvas(self.langeliai[i]) and \
                    self.langeliai[i] == self.langeliai[i+1] == self.langeliai[i+2]:
                    return True
            # Stulpeliai
            for i in range(3):
                if nelaisvas(self.langeliai[i]) and \
                    self.langeliai[i] == self.langeliai[i+3] == self.langeliai[i+6]:
                    return True

            # Istrizaines
            if nelaisvas(self.langeliai[0]) and \
                    self.langeliai[0] == self.langeliai[4] == self.langeliai[8]:
                return True
            if nelaisvas(self.langeliai[2]) and \
                    self.langeliai[2] == self.langeliai[4] == self.langeliai[6]:
                return True

            return False

    def lygiosios(self):
        return '  ' not in self.langeliai

